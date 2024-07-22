#Do topcoding corrections on a DMSP image following the procedure of Bluhm and Krause 2020
#imports-----------------------------------------------------------------------
import rasterio as rio
import numpy as np
import pandas as pd
import os, tarfile, gzip, shutil
from rasterio.windows import from_bounds
from rasterio.enums import Resampling


#Functions---------------------------------------------------------------------
def open_profile(aoi_f):
    """Opens a raster file and retrieves its profile, including metadata about the raster format and layout.
    
    Args:
        aoi_f (str): Path to the raster file.

    Returns:
        dict: The profile (metadata) of the raster file.
    """
    with rio.open(aoi_f) as aoi_o:
        profile = aoi_o.profile
    return profile

def clear_junk(d):
    """Clears and recreates a directory to ensure it is empty before use.
    
    Args:
        d (str): Path to the directory to be cleared.
    """
    shutil.rmtree(d, ignore_errors=True) #clear directory
    os.mkdir(d) #make empty directory
    
def check_data_match(dmsp_a,rc_a,dmsp_o,rc_o,dmsp_f):
    """Checks if DMSP and RC data arrays are compatible in terms of shape, bounds, and coordinate reference systems (CRS).
    
    Args:
        dmsp_a (np.array): DMSP data array.
        rc_a (np.array): Reference city (RC) data array.
        dmsp_o (rio.DatasetReader): DMSP raster object.
        rc_o (rio.DatasetReader): RC raster object.
        dmsp_f (str): Filename, used for error messaging.

    Raises:
        NameError: If data arrays or rasters do not match as expected.
    """
    if not dmsp_a.shape==rc_a.shape:
        raise NameError('Arrays of differing shapes, fix '+dmsp_f)
    if not dmsp_o.bounds==rc_o.bounds:
        raise NameError('Rasters have differing bounds, fix '+dmsp_f)
    if not dmsp_o.crs==rc_o.crs:
        raise NameError('Rasters have differing CRS, fix '+dmsp_f)
       
def unzip_tar(in_f,out_d):
    """Extracts all contents of a tar file into a specified directory.
    
    Args:
        in_f (str): Path to the input tar file.
        out_d (str): Directory where contents will be extracted.
    """
    tar_o = tarfile.open(in_f)
    tar_o.extractall(out_d)
    tar_o.close()
    
def unzip_gz(src_d,in_f,out_d):
    """Unzips a gzip file from a source directory to an output directory.
    
    Args:
        src_d (str): Directory containing the gzip file.
        in_f (str): Input filename without the .gz extension.
        out_d (str): Output directory where the file will be decompressed.
    """
    with gzip.open(src_d+in_f+".gz", 'rb') as f_o:
        with open(out_d+in_f, 'wb') as f_out:
            shutil.copyfileobj(f_o, f_out)
    
def unzip_rc_viirs(year,rc_d,viirs_d,out_d):
    """Unzips and processes radiance data for Radiance City (RC) and VIIRS datasets based on the year.
    
    Args:
        year (str): Year of the dataset, used to determine file naming conventions.
        rc_d (str): Directory containing the RC data files.
        viirs_d (str): Directory containing the VIIRS data files.
        out_d (str): Output directory for the unzipped files.
    
    Returns:
        str: Filename of the processed image.
    """
    if int(year)<=2011:
        if int(year)<=1997:
            n="F12_19960316-19970212"
        if 1998<=int(year)<=1999:
            n="F12_19990119-19991211"
        if 2000<=int(year)<=2001:
            n="F12-F15_20000103-20001229"
        if 2002<=int(year)<=2003:
            n="F14-F15_20021230-20031127"
        if 2004<=int(year)<=2004:
            n="F14_20040118-20041216"
        if 2005<=int(year)<=2008:
            n="F16_20051128-20061224"
        if 2009<=int(year)<=2011:
            n="F16_20100111-20101209"  
        unzip_tar(rc_d+n+"_rad_v4.geotiff.tgz",out_d)
        img_f=out_d+n+"_rad_v4.avg_vis.tif"
    if int(year)>=2012:
        fn='VNL_v21_npp_2013_global_vcmcfg_c202205302300.average_masked.dat.tif'
        unzip_gz(viirs_d,fn,out_d)
        img_f=out_d+fn
    return img_f        

def crop(img_o,rc_f,aoi_prf):
    """Crops an image based on the provided profile's bounds.
    
    Args:
        img_f (str): Path to the image file that needs to be cropped.
        prf (dict): Profile which includes metadata such as bounds to guide the cropping.

    Returns:
        np.array: Cropped image array.
    """
    ul=aoi_prf['transform'] * (0, 0)
    lr=aoi_prf['transform'] * (aoi_prf['width'], aoi_prf['height'])
    l,b,r,t=ul[0],lr[1],lr[0],ul[1]
    img_a=img_o.read(1, window=from_bounds(l,b,r,t, img_o.transform)) #crop to AOI extent
    new_prf=aoi_prf.copy()
    new_prf['dtype']=img_o.profile['dtype']
    with rio.open(rc_f, 'w', **new_prf) as dst:
        dst.write(img_a, 1)
      
