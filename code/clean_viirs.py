#Take world VIIRS image, crop to Arica, apply buffered mask, apply gas mask, and save
import rasterio as rio
import numpy as np
import shutil, os, gzip, re
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

def unzip_gz(in_f,year,out_d):    
    """Unzips a gzip compressed file and saves it to a specified directory.
    
    Args:
        in_f (str): Path to the input gzip file.
        year (str): Year as a string, used to name the output file.
        out_d (str): Directory where the output file will be saved.

    Returns:
        str: Path to the decompressed file.
    """
    img_f=out_d+"rawVIIRS"+year+".tif"
    with gzip.open(in_f, 'rb') as f_o:
        with open(img_f, 'wb') as f_out:
            shutil.copyfileobj(f_o, f_out)
    return img_f

def crop(img_f,prf):
    """Crops an image to the extent specified in the provided profile.
    
    Args:
        img_f (str): Path to the input image file.
        prf (dict): Raster profile dictating the extent to which the image should be cropped.

    Returns:
        tuple: A tuple containing the cropped image array and its new profile.
    """
    ul=prf['transform'] * (0, 0)
    lr=prf['transform'] * (prf['width'], prf['height'])
    l,b,r,t=ul[0],lr[1],lr[0],ul[1]
    with rio.open(img_f) as img_o:
        w=from_bounds(l,b,r,t, img_o.transform)
        w_transform = img_o.window_transform(w)
        img_a=img_o.read(1, window=w) #crop to AOI extent
        new_prf=prf.copy()
        new_prf['dtype']=img_a.dtype
        new_prf['height']=img_a.shape[0]
        new_prf['width']=img_a.shape[1]
        new_prf['transform']=w_transform
    return img_a, new_prf

def upsample_masks(img_a,aoi_bff,aoi_gas):
    """Upsamples masks to match the lower resolution of the VIIRS image array.
    
    Args:
        img_a (np.array): The image array to match the resolution.
        aoi_bff (str): Path to the buffered region raster file.
        aoi_gas (str): Path to the gas mask raster file.

    Returns:
        tuple: A tuple containing the upsampled buffered and gas mask arrays.
    """
    with rio.open(aoi_bff) as bff_o, rio.open(aoi_gas) as gas_o:
        #upsample masks so they match the lower resolution of VIIRS
        os=(1,img_a.shape[0],img_a.shape[1])
        gas_a=gas_o.read(1,out_shape=os,resampling=Resampling.average)
        bff_a=bff_o.read(1,out_shape=os,resampling=Resampling.average)
    return bff_a, gas_a


def check_shape(img_a,bff_a,gas_a,img_f):
    """Checks if all provided arrays have the same shape; raises an error if they do not.
    
    Args:
        img_a (np.array): Main image array.
        bff_a (np.array): Buffered mask array.
        gas_a (np.array): Gas mask array.
        img_f (str): Image file path, used in the error message.
    
    Raises:
        NameError: If arrays do not have the same shape.
    """
    if not img_a.shape==bff_a.shape==gas_a.shape:
        raise NameError('Arrays of of differing shapes, fix '+img_f)

def apply_masks(img_a,bff_a,gas_a,cln_f,prf):
    """Applies buffered and gas masks to the VIIRS image and saves the cleaned image.
    
    Args:
        img_a (np.array): Original VIIRS image array.
        bff_a (np.array): Buffered mask array.
        gas_a (np.array): Gas mask array.
        cln_f (str): Path where the cleaned image will be saved.
        prf (dict): Profile to use for saving the cleaned image.
    """
    check_shape(img_a,bff_a,gas_a,cln_f) 
    img_a=np.where(((bff_a==1) & (gas_a==0)),img_a,0)
    new_prf=prf.copy()
    new_prf['dtype']=img_a.dtype
    with rio.open(cln_f, 'w', **new_prf) as dst:
        dst.write(img_a, 1)

def main(viirs_d,jdir,aoi_bff,aoi_gas,cln_f):
    """Main function to process VIIRS data: unzips, crops, applies masks, and saves cleaned images.
    
    Args:
        viirs_d (str): Directory containing the VIIRS data files.
        jdir (str): Directory for storing temporary files during processing.
        aoi_bff (str): Path to the raster file of the buffered regions.
        aoi_gas (str): Path to the raster file of the gas mask.
        cln_f (str): Format string for the path where the cleaned images will be saved, includes placeholders for the year.

    Workflow:
        1. Retrieves the profile from the buffered regions file to use as a reference for cropping.
        2. Iterates over all VIIRS .tif.gz files in the provided directory.
        3. For each file, unzips and crops the image to the Area of Interest (AOI).
        4. Upsamples the buffered and gas masks to match the VIIRS image resolution.
        5. Applies these masks to the VIIRS image to filter out unwanted data.
        6. Saves the cleaned and masked image to the designated output path.
    """
    prf=open_profile(aoi_bff)
    zf_lst=[f for f in os.listdir(viirs_d) if f.endswith(".tif.gz")]
    for zf in zf_lst:
        year=re.search(r'\d{4}', zf).group()
        #unzip, crop, and resample VIIRS
        img_f=unzip_gz(viirs_d+zf,year,jdir)  
        
        #crop VIIRS to AOI
        img_a,crop_prf=crop(img_f,prf)  
        
        #open upsampled masks
        bff_a,gas_a=upsample_masks(img_a, aoi_bff,aoi_gas)
        
        #mask VIIRS and save
        apply_masks(img_a,bff_a,gas_a,cln_f.format(y=year),crop_prf)

    

#SCRIPT------------------------------------------------------------------------
if __name__ == "__main__":
    # execute only if run as a script
    main(viirs_d,jdir,aoi_bff,aoi_gas,cln_f)
 
#END---------------------------------------------------------------------------