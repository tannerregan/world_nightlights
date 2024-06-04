#Take world DMSP image, crop to Arica, apply buffered mask, apply gas mask, and save
import rasterio as rio
import numpy as np
import zipfile
from rasterio.windows import from_bounds


#Functions---------------------------------------------------------------------
def open_profile(aoi_f):
    with rio.open(aoi_f) as aoi_o:
        profile = aoi_o.profile
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
        
def apply_masks(dmsp_a,bff_a,gas_a,cln_f,prf):
    dmsp_a=np.where(((bff_a==1) & (gas_a==0)),dmsp_a,0)
    ##pyplot.imshow(dmsp_a, cmap='pink') #take a look to make sure masks were applied

    #save to file
    with rio.open(cln_f, 'w', **prf) as dst:
        dst.write(dmsp_a, 1)

def main(dmsp_viirs_zip,jdir,aoi_bff,aoi_gas,cln_f,sim_cln_f):
    prf=open_profile(aoi_bff)
    with zipfile.ZipFile(dmsp_viirs_zip, 'r') as zip_ref:    
        zip_lst=[zf for zf in zip_ref.namelist() if zf.startswith("Harmonized_DN_NTL_") & zf.endswith(".tif")]
        for zf in zip_lst:
            year=zf[len("Harmonized_DN_NTL_"):len("Harmonized_DN_NTL_")+4]
            if int(year)<=2013: #we only want the DMSP data (not the predicted DMSP)
                zip_ref.extract(zf, jdir)
                dmsp_f=jdir+zf
                dmsp_a,bff_a,gas_a=open_rasters(dmsp_f,aoi_bff,aoi_gas) #open the rasters on an AOI window, output arrays
                check_shape(dmsp_a,bff_a,gas_a,dmsp_f) #check all shapes are the same
                apply_masks(dmsp_a,bff_a,gas_a,cln_f.format(y=year),prf) #Mask with AOI land and gasmask, save to file
                
        #also open the extra DMSP 'similar' in 2013 where VIIRS and DMSP overlap - this is used in validation of VIIRS downgrading
        zip_lst=[zf for zf in zip_ref.namelist() if zf.startswith("DN_NTL_") & zf.endswith(".tif")]
        for zf in zip_lst:
            year=zf[len("DN_NTL_"):len("DN_NTL_")+4]
            zip_ref.extract(zf, jdir)
            dmsp_f=jdir+zf
            dmsp_a,bff_a,gas_a=open_rasters(dmsp_f,aoi_bff,aoi_gas) #open the rasters on an AOI window, output arrays
            check_shape(dmsp_a,bff_a,gas_a,dmsp_f) #check all shapes are the same
            apply_masks(dmsp_a,bff_a,gas_a,sim_cln_f.format(y=year+'sim'),prf) #Mask with AOI land and gasmask, save to file

#SCRIPT------------------------------------------------------------------------
if __name__ == "__main__":
    # execute only if run as a script
    main(dmsp_viirs_zip,jdir,aoi_bff,aoi_gas,cln_f,sim_cln_f)
 
#END---------------------------------------------------------------------------