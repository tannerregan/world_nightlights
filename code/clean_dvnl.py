#Take world DMSP image, crop to Arica, apply buffered mask, apply gas mask, and save
import rasterio as rio
import numpy as np
import os
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
    """Main function to process DMSP images: crops, applies masks, and saves cleaned images.
    
    Args:
        dmsp_ols_d (str): Directory containing the DMSP data files.
        jdir (str): Directory for storing temporary files during processing.
        aoi_bff (str): Path to the buffered region raster file.
        aoi_gas (str): Path to the gas mask raster file.
        cln_f (str): Format string for the path where the cleaned images will be saved, includes placeholders for the year.

    Workflow:
        1. Opens the profile of the AOI buffered regions.
        2. Iterates over all DMSP files in the directory.
        3. For each file, extracts the year from the filename.
        4. Opens and crops DMSP and mask rasters to the AOI extent.
        5. Checks that the shapes of all arrays match.
        6. Applies masks to the DMSP data and saves the cleaned image.
    """
    prf=open_profile(aoi_bff)
    for zf in os.listdir(dmsp_ols_d):
        
        year=zf[len("DVNL_"):len("DVNL_")+4]
        dmsp_f=dmsp_ols_d+zf
        
        dmsp_a,bff_a,gas_a=open_rasters(dmsp_f,aoi_bff,aoi_gas) #open the rasters on an AOI window, output arrays
        check_shape(dmsp_a,bff_a,gas_a,dmsp_f) #check all shapes are the same
        apply_masks(dmsp_a,bff_a,gas_a,cln_f.format(y=year),prf) #Mask with AOI land and gasmask, save to file


#SCRIPT------------------------------------------------------------------------
if __name__ == "__main__":
    # execute only if run as a script
    main(dvnl_d,jdir,aoi_bff,aoi_gas,cln_f)
 
#END---------------------------------------------------------------------------