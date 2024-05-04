#Do topcoding corrections on a DMSP image following the procedure of Bluhm and Krause 2020
#imports-----------------------------------------------------------------------
import rasterio, pandas, time
from scipy.ndimage.filters import uniform_filter
from rasterio import warp
import numpy as np
from sklearn.ensemble import ExtraTreesRegressor

#Functions---------------------------------------------------------------------
def open_viirs_data(viirs_f,afr_gas,afr_bff,afr_rgn,jdir,year, prf):
    viirs_o=rasterio.open(viirs_f.format(y=year)) #need to downsample first
    gasm_o=rasterio.open(afr_gas)   
    afrm_o=rasterio.open(afr_bff)   
    argn_o=rasterio.open(afr_rgn)  

    #regions as array
    argn_a=argn_o.read(1)
        
    #mask as array: combine two masks as one (mask is 1 if gas flares=1 or africa land=0)
    mask_a=((gasm_o.read(1)==1) | (afrm_o.read(1)==0)) 
    
    #viirs as arrays: resample VIIRS to DMSP resolution, do this for four types of resampling (mean=5, median=10, min=9, and max=8)
    viirs_b=rasterio.band(viirs_o,1)
    new_prf=prf.copy()
    new_prf.update(
        dtype=viirs_b.dtype,)
    viirs_a=[]
    for stat in [5,10,9,8]:
        tmp_f=jdir+"viirs_rsmp_{s}.tif".format(s=stat)
        with rasterio.open(tmp_f, 'w', **new_prf) as out_dst:
            destination=rasterio.band(out_dst,1)
            warp.reproject(viirs_b,destination,dst_transform=new_prf['transform'],dst_crs=new_prf['crs'],dst_nodata=new_prf['nodata'], resampling=stat)
        viirs_a.append(rasterio.open(tmp_f).read(1))
        
    viirs_mn_a=viirs_a[0]
    viirs_md_a=viirs_a[1]
    viirs_mi_a=viirs_a[2]
    viirs_mx_a=viirs_a[3]
    
    open_names=["VIIRS_mn", "VIIRS_md", "VIIRS_mi", "VIIRS_mx", "Africa Regions", "mask"]
    open_arrays=[viirs_mn_a, viirs_md_a, viirs_mi_a, viirs_mx_a,argn_a, mask_a]
    stacked=np.stack(open_arrays,axis=0) 
    for a in open_arrays:
        del a
    
    return stacked, open_names

def add_uni_filters(data,names):
    viirs_loc_in_list=0
    if names[viirs_loc_in_list]!='VIIRS_mn': #Ensure that we use VIIRS for the filter
        raise NameError('VIIRS_mn in wrong place of stacked arrays!')
    for w in [3,5,7,9,11,13,17,21]:
        #Uniform filter
        filter_u = uniform_filter(data[viirs_loc_in_list],size=w, mode='constant',cval=0)
        data=np.concatenate((data,filter_u[None,:, :,]), axis=0) #Need to add a new dimension to filter
        names.append('VIIRS_mn_uni'+str(w))
        
        #Variance filter
        filter_sq=uniform_filter(data[viirs_loc_in_list]**2,size=w, mode='constant',cval=0)
        filter_var=filter_sq - filter_u**2
        data=np.concatenate((data,filter_var[None,:, :,]), axis=0) #Need to add a new dimension to filter
        names.append('VIIRS_mn_var'+str(w))      
        
    return data,names

def add_dmsp_data(data,names,dmsp_f,year):
    dmsp_o=rasterio.open(dmsp_f.format(y=year))  
    dmsp_a=dmsp_o.read(1) 
    data=np.concatenate((data,dmsp_a[None,:, :,]), axis=0)
    names.append('DMSP')
      
    return data,names

def add_xy_data(data,names,prf):  
    grid=np.stack((np.meshgrid(np.arange(prf['width']), np.arange(prf['height'])))) #add a grid of coordinates
    data=np.concatenate((data,grid),axis=0) 
    names.append('x')
    names.append('y')
    
    return data,names

def data_to_frame(stacked,col_names):
    columns=np.transpose(np.reshape(stacked,(len(col_names),-1)))
    df=pandas.DataFrame(columns, columns=col_names)
    df=df[(df['mask']==0)]  #exclude gas and Africa masked areas    
    df=df.drop(['mask'], axis=1)
    return df

