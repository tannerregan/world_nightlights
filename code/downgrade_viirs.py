#Downgrade VIIRS to match DMSP
#imports-----------------------------------------------------------------------
import rasterio as rio
import numpy as np
import pandas as pd
import time
from scipy.ndimage import uniform_filter
from rasterio import warp
from sklearn.ensemble import ExtraTreesRegressor

#Functions---------------------------------------------------------------------
def open_profile(aoi_f):
    with rio.open(aoi_f) as aoi_o:
        profile = aoi_o.profile
    return profile

def open_viirs_data(viirs_f,aoi_gas,aoi_bff,aoi_rgn,jdir,year, prf): 
    #regions as array
    argn_o=rio.open(aoi_rgn)  
    argn_a=argn_o.read(1)
    
    #mask as array: combine two masks as one (mask is 1 if gas flares=1 or AOI land=0)
    gasm_o=rio.open(aoi_gas)   
    aoim_o=rio.open(aoi_bff)  
    mask_a=((gasm_o.read(1)==1) | (aoim_o.read(1)==0)) 
    
    #viirs as arrays: resample VIIRS to DMSP resolution, do this for four types of resampling (mean=5, median=10, min=9, and max=8)
    viirs_o=rio.open(viirs_f.format(y=year)) #need to downsample first
    viirs_b=rio.band(viirs_o,1)
    new_prf=prf.copy()
    new_prf.update(
        dtype=viirs_b.dtype,)
    viirs_a=[]
    for stat in [5,10,9,8]:
        tmp_f=jdir+"viirs_rsmp_{s}.tif".format(s=stat)
        print('resampling VIIRS to DMSP resolution by stat '+str(stat)+' where (mean=5, median=10, min=9, and max=8)')
        with rio.open(tmp_f, 'w', **new_prf) as out_dst:
            out_o=rio.band(out_dst,1)
            warp.reproject(viirs_b,out_o,dst_transform=new_prf['transform'],dst_crs=new_prf['crs'],dst_nodata=new_prf['nodata'], resampling=stat)
        viirs_a.append(rio.open(tmp_f).read(1))
        
    viirs_mn_a=viirs_a[0]
    viirs_md_a=viirs_a[1]
    viirs_mi_a=viirs_a[2]
    viirs_mx_a=viirs_a[3]
    
    open_names=["VIIRS_mn", "VIIRS_md", "VIIRS_mi", "VIIRS_mx", "AOI Regions"]
    open_arrays=[viirs_mn_a, viirs_md_a, viirs_mi_a, viirs_mx_a,argn_a]
    
    return open_arrays, open_names, mask_a

def add_uni_filters(viirs_a):
    arrays=[]
    names=[]
    st=time.time()
        
    for w in [3,5,7,9,11,13,17,21]:
        print('running local filters on VIIRS mn for window='+str(w))
        
        #Uniform filter
        filter_u = uniform_filter(viirs_a,size=w, mode='constant',cval=0)
        arrays.append(filter_u)
        names.append('VIIRS_mn_uni'+str(w))
        
        #Variance filter
        filter_sq=uniform_filter(viirs_a**2,size=w, mode='constant',cval=0)
        filter_var=filter_sq - filter_u**2
        arrays.append(filter_var)
        names.append('VIIRS_mn_var'+str(w))      
        
        print('elapsed time: '+time.strftime("%H:%M:%S", time.gmtime(time.time() - st)))
        st=time.time()
        #end loop
        
    return arrays,names

def add_dmsp_data(dmsp_f,year):
    names=[]
    arrays=[]
    dmsp_o=rio.open(dmsp_f.format(y=year))  
    dmsp_a=dmsp_o.read(1) 
    arrays.append(dmsp_a)
    names.append('DMSP')
      
    return arrays,names

def arrays_to_frame(arrays,names,mask_a):
    mask_c=np.reshape(mask_a,(-1,1))
    df=pd.DataFrame(mask_c, columns=['mask']) #import the full array into a df- NB: this is important because the index (ubercode) can later on be used to convert back to (x,y) cell coordinates.
    df=df[(df['mask']==0)]  #exclude gas and AOI masked areas now that we have an index for each cell/row    
    df=df.drop(['mask'], axis=1) #drop the mask column
    
    for i,a in enumerate(arrays):
        print('adding new column: '+names[i])
        c=a[mask_a==0] #mask out cells, and convert to a 1D column
        df[names[i]]=c[mask_c] #add to dataframe as new column
    return df

