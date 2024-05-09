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

"""VERSION 1
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
            destination=rio.band(out_dst,1)
            warp.reproject(viirs_b,destination,dst_transform=new_prf['transform'],dst_crs=new_prf['crs'],dst_nodata=new_prf['nodata'], resampling=stat)
        viirs_a.append(rio.open(tmp_f).read(1))
        
    viirs_mn_a=viirs_a[0]
    viirs_md_a=viirs_a[1]
    viirs_mi_a=viirs_a[2]
    viirs_mx_a=viirs_a[3]
    
    open_names=["VIIRS_mn", "VIIRS_md", "VIIRS_mi", "VIIRS_mx", "AOI Regions", "mask"]
    open_arrays=[viirs_mn_a, viirs_md_a, viirs_mi_a, viirs_mx_a,argn_a, mask_a]
    stacked=np.stack(open_arrays,axis=0) 
    for a in open_arrays:
        del a
    
    return stacked, open_names

def data_to_frame(stacked,col_names):
    columns=np.transpose(np.reshape(stacked,(len(col_names),-1)))
    df=pd.DataFrame(columns, columns=col_names)
    df=df[(df['mask']==0)]  #exclude gas and AOI masked areas    
    df=df.drop(['mask'], axis=1)
    return df
"""

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

def add_xy_data(data,names,prf):  
    grid=np.stack((np.meshgrid(np.arange(prf['width']), np.arange(prf['height'])))) #add a grid of coordinates
    data=np.concatenate((data,grid),axis=0) 
    names.append('x')
    names.append('y')
    
    return data,names


def arrays_to_frame(arrays,names,mask_a):
    mask_c=np.transpose(np.reshape(mask_a,(1,-1)))
    df=pd.DataFrame(mask_c, columns=['mask'])
    
    for i,a in enumerate(arrays):
        print('adding new column: '+names[i])
        c=np.transpose(np.reshape(a,(1,-1))) #reshape array from 2D to 1D column
        df[names[i]]=c
            
    df=df[(df['mask']==0)]  #exclude gas and AOI masked areas    
    df=df.drop(['mask'], axis=1)
    return df


def open_etr_train_data(dmsp_f,viirs_f,aoi_gas,aoi_bff,aoi_rgn,jdir,year,prf):     
    #get the viirs data at DMSP resolution (resampling with mean, median, min, max) and geographical regions, and data mask
    viirs_arrays,viirs_names,mask_array=open_viirs_data(viirs_f,aoi_gas,aoi_bff,aoi_rgn,jdir,year,prf)  #open VIIRS data
    viirs_df=arrays_to_frame(viirs_arrays,viirs_names, mask_array)

    print('viirs dataframe using '+str(round(viirs_df.memory_usage(deep=True).sum()/1e9,1))+'GB of memory')
    del viirs_arrays[1:], viirs_names[1:] #don't delete the mean that will be used in the next step
    
    
    #run uniform filters to get local means and variances over different window sizes on the mean VIIRS array
    if viirs_names[0]=='VIIRS_mn': #Ensure that we use mean VIIRS for the filter
        fltr_arrays,fltr_names=add_uni_filters(viirs_arrays[0]) #add spatial filters
    else:
        raise NameError('VIIRS_mn in wrong place of array list!')
    fltr_df=arrays_to_frame(fltr_arrays,fltr_names, mask_array)
        
    print('filter dataframe using '+str(round(fltr_df.memory_usage(deep=True).sum()/1e9,1))+'GB of memory')
    del fltr_arrays, viirs_arrays
        
    
    #get the DMSP data that will be used as 'groundtruth' in model prediction
    dmsp_arrays,dmsp_names=add_dmsp_data(dmsp_f,year) #add DMSP
    dmsp_df=arrays_to_frame(dmsp_arrays,dmsp_names, mask_array)
        
    print('dmsp dataframe using '+str(round(fltr_df.memory_usage(deep=True).sum()/1e9,1))+'GB of memory')
    del dmsp_arrays, mask_array
    
    #merge all dataframes together
    df = pd.merge(viirs_df, fltr_df, left_index=True, right_index=True, how='inner')
    del viirs_df, fltr_df
    df = pd.merge(merged_df, dmsp_df, left_index=True, right_index=True, how='inner')
    del dmsp_df
    
    return df


    
ifn=dmsp_f.rsplit('/', 1)[-1]
print("Downgrading VIIRS based on "+ifn)
start_time=time.time()
aoi_prf=open_profile(aoi_rgn)


dmsp_f=dmsp_cln
viirs_f=viirs_cln
prf=aoi_prf
year='2013'







Maybe move this so it is inside the ETR prediction
np.random.seed(0) ; df=df[(np.random.rand(len(df)) < 0.1)] #sample just 10% of the data (otherwise takes a long time to run)
del stacked_inputs,stacked_names
    
#add indicators for regions
for c in df.columns: #Make sure there are no missings
    if df[c].isna().sum()!=0:
        raise NameError('Missing data for column '+c+'!')
df=pd.get_dummies(df,columns=['AOI Regions'])
    
    
def open_etr_prdct_data(viirs_f,aoi_gas,aoi_bff,aoi_rgn,jdir,year,prf):
    stacked_inputs,stacked_names=open_viirs_data(viirs_f,aoi_gas,aoi_bff,aoi_rgn,jdir,year,prf)  #open VIIRS data
    stacked_inputs,stacked_names=add_uni_filters(stacked_inputs,stacked_names) #add spatial filters
    stacked_inputs,stacked_names=add_xy_data(stacked_inputs,stacked_names,prf) #Add x,y to identify each cell
    ^^ I think this is redundant, already given by index. BUT currently used to map predictions back to raster, so need an alternative if skipping this. Can double check that the index can be unpacked into x and y
    
    df=data_to_frame(stacked_inputs,stacked_names)
    del stacked_inputs,stacked_names
    
    for c in df.columns: #Make sure there are no missings
        if df[c].isna().sum()!=0:
            raise NameError('Missing data for column '+c+'!')
    df=pd.get_dummies(df,columns=['AOI Regions'])
    
    return df

