#Make global gas flare mask, make 'ubergrid' raster of AOI regions, make buffered regions
import pandas as pd
import geopandas as gpd
import rasterio as rio
import os, shutil, tarfile, math, json
from rasterio import features
from rasterio.transform import from_origin
from matplotlib import pyplot

#Functions---------------------------------------------------------------------
def select_aoi(in_f):
    gdf=gpd.read_file(in_f)
    gdf=gdf[(gdf['REGION']!='Antarctica')]
    return gdf

def create_aoi_profile(in_gdf, out_prf):
    # Get the bounding box (spatial extent) of the GeoDataFrame
    bbox = in_gdf.total_bounds  # Returns (minx, miny, maxx, maxy)
    #reduce the northern/southern limits so inside the DMSP range (below 75 degrees north, above -65 degrees south)
    if bbox[3]>75:
        bbox[3]=75
    if bbox[1]<-65:
        bbox[1]=-65
    #set east and west bounds
    bbox[0],bbox[2]=-180,180
    # Specify the desired resolution in the units of your CRS
    res = 0.0083333333  # Set the resolution in decimal degrees to match DMSP
    # Calculate the width and height based on the resolution
    width = math.ceil((bbox[2] - bbox[0]) / res)
    height = math.ceil((bbox[3] - bbox[1]) / res)
    # Create the transform for the new raster profile
    transform = from_origin(bbox[0], bbox[3], res, res)
    # Create a dictionary containing the raster profile parameters
    profile = {
        'driver': 'GTiff',
        'dtype': 'uint8',
        'width': width,
        'height': height,
        'count': 1,
        'crs': 'EPSG:4326',
        'transform': transform,
        'nodata': None,
        'tiled': False,
        'interleave': 'band',
        'compress': 'lzw'
    }
    # Write the dictionary to the file in JSON format
    with open(out_prf, 'w') as file:
        json.dump(profile, file, indent=4)  # indent parameter adds pretty formatting

def open_profile(out_prf):
    with open(out_prf, 'r') as file:
        profile = json.load(file)
    return profile

def geodf2raster(in_gdf,out_f,in_prf):
    prf=open_profile(in_prf)
    with rio.open(out_f, 'w+', **prf) as out:
        out_arr = out.read(1)  
        shapes = ((geom,value) for geom, value in zip(in_gdf.geometry, in_gdf.OBJECTID)) # this is where we create a generator of geom, value pairs to use in rasterizing
        burned = features.rasterize(shapes=shapes, fill=0, out=out_arr, transform=out.transform)
        ##pyplot.imshow(burned, cmap='pink') #check the map
        out.write_band(1, burned)

def unzip_tars(in_d,out_d):
    #unzip all tars in a directory to an output directory
    for tar_f in os.listdir(in_d): 
        tar_o = tarfile.open(in_d+tar_f)
        tar_o.extractall(out_d)
        tar_o.close()

def append_shapefiles(in_d,shp_lst):
    jnd_gdf=gpd.read_file(in_d+shp_lst[0]) #append all shapefiles
    crs=jnd_gdf.crs
    for shp in shp_lst[1:]:
        gdf=gpd.read_file(in_d+shp)
        if crs!=gdf.crs:
            print("no crs match on "+shp)
        jnd_gdf = pd.concat([jnd_gdf,gdf],ignore_index=True)
    return jnd_gdf
        
def make_aoi_regions(in_f,out_f,prf_f):
    gdf=select_aoi(in_f)
    create_aoi_profile(gdf, prf_f)
    ##gdf.plot();
    geodf2raster(gdf,out_f,prf_f)
    
def make_aoi_buffer(in_f,out_f,prf_f):  
    gdf=select_aoi(in_f)
    gdf['OBJECTID']=1
    bff=gdf[['geometry','OBJECTID']].dissolve(by='OBJECTID').buffer(0.066) #Dissolve all countries, and buffer by 0.066 (approx. 7.5km) to get coast line
    ##bff.plot(); #check boundaries are buffered
    gdf=gpd.GeoDataFrame(geometry=gpd.GeoSeries(bff))
    gdf['OBJECTID']=1
    geodf2raster(gdf,out_f,prf_f)

def make_gas_mask(gasf_dir,junk_d,aoi_gas,prf_f):
    shutil.rmtree(junk_d, ignore_errors=True) #clear gas flare junk
    os.mkdir(junk_d) #make empty generated directory
    unzip_tars(gasf_dir,junk_d)
    shp_lst=[shp_f for shp_f in os.listdir(junk_d) if shp_f.endswith(".shp")] #list all shapefiles
    jnd_gdf=append_shapefiles(junk_d, shp_lst)
    ##jnd_gdf.plot(); #make sure all shapefiles are in the correct place
    jnd_gdf['OBJECTID']=1
    geodf2raster(jnd_gdf,aoi_gas,prf_f)

def main(wrld_rgn,aoi_rgn,aoi_bff, gasf_dir,gas_jdir, aoi_gas,aoi_prf):
    #Make 'ubergrid' raster of all non-antarica regions (PROFILE also gets made here)
    make_aoi_regions(wrld_rgn, aoi_rgn, aoi_prf)
     
    #Make buffered regions
    make_aoi_buffer(wrld_rgn, aoi_bff, aoi_prf)
    
    #Make global gas flare mask
    make_gas_mask(gasf_dir, gas_jdir, aoi_gas, aoi_prf)
    

#SCRIPT------------------------------------------------------------------------
if __name__ == "__main__":
    # execute only if run as a script
    main(wrld_rgn,aoi_rgn,aoi_bff, gasf_dir,gas_jdir, aoi_gas,aoi_prf)
#END---------------------------------------------------------------------------