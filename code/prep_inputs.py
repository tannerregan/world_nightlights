#Make global gas flare mask, make 'ubergrid' raster of AOI regions, make buffered regions
import pandas as pd
import geopandas as gpd
import rasterio as rio
import os, shutil, tarfile, math
from rasterio import features
from rasterio.transform import from_origin
import pyproj
from pyproj import CRS

#Functions---------------------------------------------------------------------
def select_aoi(in_f, AOI_lst):
    """Selects and returns regions specified in AOI_lst from a geospatial file.
    Args:
        in_f (str): Path to the input geospatial file.
        AOI_lst (list): List of regions to include in the output.
    
    Returns:
        gpd.GeoDataFrame: GeoDataFrame containing only the selected regions.
    """
    gdf=gpd.read_file(in_f)
    gdf=gdf[(gdf['REGION'].apply(lambda x: any([k in x for k in AOI_lst])))]
    return gdf

def create_aoi_profile(in_gdf):
    """Creates a raster profile based on the bounding box of the input GeoDataFrame.
    
    Adjusts the bounding box to stay within latitudinal limits suitable for DMSP data.
    Sets the resolution to match DMSP characteristics.
    
    Args:
        in_gdf (gpd.GeoDataFrame): Input GeoDataFrame from which to create the profile.

    Returns:
        dict: A dictionary containing the raster profile parameters.
    """
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
    return profile

def open_profile(aoi_f):
    """Opens a raster file and retrieves its profile.
    
    Args:
        aoi_f (str): Path to the raster file.

    Returns:
        dict: The profile (metadata) of the raster file.
    """
    with rio.open(aoi_f) as aoi_o:
        profile = aoi_o.profile
    return profile

def geodf2raster(in_gdf,out_f,prf):
    """Converts a GeoDataFrame to a raster using specified profile settings.
    
    Args:
        in_gdf (gpd.GeoDataFrame): GeoDataFrame to convert.
        out_f (str): Output file path for the raster.
        prf (dict): Raster profile to use for conversion.

    """
    with rio.open(out_f, 'w+', **prf) as out:
        out_arr = out.read(1)  
        shapes = ((geom,value) for geom, value in zip(in_gdf.geometry, in_gdf.OBJECTID)) # this is where we create a generator of geom, value pairs to use in rasterizing
        burned = features.rasterize(shapes=shapes, fill=0, out=out_arr, transform=out.transform)
        out.write_band(1, burned)

def unzip_tars(gasf_dir,junk_d):
    """Unzips tar files containing gas flare data into a designated junk directory.
    
    Args:
        gasf_dir (str): Directory where the tar files are stored.
        junk_d (str): Temporary directory to extract the files into.

    Note:
        This function assumes all tar files in the specified directory need to be extracted.
    """
    #unzip all tars in a directory to an output directory
    for tar_f in os.listdir(gasf_dir): 
        tar_o = tarfile.open(gasf_dir+tar_f)
        tar_o.extractall(junk_d)
        tar_o.close()

def append_shapefiles(junk_d,shp_lst):
    """Combines multiple shapefiles into a single GeoDataFrame.
    
    Args:
        junk_d (str): Directory containing the shapefiles.
        shp_lst (list): List of shapefile names to be combined.

    Returns:
        gpd.GeoDataFrame: A GeoDataFrame containing all geometries from the listed shapefiles.

    Note:
        All shapefiles are assumed to have a compatible coordinate reference system (CRS).
    """
    jnd_gdf=gpd.read_file(junk_d+shp_lst[0]) #append all shapefiles
    crs=jnd_gdf.crs
    for shp in shp_lst[1:]:
        gdf=gpd.read_file(junk_d+shp)
        if crs!=gdf.crs:
            print("no crs match on "+shp)
        jnd_gdf = pd.concat([jnd_gdf,gdf],ignore_index=True)
    return jnd_gdf

