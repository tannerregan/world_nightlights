#Take world VIIRS image, crop to Arica, apply buffered mask, apply gas mask, and save
import rasterio as rio
import numpy as np
import shutil, os, gzip, re
from rasterio.windows import from_bounds
from rasterio.enums import Resampling
from matplotlib import pyplot

#Functions---------------------------------------------------------------------
def open_profile(aoi_f):
    with rio.open(aoi_f) as aoi_o:
        profile = aoi_o.profile
    return profile

def unzip_gz(in_f,year,out_d):
    img_f=out_d+"rawVIIRS"+year+".tif"
    with gzip.open(in_f, 'rb') as f_o:
        with open(img_f, 'wb') as f_out:
            shutil.copyfileobj(f_o, f_out)
    return img_f

def crop(img_f,prf):
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
    with rio.open(aoi_bff) as bff_o, rio.open(aoi_gas) as gas_o:
        #upsample masks so they match the lower resolution of VIIRS
        os=(1,img_a.shape[0],img_a.shape[1])
        gas_a=gas_o.read(1,out_shape=os,resampling=Resampling.average)
        bff_a=bff_o.read(1,out_shape=os,resampling=Resampling.average)
    return bff_a, gas_a


def check_shape(img_a,bff_a,gas_a,img_f):
    if not img_a.shape==bff_a.shape==gas_a.shape:
        raise NameError('Arrays of of differing shapes, fix '+img_f)

def apply_masks(img_a,bff_a,gas_a,cln_f,prf):
    check_shape(img_a,bff_a,gas_a,cln_f) 
    img_a=np.where(((bff_a==1) & (gas_a==0)),img_a,0)
    new_prf=prf.copy()
    new_prf['dtype']=img_a.dtype
    with rio.open(cln_f, 'w', **new_prf) as dst:
        dst.write(img_a, 1)

def main(viirs_d,jdir,aoi_bff,aoi_gas,cln_f):
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