def save_to_file(in_a,out_f,prf):
    with rio.open(out_f, 'w', **prf) as dst:
        dst.write(in_a, 1)  
        
def write_predictions_to_raster(df,prf,is_topcoded,fn):
    pix_fix=df.to_numpy() #DF needs to be in order: x,y,z
    shape_out=(prf['height'],prf['width'])
    dmsp_hat = 0 * np.empty(shape=shape_out)
    dmsp_hat[pix_fix.transpose()[1].astype(int), pix_fix.transpose()[0].astype(int)] = pix_fix.transpose()[2]
    
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


def train_ETR(df,importance_csv):
    
    #pick a random sample to train on
    
    # add indicators for regions
    make sure these always give the same values
    
    #Best parameters from a random grid search with 1% of sample, 10 iterations, 3 crossfolds
    best_params={'n_estimators': 150, 'min_samples_split': 16, 'min_samples_leaf': 4, 
                 'max_features': 'sqrt', 'max_depth': 110, 'bootstrap': True}
    
    # fit the best ETR model
    Best_ETR=ExtraTreesRegressor(**best_params)
    Best_ETR.fit(df.drop(['DMSP'],axis=1),df['DMSP'])
     
    # Save feature importances save to csv
    if importance_csv!=None:
        importances=pd.DataFrame()
        importances['feature']=df.drop(['DMSP'],axis=1).columns
        importances['ETR']=pd.Series(Best_ETR.feature_importances_)
        importances=importances.sort_values(by=['ETR'],ascending=False)
        importances.to_csv(importance_csv)
    
    return Best_ETR

def etr_predict_save(Best_ETR,is_topcoded,out_f,viirs_f,aoi_gas,aoi_bff,aoi_rgn,jdir,year,prf):
    #a) open contemporaneous VIIRS, apply model.
    prdct_df=open_etr_prdct_data(viirs_f,aoi_gas,aoi_bff,aoi_rgn,jdir,year,prf)
    #b) apply prediction
    prdct_df['dmsp_hat']=Best_ETR.predict(prdct_df.drop(['x','y'], axis=1))
    #c)save to file
    write_predictions_to_raster(df=prdct_df[['x','y','dmsp_hat']],
                        prf=prf,
                        is_topcoded=is_topcoded,
                        fn=out_f.format(y=year))

def main(dmsp_f,viirs_f,aoi_gas,aoi_bff,aoi_rgn,jdir,val_f):
    ifn=dmsp_f.rsplit('/', 1)[-1]
    print("Downgrading VIIRS based on "+ifn)
    start_time=time.time()
    
    aoi_prf=open_profile(aoi_rgn)
    
    #1) Open training data (random sample of 2013) 
    train_df=open_etr_train_data(dmsp_f,viirs_f,aoi_gas,aoi_bff,aoi_rgn,jdir,year='2013',prf=aoi_prf)
    is_topcoded=(train_df['DMSP'].max()<64) #record whether data is topcoded or not
    
    #2) Train ETR on DMSP in 2013
    Best_ETR=train_ETR(train_df,importance_csv=home+"/figures/importances_ETR_"+ifn[:-4].format(y=2013)+".csv")
    del train_df
    print('Setup time: '+time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time)))
    

    #3) Predict using Best ETR for all years 2014-2020 (open data, predict DMSP, save predictions to file)
    for y in range(2014,2020+1):
        print("Downgrading VIIRS in "+str(y))
        start_time=time.time()
        etr_predict_save(Best_ETR,is_topcoded,dmsp_f,viirs_f,aoi_gas,aoi_bff,aoi_rgn,jdir,year=str(y),prf=aoi_prf)
        print('Predict time: '+time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time)))
        
    #EXTRAS for validation----
    #x) Add for validation (predict 2012 with 2013)
    suffix=dmsp_f.split('_')[-1]
    suffix=suffix.split('.')[0]
    print("Adding extras for validation of "+suffix)
    out_f=val_f.format(y='2012',c=suffix)
    etr_predict_save(Best_ETR,is_topcoded,out_f,viirs_f,aoi_gas,aoi_bff,aoi_rgn,jdir,year='2012',prf=aoi_prf)
    
    #y) Add for validation (predict 2013 with 2012)
    print("Adding extras for validation of 2013 "+suffix)
    #y1) Open training data (random sample of 2012) 
    train_df=open_etr_train_data(dmsp_f,viirs_f,aoi_gas,aoi_bff,aoi_rgn,jdir,year='2012',prf=aoi_prf)
    is_topcoded=(train_df['DMSP'].max()<64) #record whether data is topcoded or not
    
    #y2) Train ETR on DMSP in 2012
    Best_ETR=train_ETR(train_df,importance_csv=None)
    del train_df
    
    #y3) Predict using Best ETR fo2 2013
    out_f=val_f.format(y='2013',c=suffix)
    etr_predict_save(Best_ETR,is_topcoded,out_f,viirs_f,aoi_gas,aoi_bff,aoi_rgn,jdir,year='2013',prf=aoi_prf)

    
#SCRIPT------------------------------------------------------------------------
# execute only if run as a script
if __name__ == "__main__":
    main(dmsp_f,viirs_f,aoi_gas,aoi_bff,aoi_rgn,jdir,val_f)
     
#END---------------------------------------------------------------------------


        