def open_etr_train_data(dmsp_f,viirs_f,afr_gas,afr_bff,afr_rgn,jdir,year,prf):
    stacked_inputs,stacked_names=open_viirs_data(viirs_f,afr_gas,afr_bff,afr_rgn,jdir,year,prf)  #open VIIRS data
    stacked_inputs,stacked_names=add_uni_filters(stacked_inputs,stacked_names) #add spatial filters
    stacked_inputs,stacked_names=add_dmsp_data(stacked_inputs,stacked_names,dmsp_f,year) #add DMSP
    
    df=data_to_frame(stacked_inputs,stacked_names)
    np.random.seed(0) ; df=df[(np.random.rand(len(df)) < 0.1)] #sample just 10% of the data (otherwise takes a long time to run)
    del stacked_inputs,stacked_names
    
    for c in df.columns: #Make sure there are no missings
        if df[c].isna().sum()!=0:
            raise NameError('Missing data for column '+c+'!')
    df=pandas.get_dummies(df,columns=['Africa Regions'])
    
    return df


def open_etr_prdct_data(viirs_f,afr_gas,afr_bff,afr_rgn,jdir,year,prf):
    stacked_inputs,stacked_names=open_viirs_data(viirs_f,afr_gas,afr_bff,afr_rgn,jdir,year,prf)  #open VIIRS data
    stacked_inputs,stacked_names=add_uni_filters(stacked_inputs,stacked_names) #add spatial filters
    stacked_inputs,stacked_names=add_xy_data(stacked_inputs,stacked_names,prf) #Add x,y to identify each cell
    
    df=data_to_frame(stacked_inputs,stacked_names)
    del stacked_inputs,stacked_names
    
    for c in df.columns: #Make sure there are no missings
        if df[c].isna().sum()!=0:
            raise NameError('Missing data for column '+c+'!')
    df=pandas.get_dummies(df,columns=['Africa Regions'])
    
    return df

def save_to_file(in_a,out_f,prf):
    with rasterio.open(out_f, 'w', **prf) as dst:
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
        new_prf['dtype']=rasterio.uint8
    if is_topcoded==0:
        dmsp_hat=dmsp_hat.astype(np.int32) #store as 32bit integer for topcoding
        new_prf['dtype']=rasterio.int32
    save_to_file(dmsp_hat,fn,new_prf)   


def train_ETR(df,importance_csv):
    #Best parameters from a random grid search with 1% of sample, 10 iterations, 3 crossfolds
    best_params={'n_estimators': 150, 'min_samples_split': 16, 'min_samples_leaf': 4, 
                 'max_features': 'sqrt', 'max_depth': 110, 'bootstrap': True}
    
    # fit the best ETR model
    Best_ETR=ExtraTreesRegressor(**best_params)
    Best_ETR.fit(df.drop(['DMSP'],axis=1),df['DMSP'])
     
    # Save feature importances save to csv
    if importance_csv!=None:
        importances=pandas.DataFrame()
        importances['feature']=df.drop(['DMSP'],axis=1).columns
        importances['ETR']=pandas.Series(Best_ETR.feature_importances_)
        importances=importances.sort_values(by=['ETR'],ascending=False)
        importances.to_csv(importance_csv)
    
    return Best_ETR

def etr_predict_save(Best_ETR,is_topcoded,out_f,viirs_f,afr_gas,afr_bff,afr_rgn,jdir,year,prf):
    #a) open contemporaneous VIIRS, apply model.
    prdct_df=open_etr_prdct_data(viirs_f,afr_gas,afr_bff,afr_rgn,jdir,year,prf)
    #b) apply prediction
    prdct_df['dmsp_hat']=Best_ETR.predict(prdct_df.drop(['x','y'], axis=1))
    #c)save to file
    write_predictions_to_raster(df=prdct_df[['x','y','dmsp_hat']],
                        prf=prf,
                        is_topcoded=is_topcoded,
                        fn=out_f.format(y=year))

