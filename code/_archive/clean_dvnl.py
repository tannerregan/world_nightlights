#Take world DMSP image, crop to Arica, apply buffered mask, apply gas mask, and save
import rasterio as rio
import numpy as np
import os, json
from rasterio.windows import from_bounds


#Functions---------------------------------------------------------------------
def open_profile(out_prf):
    with open(out_prf, 'r') as file:
        profile = json.load(file)
    return profile

def open_rasters(dmsp_f,aoi_bff,aoi_gas):
    with rio.open(dmsp_f) as dmsp_o, rio.open(aoi_bff) as bff_o, rio.open(aoi_gas) as gas_o:
        bff_a=bff_o.read(1)
        gas_a=gas_o.read(1)
        l,b,r,t=bff_o.bounds[0],bff_o.bounds[1],bff_o.bounds[2],bff_o.bounds[3]
        dmsp_a=dmsp_o.read(1, window=from_bounds(l,b,r,t, dmsp_o.transform)) #crop to AOI extent
        ##pyplot.imshow(dmsp_a, cmap='pink') #take a look to make sure it's AOI
    return dmsp_a,bff_a,gas_a

def check_shape(dmsp_a,bff_a,gas_a,dmsp_f):
    if not dmsp_a.shape==bff_a.shape==gas_a.shape:
        raise NameError('Arrays of of differing shapes, fix '+dmsp_f)
        
def apply_masks(dmsp_a,bff_a,gas_a,cln_f,aoi_prf):
    prf=open_profile(aoi_prf)
    dmsp_a=np.where(((bff_a==1) & (gas_a==0)),dmsp_a,0)
    ##pyplot.imshow(dmsp_a, cmap='pink') #take a look to make sure masks were applied

    #save to file
    with rio.open(cln_f, 'w', **prf) as dst:
        dst.write(dmsp_a, 1)


def main(dmsp_ols_d,jdir,aoi_bff,aoi_gas,cln_f,aoi_prf):
    for zf in os.listdir(dmsp_ols_d):
        
        year=zf[len("DVNL_"):len("DVNL_")+4]
        dmsp_f=dmsp_ols_d+zf
        
        dmsp_a,bff_a,gas_a=open_rasters(dmsp_f,aoi_bff,aoi_gas) #open the rasters on an AOI window, output arrays
        check_shape(dmsp_a,bff_a,gas_a,dmsp_f) #check all shapes are the same
        apply_masks(dmsp_a,bff_a,gas_a,cln_f.format(y=year),aoi_prf) #Mask with AOI land and gasmask, save to file


#SCRIPT------------------------------------------------------------------------
if __name__ == "__main__":
    # execute only if run as a script
    main(dvnl_d,jdir,aoi_bff,aoi_gas,cln_f,aoi_prf)
 
#END---------------------------------------------------------------------------