def make_aoi_regions(in_f, out_f, AOI_lst):
    """Processes input geographic file to create a raster of Areas of Interest (AOI).
    
    Args:
        in_f (str): Input file path for geographic data.
        out_f (str): Output file path for the AOI raster.
        AOI_lst (list): List of areas to include.
    """
    gdf = select_aoi(in_f, AOI_lst)
    prf = create_aoi_profile(gdf)
    geodf2raster(gdf, out_f, prf)

def make_aoi_buffer(in_f, out_f, aoi_rgn, AOI_lst):
    """Creates a buffered raster around selected areas, useful for defining boundaries.
    
    Args:
        in_f (str): Input file path for geographic data.
        out_f (str): Output file path for the buffered raster.
        aoi_rgn (str): Raster file of the AOI used to get profile data.
    """
    gdf = select_aoi(in_f,AOI_lst)
    gdf['OBJECTID'] = 1
    # Project to Eckert IV projection, buffer, and project back
    bff = gdf[['geometry', 'OBJECTID']].to_crs(crs=CRS.from_string('esri:54014')).dissolve(by='OBJECTID').buffer(7.5)
    bff = bff.to_crs(gdf.crs)  # Project back to original CRS
    gdf = gpd.GeoDataFrame(geometry=gpd.GeoSeries(bff))
    gdf['OBJECTID'] = 1
    prf = open_profile(aoi_rgn)
    geodf2raster(gdf, out_f, prf)

def make_gas_mask(gasf_dir,junk_d,aoi_gas,aoi_rgn):
    """Creates a global gas flare mask by processing shapefiles and rasterizing them.

    Args:
        gasf_dir (str): Directory containing gas flare shapefiles.
        junk_d (str): Directory for storing temporary files.
        aoi_gas (str): Output path for the gas mask raster.
        aoi_rgn (str): Raster file of the AOI to retrieve profile data.
    """
    shutil.rmtree(junk_d, ignore_errors=True) #clear gas flare junk
    os.mkdir(junk_d) #make empty generated directory
    unzip_tars(gasf_dir,junk_d)
    shp_lst=[shp_f for shp_f in os.listdir(junk_d) if shp_f.endswith(".shp")] #list all shapefiles
    jnd_gdf=append_shapefiles(junk_d, shp_lst)
    ##jnd_gdf.plot(); #make sure all shapefiles are in the correct place
    jnd_gdf['OBJECTID']=1
    prf=open_profile(aoi_rgn)
    geodf2raster(jnd_gdf,aoi_gas,prf)

def main(wrld_rgn,aoi_rgn,aoi_bff, gasf_dir,gas_jdir, aoi_gas, AOI_lst):
    """The main function orchestrates the creation of AOI rasters, buffered regions, and a global gas flare mask.

    Args:
        wrld_rgn (str): Path to the world regions geospatial file.
        aoi_rgn (str): Output file path for the AOI regions raster.
        aoi_bff (str): Output file path for the buffered AOI raster.
        gasf_dir (str): Directory containing gas flare data.
        gas_jdir (str): Temporary directory for processing junk data.
        aoi_gas (str): Output file path for the gas mask raster.
        AOI_lst (list): List of areas to include as Areas of Interest (AOI).
    
    Processes:
        1. Creates a raster of all non-Antarctica regions using `make_aoi_regions`.
        2. Creates buffered regions to define boundaries around AOIs using `make_aoi_buffer`.
        3. Creates a global gas flare mask by processing and rasterizing shapefiles using `make_gas_mask`.
    """
    #Make 'ubergrid' raster of all non-antarica regions (PROFILE also gets made here)
    make_aoi_regions(wrld_rgn, aoi_rgn, AOI_lst)
     
    #Make buffered regions
    make_aoi_buffer(wrld_rgn, aoi_bff,aoi_rgn, AOI_lst)
    
    #Make global gas flare mask
    make_gas_mask(gasf_dir, gas_jdir, aoi_gas, aoi_rgn)
    

#SCRIPT------------------------------------------------------------------------
if __name__ == "__main__":
    # execute only if run as a script
    main(wrld_rgn,aoi_rgn,aoi_bff, gasf_dir,gas_jdir, aoi_gas, AOI_lst)
#END---------------------------------------------------------------------------