def open_etr_train_data(dmsp_f,viirs_f,aoi_gas,aoi_bff,aoi_rgn,jdir,year,prf):     
    #get the viirs data at DMSP resolution (resampling with mean, median, min, max) and geographical regions, and data mask
    viirs_arrays,viirs_names,mask_array=open_viirs_data(viirs_f,aoi_gas,aoi_bff,aoi_rgn,jdir,year,prf)  #open VIIRS data
    viirs_df=arrays_to_frame(viirs_arrays,viirs_names, mask_array)
    del viirs_arrays[1:], viirs_names[1:] #don't delete the mean that will be used in the next step
    
    #run uniform filters to get local means and variances over different window sizes on the mean VIIRS array
    if viirs_names[0]=='VIIRS_mn': #Ensure that we use mean VIIRS for the filter
        fltr_arrays,fltr_names=add_uni_filters(viirs_arrays[0]) #add spatial filters
    else:
        raise NameError('VIIRS_mn in wrong place of array list!')
    fltr_df=arrays_to_frame(fltr_arrays,fltr_names, mask_array)
    del fltr_arrays, viirs_arrays
        
    
    #get the DMSP data that will be used as 'groundtruth' in model prediction
    dmsp_arrays,dmsp_names=add_dmsp_data(dmsp_f,year) #add DMSP
    dmsp_df=arrays_to_frame(dmsp_arrays,dmsp_names, mask_array)
    del dmsp_arrays, mask_array
    
    #merge all dataframes together
    df = pd.merge(viirs_df, fltr_df, left_index=True, right_index=True, how='inner')
    del viirs_df, fltr_df
    df = pd.merge(df, dmsp_df, left_index=True, right_index=True, how='inner')
    del dmsp_df
    
    return df

def train_ETR(df,importance_csv):
    #a) pick a random sample to train on (10% of data from each region)
    df = df.groupby('AOI Regions').apply(lambda x: x.sample(frac=0.10,random_state=2406))
   
    #b) add indicators for regions
    for c in df.columns: #Make sure there are no missings
        if df[c].isna().sum()!=0:
            raise NameError('Missing data for column '+c+'!')
    df=pd.get_dummies(df,columns=['AOI Regions'])
            
    #c) Best parameters from a random grid search with 1% of sample, 10 iterations, 3 crossfolds
    best_params={'n_estimators': 150, 'min_samples_split': 16, 'min_samples_leaf': 4, 
                 'max_features': 'sqrt', 'max_depth': 110, 'bootstrap': True}
    
    #d) fit the best ETR model
    Best_ETR=ExtraTreesRegressor(**best_params)
    Best_ETR.fit(df.drop(['DMSP'],axis=1),df['DMSP'])
     
    #e) Save feature importances save to csv
    if importance_csv!=None:
        importances=pd.DataFrame()
        importances['feature']=df.drop(['DMSP'],axis=1).columns
        importances['ETR']=pd.Series(Best_ETR.feature_importances_)
        importances=importances.sort_values(by=['ETR'],ascending=False)
        importances.to_csv(importance_csv)
    
    return Best_ETR
    
def save_to_file(in_a,out_f,prf):
    with rio.open(out_f, 'w', **prf) as dst:
        dst.write(in_a, 1)  
        
def write_predictions_to_raster(df,prf,is_topcoded,fn):
    #need to add x and y coordinates from index/"ubercode"
    #NB: the index or "ubercode" gives the cell location in the raster grid starting at the top left, moving across columns, then down rows 
    df.loc[:,'y']=np.floor(df.index/prf['width']).astype(int)
    df.loc[:,'x']=(df.index-df.y*prf['width']).astype(int)
        
    #covert pandas column to a numpy array
    df = df[['x', 'y', 'dmsp_hat']] #DF needs to be in order: x,y,dmsp
    pix_fix=df.to_numpy() 
    shape_out=(prf['height'],prf['width'])
    dmsp_hat = 0 * np.empty(shape=shape_out)
    dmsp_hat[pix_fix.transpose()[1].astype(int), pix_fix.transpose()[0].astype(int)] = pix_fix.transpose()[2]
    
    #save array as raster
    new_prf=prf.copy() 
    dmsp_hat[(dmsp_hat<0)]=0 #bottomcode
    dmsp_hat=np.around(dmsp_hat, decimals=0) #round to integer
    if is_topcoded==1:
        dmsp_hat[(dmsp_hat>63)]=63 #topcode
        dmsp_hat=dmsp_hat.astype(np.uint8) #store as 8bit integer for non topcoding corrected
        new_prf['dtype']=rio.uint8
    if is_topcoded==0:
        dmsp_hat=dmsp_hat.astype(np.int32) #store as 32bit integer for topcoding
        new_prf['dtype']=rio.int32
    save_to_file(dmsp_hat,fn,new_prf)   