def main(dmsp_f,viirs_f,afr_gas,afr_bff,afr_rgn,jdir,val_f,afr_prf):
    ifn=dmsp_f.rsplit('/', 1)[-1]
    print("Downgrading VIIRS based on "+ifn)
    start_time=time.time()
    
    #1) Open training data (random sample of 2013) 
    train_df=open_etr_train_data(dmsp_f,viirs_f,afr_gas,afr_bff,afr_rgn,jdir,year='2013',prf=afr_prf)
    is_topcoded=(train_df['DMSP'].max()<64) #record whether data is topcoded or not
    
    #2) Train ETR on DMSP in 2013
    Best_ETR=train_ETR(train_df,importance_csv=home+"/figures/importances_ETR_"+ifn[:-4].format(y=2013)+".csv")
    del train_df
    print('Setup time: '+time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time)))
    

    #3) Predict using Best ETR for all years 2014-2020 (open data, predict DMSP, save predictions to file)
    for y in range(2014,2020+1):
        print("Downgrading VIIRS in "+str(y))
        start_time=time.time()
        etr_predict_save(Best_ETR,is_topcoded,dmsp_f,viirs_f,afr_gas,afr_bff,afr_rgn,jdir,year=str(y),prf=afr_prf)
        print('Predict time: '+time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time)))
        
    #EXTRAS for validation----
    #x) Add for validation (predict 2012 with 2013)
    suffix=dmsp_f.split('_')[-1]
    suffix=suffix.split('.')[0]
    print("Adding extras for validation of "+suffix)
    out_f=val_f.format(y='2012',c=suffix)
    etr_predict_save(Best_ETR,is_topcoded,out_f,viirs_f,afr_gas,afr_bff,afr_rgn,jdir,year='2012',prf=afr_prf)
    
    #y) Add for validation (predict 2013 with 2012)
    print("Adding extras for validation of 2013 "+suffix)
    #y1) Open training data (random sample of 2012) 
    train_df=open_etr_train_data(dmsp_f,viirs_f,afr_gas,afr_bff,afr_rgn,jdir,year='2012',prf=afr_prf)
    is_topcoded=(train_df['DMSP'].max()<64) #record whether data is topcoded or not
    
    #y2) Train ETR on DMSP in 2012
    Best_ETR=train_ETR(train_df,importance_csv=None)
    del train_df
    
    #y3) Predict using Best ETR fo2 2013
    out_f=val_f.format(y='2013',c=suffix)
    etr_predict_save(Best_ETR,is_topcoded,out_f,viirs_f,afr_gas,afr_bff,afr_rgn,jdir,year='2013',prf=afr_prf)


#Settings----------------------------------------------------------------------

mchn="C:/Users/tregan/Dropbox/My PC (4TQDB63)/Desktop/LBS/data/" #Machine
home=mchn+"/code/setup_night_lights/" #location of code
sdir=mchn+"/source/" #location of source data
gdir=mchn+"/gen/night_lights/" #location of generated data
jdir=gdir+"/__junk/" #location to store temporary junk data


#inputs
#dmsp_f=gdir+"/clean_dmsp/DMSP{y}_cln.tif"
#dmsp_f=gdir+"/bloom_fix/DMSP{y}_blfix.tif"
#dmsp_f=gdir+"/bloomtopcode_fix/DMSP{y}_bltcfix.tif"
#dmsp_f=gdir+"/topcode_fix/DMSP{y}_tcfix.tif"
viirs_f=gdir+"/clean_viirs/VIIRS{y}_cln.tif"
afr_bff=gdir+"/Africa_buffered.tif"
afr_gas=gdir+"/Africa_gasmask.tif"
afr_rgn=gdir+"/Africa_regions.tif"

#outputs (to later years of dmsp_f)
val_f=gdir+"/downgrade_viirs_validation/DMSPhat{y}{c}_ETR.tif"

#standard settings for Africa rasters
afr_prf={'driver': 'GTiff', 'dtype': 'uint8', 'nodata': None, 
         'width': 9180, 'height': 8730, 'count': 1, 'crs': rasterio.crs.CRS.from_epsg(4326), 
         'transform': rasterio.Affine(0.0083333333, 0.0, -18.5, 0.0, -0.0083333333, 37.75), 
         'tiled': False, 'interleave': 'band','compress': 'lzw'}



    
#SCRIPT------------------------------------------------------------------------
# execute only if run as a script
if __name__ == "__main__":
    main(dmsp_f,viirs_f,afr_gas,afr_bff,afr_rgn,jdir,val_f,afr_prf)
     
#END---------------------------------------------------------------------------


        

