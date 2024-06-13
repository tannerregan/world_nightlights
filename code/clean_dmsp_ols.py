#Take world DMSP image, crop to Arica, apply buffered mask, apply gas mask, and save
import numpy as np
import os, shutil, gzip
import rasterio as rio
from rasterio.windows import from_bounds


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

def unzip_gz(in_f,year,out_d):    
    """Unzips a gzip compressed file and saves it to a specified directory.
    
    Args:
        in_f (str): Path to the input gzip file.
        year (str): Year as a string, used to name the output file.
        out_d (str): Directory where the output file will be saved.

    Returns:
        str: Path to the decompressed file.
    """
    img_f=out_d+"olsDMSP"+year+".tif"
    with gzip.open(in_f, 'rb') as f_o:
        with open(img_f, 'wb') as f_out:
            shutil.copyfileobj(f_o, f_out)
    return img_f

def open_rasters(dmsp_f,aoi_bff,aoi_gas):
    """Opens DMSP and mask raster files, crops DMSP to the Area of Interest (AOI) extent, and reads the arrays.
    
    Args:
        dmsp_f (str): Path to the DMSP raster file.
        aoi_bff (str): Path to the buffered region raster file.
        aoi_gas (str): Path to the gas mask raster file.

    Returns:
        tuple: A tuple containing arrays for DMSP, buffered mask, and gas mask.
    """
    with rio.open(dmsp_f) as dmsp_o, rio.open(aoi_bff) as bff_o, rio.open(aoi_gas) as gas_o:
        bff_a=bff_o.read(1)
        gas_a=gas_o.read(1)
        l,b,r,t=bff_o.bounds[0],bff_o.bounds[1],bff_o.bounds[2],bff_o.bounds[3]
        dmsp_a=dmsp_o.read(1, window=from_bounds(l,b,r,t, dmsp_o.transform)) #crop to AOI extent
        ##pyplot.imshow(dmsp_a, cmap='pink') #take a look to make sure it's AOI
    return dmsp_a,bff_a,gas_a

def check_shape(dmsp_a,bff_a,gas_a,dmsp_f):
    """Checks if DMSP, buffered mask, and gas mask arrays have the same shape.
    
    Args:
        dmsp_a (np.array): DMSP data array.
        bff_a (np.array): Buffered mask array.
        gas_a (np.array): Gas mask array.
        dmsp_f (str): Filename of the DMSP file, used for error messaging.

    Raises:
        NameError: If arrays do not have the same shape.
    """
    if not dmsp_a.shape==bff_a.shape==gas_a.shape:
        raise NameError('Arrays of of differing shapes, fix '+dmsp_f)

def apply_masks(dmsp_a,bff_a,gas_a,cln_f,prf):
    """Applies buffered and gas masks to the DMSP data array and saves the cleaned image.
    
    Args:
        dmsp_a (np.array): Original DMSP data array.
        bff_a (np.array): Buffered mask array.
        gas_a (np.array): Gas mask array.
        cln_f (str): Path where the cleaned image will be saved.
        prf (dict): Profile to use for saving the cleaned image.
    """
    dmsp_a=np.where(((bff_a==1) & (gas_a==0)),dmsp_a,0)
    ##pyplot.imshow(dmsp_a, cmap='pink') #take a look to make sure masks were applied

    #save to file
    with rio.open(cln_f, 'w', **prf) as dst:
        dst.write(dmsp_a, 1)

        
def main(dmsp_ols_d,jdir,aoi_bff,aoi_gas,cln_f):
    zf_lst=[f for f in os.listdir(dmsp_ols_d) if f[-len(".tif.gz"):]==".tif.gz"]
    for zf in zf_lst:
        print("working on: "+zf)
        year=zf[len("FXX"):len("FXX")+4]
        #unzip, crop
        dmsp_f=unzip_gz(dmsp_ols_d+zf,year,jdir)  
        
        #open the rasters on AOI window, output arrays
        dmsp_a,bff_a,gas_a=open_rasters(dmsp_f,aoi_bff,aoi_gas) 
        
        #check all shapes are the same
        check_shape(dmsp_a,bff_a,gas_a,dmsp_f) 
        
        #Mask with African land and gasmask, save to file
        prf=open_profile(aoi_bff)
        apply_masks(dmsp_a,bff_a,gas_a,cln_f.format(y=year),prf) 

#Settings----------------------------------------------------------------------


#SCRIPT------------------------------------------------------------------------
if __name__ == "__main__":
    # execute only if run as a script
    main(dmsp_ols_d,jdir,aoi_bff,aoi_gas,cln_f)
    
#END---------------------------------------------------------------------------