def predict_batch(model, data, batch_size=1e6):
    predictions = np.array([])
    for i in range(0, len(data), int(batch_size)):
        batch = data.iloc[int(i):int(i+batch_size)]
        batch_predictions = model.predict(batch)
        predictions=np.append(predictions,batch_predictions)
    return predictions

def etr_predict_save(Best_ETR,is_topcoded,df,year,prf,out_f):
    #a) open contemporaneous VIIRS, apply model.
    #prdct_df=open_etr_prdct_data(viirs_f,aoi_gas,aoi_bff,aoi_rgn,jdir,year,prf)
    
    #a) add indicators for regions
    for c in df.columns: #Make sure there are no missings
        if df[c].isna().sum()!=0:
            raise NameError('Missing data for column '+c+'!')
    df=pd.get_dummies(df,columns=['AOI Regions'])
    
    #b) apply prediction (in batches)
    df['dmsp_hat'] = predict_batch(Best_ETR, df)
    df=df.loc[:, ['dmsp_hat']] #Only need predictions from here
    
    #c)save to file
    write_predictions_to_raster(df,prf,is_topcoded,out_f.format(y=year))


def main(dmsp_f,viirs_f,aoi_gas,aoi_bff,aoi_rgn,jdir,val_f):
    ifn=dmsp_f.rsplit('/', 1)[-1]
    print("Downgrading VIIRS based on "+ifn)
    start_time=time.time()
    
    aoi_prf=open_profile(aoi_rgn)
    
    #1) Open training data (random sample of 2013) 
    train_df=open_etr_train_data(dmsp_f,viirs_f,aoi_gas,aoi_bff,aoi_rgn,jdir,year='2013',prf=aoi_prf)
    is_topcoded=(train_df['DMSP'].max()<64) #record whether data is topcoded or not
    
    #2) Train ETR on DMSP in 2013
    print("Start model training ")
    Best_ETR=train_ETR(train_df,importance_csv=val_f.rsplit('/', 1)[0]+"/importances_ETR_"+ifn[:-4].format(y=2013)+".csv")
    train_df=train_df.drop(['DMSP'],axis=1)
    print('Setup time: '+time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time)))
        
    #3) Predict using Best ETR for all years 2014-2020 (open data, predict DMSP, save predictions to file)
    for y in range(2014,2023+1):
        print("Downgrading VIIRS in "+str(y))
        start_time=time.time()
        etr_predict_save(Best_ETR,is_topcoded,train_df,str(y),aoi_prf,dmsp_f)
        print('Predict time: '+time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time)))
        
    #v0) EXTRAS for validation----
    #v1) Add for validation (predict 2012 with 2013)

    suffix=dmsp_f.split('_')[-1]
    suffix=suffix.split('.')[0]
    print("Adding extras for validation of "+suffix+"-------------------")
    start_time=time.time()
    out_f=val_f.format(y='2012',c=suffix)
    etr_predict_save(Best_ETR,is_topcoded,train_df,'2012',aoi_prf,out_f)
    
    #v2) Add for validation (predict 2013 with 2012)
    del train_df
    print("Adding extras for validation of 2013 "+suffix)
    start_time=time.time()
    #y1) Open training data (random sample of 2012) 
    train_df=open_etr_train_data(dmsp_f,viirs_f,aoi_gas,aoi_bff,aoi_rgn,jdir,year='2012',prf=aoi_prf)
    is_topcoded=(train_df['DMSP'].max()<64) #record whether data is topcoded or not
    
    #v3) Train ETR on DMSP in 2012
    Best_ETR=train_ETR(train_df,importance_csv=val_f.rsplit('/', 1)[0]+"/importances_ETR_"+ifn[:-4].format(y=2012)+".csv")
    train_df=train_df.drop(['DMSP'],axis=1)
    print('Setup time: '+time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time)))
    
    #v4) Predict using Best ETR for 2013
    start_time=time.time()
    out_f=val_f.format(y='2013',c=suffix)
    etr_predict_save(Best_ETR,is_topcoded,train_df,'2013',aoi_prf,out_f)
    print('Predict time: '+time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time)))
    
    
#SCRIPT------------------------------------------------------------------------
# execute only if run as a script
if __name__ == "__main__":
    main(dmsp_f,viirs_f,aoi_gas,aoi_bff,aoi_rgn,jdir,val_f)
     
#END---------------------------------------------------------------------------


        