def crop_resample(img_o,rc_f,aoi_prf): 
    """Crops and resamples an image to a new shape based on provided profile.
    
    Args:
        img_f (str): Path to the image file.
        prf (dict): Profile with original metadata.
        new_shape (tuple): New dimensions to which the image should be resampled.

    Returns:
        np.array: Cropped and resampled image array.
    """
    rf = img_o.transform[0]/aoi_prf['transform'][0] # resample factor: Downsample resolution to match AOI grid
    ul=aoi_prf['transform'] * (0, 0)
    lr=aoi_prf['transform'] * (aoi_prf['width'], aoi_prf['height'])
    l,b,r,t=ul[0],lr[1],lr[0],ul[1]
    w=from_bounds(l,b,r,t, img_o.transform)
    os=(1,int(w.height*rf),int(w.width*rf)) #out shape
    img_a = img_o.read(out_shape=os, resampling=Resampling.average, window=w)
    img_a=img_a.reshape(img_a.shape[1],img_a.shape[2])
    #pyplot.imshow(img_a, cmap='pink')
    new_prf=aoi_prf.copy()
    new_prf['dtype']=img_o.profile['dtype']
    with rio.open(rc_f, 'w', **new_prf) as dst:
        dst.write(img_a, 1)


def clean_rc_viirs(img_f,rc_f,aoi_prf):
    """Cleans and aligns RC and VIIRS data to be used in further analysis.
    
    Args:
        img_f (str): Path to the VIIRS image file.
        rc_f (str): Path to the RC image file.
        aoi_prf (dict): Area of interest profile used for alignment.

    Processes:
        - Opens the VIIRS image and the RC image.
        - Applies necessary transformations to align both images according to the AOI profile.
        - Cleans and processes the images for further comparative analysis or corrections.
    """
    with rio.open(img_f) as img_o:
        #crop images that DO NOT need a resample
        if img_o.transform[0]==aoi_prf['transform'][0]: 
            crop(img_o,rc_f,aoi_prf)
        #crop AND resample images that need it
        if img_o.transform[0]!=aoi_prf['transform'][0]: 
            crop_resample(img_o,rc_f,aoi_prf)


def open_rasters(dmsp_f,rc_f,aoi_prf):
    """Opens and stacks the DMSP and RC raster files for processing.
    
    Args:
        dmsp_f (str): Path to the DMSP raster file.
        rc_f (str): Path to the RC raster file.
        aoi_prf (dict): Profile containing metadata for the rasters.

    Returns:
        tuple: A tuple of numpy arrays containing the data from the DMSP and RC rasters.
    """
    with rio.open(dmsp_f) as dmsp_o, rio.open(rc_f) as rc_o:
        dmsp_a=dmsp_o.read()
        rc_a=rc_o.read()
        check_data_match(dmsp_a,rc_a,dmsp_o,rc_o,dmsp_f) #ensure same shape, same projection, same bounds        
        stacked=np.concatenate((dmsp_a,rc_a),axis=0) #stack the arrays
        grid=np.stack((np.meshgrid(np.arange(dmsp_o.width), np.arange(dmsp_o.height)))) #add a grid of coordinates, same size as input raster
        stacked=np.concatenate((dmsp_a,rc_a,grid),axis=0) 
    return stacked

def rank_tc(stacked):
    """Ranks topcoded pixels from the stacked DMSP and RC data for further processing.
    
    Args:
        stacked (tuple): Tuple containing arrays of DMSP and RC data.

    Returns:
        pd.DataFrame: DataFrame containing ranked topcoded pixels and associated data.
    """
    tc_pix=stacked[:,(55 <= stacked[0,:,:])].transpose() #get all (dmsp,rc,x,y) pairs where there is topcoding
    rank = np.lexsort((tc_pix[:,1],tc_pix[:,0])) #create a rank by RC first, and then if RC ties by DMSP
    df = pd.DataFrame(tc_pix[rank], columns=['DMSP','RC', 'x','y']) #rank is taken as the index
    return df

def break_ties(df):
    """Breaks ties in rankings for topcoded pixels, replacing ties with their average rank.
    
    Args:
        df (pd.DataFrame): DataFrame containing ranked topcoded pixels and associated data.

    Returns:
        pd.DataFrame: DataFrame with ties in ranking resolved.
    """
    df['rank'] = df.index
    df['rank'] =df.groupby(['DMSP','RC'])['rank'].transform('mean') #take mean ranks where DMSP and RC are still tied
    #divide rank by max to get percentile
    df['rank']=df['rank'].div(df['rank'].max()) 
    return df

def inverse_pareto(df):
    """Uses the inverse truncated Pareto distribution to impute Digital Number (DN) values for topcoded pixels.
    
    Args:
        df (pd.DataFrame): DataFrame containing ranked topcoded pixels and associated data.

    Returns:
        pd.DataFrame: DataFrame with imputed DN values for topcoded pixels.
    """
    alpha=1.5
    L=55
    H=2000
    df['rank']=(L/(1-df['rank']*(1-(L/H)**alpha))**(1/alpha)) 
    df=df.drop(columns=['DMSP','RC']) #drop DMSP and RC
    return df

def fill_tc_with_fix(df,dmsp_a):
    """Fills topcoded pixels in the DMSP array with the imputed fixed values.
    
    Args:
        df (pd.DataFrame): DataFrame containing the imputed DN values for topcoded pixels.
        dmsp_a (np.array): Original DMSP data array.

    Returns:
        np.array: DMSP array with topcoded pixels replaced by the imputed values.
    """
    tc_pix_fix=df.to_numpy()
    fix_a = 0 * np.empty(dmsp_a.shape)
    fix_a[tc_pix_fix.transpose()[1].astype(int), tc_pix_fix.transpose()[0].astype(int)] = tc_pix_fix.transpose()[2]
    dmsp_a_fix=np.where(dmsp_a>=55, fix_a, dmsp_a) #replace topcoded cells with theoretical values based on pareto
    dmsp_a_fix=np.around(dmsp_a_fix, decimals=0) #round to integer
    dmsp_a_fix=dmsp_a_fix.astype(int) #set as type integer
    return dmsp_a_fix

def save_to_file(dmsp_a_fix,tcfx,aoi_prf):
    """Saves the corrected DMSP data to a file.
    
    Args:
        dmsp_a_fix (np.array): Corrected DMSP data array.
        tcfx (str): Filename where the data will be saved.
        aoi_prf (dict): Raster profile to use for the output file.
    """
    new_prf=aoi_prf.copy()
    new_prf['dtype']=rio.int32
    with rio.open(tcfx, 'w', **new_prf) as dst:
            dst.write(dmsp_a_fix.astype(rio.int32),1)  

def main(dmsp_d,rc_d,viirs_d,junk_d,tcfx_f):
    """Main function to execute the topcoding correction workflow for DMSP satellite images.
    
    Args:
        dmsp_d (str): Directory containing the DMSP data files.
        rc_d (str): Directory containing the Radiance Calibrated (RC) data files.
        viirs_d (str): Directory containing the VIIRS data files.
        junk_d (str): Temporary directory used for storing intermediate files during processing.
        tcfx_f (str): Format string for the path where the corrected images will be saved, including placeholders for the year.

    Workflow:
        1. Clears the temporary directory to prepare for new processing tasks.
        2. Iterates over all DMSP files in the directory.
        3. For each file, determines the corresponding year and selects the appropriate RC and VIIRS data based on the year.
        4. Unzips and prepares RC and VIIRS data for comparison and correction.
        5. Performs topcoding correction by comparing DMSP data with reference city (RC) data to adjust over-saturated pixel values.
        6. Saves the corrected images to the specified output directory using the provided format string for filenames.
    """
    # Iterate through each DMSP file in the directory
    dmsp_lst=[f for f in os.listdir(dmsp_d) if f.startswith("DMSP")]
      
    for dmsp_f in dmsp_lst:
        aoi_prf=open_profile(dmsp_d+dmsp_f)
        print("Topcode correction for "+dmsp_f[:len("DMSP")+4])
        clear_junk(junk_d)
        year=dmsp_f[len("DMSP"):len("DMSP")+4]
        rc_f=junk_d+"/RCVIIRS{y}_cln.tif".format(y=year)
        if int(year)<=2013: #double check that the year is right
            #unzip, crop, and resample RC and VIIRS
            img_f=unzip_rc_viirs(year,rc_d,viirs_d,junk_d)
            
            #crop and resample RC and VIIRS
            clean_rc_viirs(img_f,rc_f,aoi_prf)
            
            #0. Open and stack the rasters
            stacked=open_rasters(dmsp_d+dmsp_f,rc_f,aoi_prf)
            
            #1a. get  topcoded pixels, rank them, and add to pandas dataframe
            df=rank_tc(stacked)
            
            #1b. If both RC and DMSP are tied, then replace rank with the average for this pair
            df=break_ties(df)
        
            #2. use inverse truncated pareto to impute DN numbers
            df=inverse_pareto(df)
        
            #3. fill topcoded pixels with fixed values
            dmsp_a_fix=fill_tc_with_fix(df,stacked[0])
            
            #4. save to tiff (update profile to match range)
            save_to_file(dmsp_a_fix,tcfx_f.format(y=year),aoi_prf)
        else:
            print('year {} does not match DMSP available years'.format(int(year)))
    

#SCRIPT------------------------------------------------------------------------
if __name__ == "__main__":
    # execute only if run as a script
    main(dmsp_d,rc_d,viirs_d,jdir,tcfx_f)
     
#END---------------------------------------------------------------------------