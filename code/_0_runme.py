"""
This file runs all files for the Illuminating Africa dataset creation.

It is essential to:
    1. Adjust the path names here to match your local environment
    2. Select the world regions from the AOI list to match your purpose
"""
    
import os, shutil, runpy
from urllib.request import urlretrieve
import requests
import json
from google_drive_downloader import GoogleDriveDownloader as gdd

#Settings----------------------------------------------------------------------
#Directory Paths
if os.getlogin() == "username_here":
    data_dir="C:/Users/username/data_main/world_nightlights/"
    code_dir="C:/Users/username_here/Documents/GitHub/world_nightlights/code/"
    
else: raise ValueError('Path not correctly specified for this computer.')

#choose whether to re-download source data
download_from_source=True #set to false if you have already downloaded the data

#sub-directories
sdir=data_dir+"/source/" #location of source data
gdir=data_dir+"/gen/" #location of generated dat
jdir=gdir+"/__junk/" #location to store temporary junk data

#Input data paths
dmsp_viirs_zip=sdir+"/Li_etal_2021_series/DMSP_VIIRS_1992_2018.zip"
rc_d=sdir+"/DMSP_RC/"
viirs_d=sdir+"/VIIRS/"
dvnl_d=sdir+"/DVNL/"
dmsp_ols_d=sdir+"/DMSP/"
gasf_dir=sdir+"/gas_flaring/"
wrld_rgn=sdir+"/admin_boundaries/world_regions.shp"

#Input data paths
dmsp_viirs_zip=sdir+"/Li_etal_2021_series/DMSP_VIIRS_1992_2018.zip"
rc_d=sdir+"/DMSP_RC/"
viirs_d=sdir+"/VIIRS/"
dvnl_d=sdir+"/DVNL/"
gasf_dir=sdir+"/gas_flaring/"
wrld_rgn=sdir+"/admin_boundaries/world_regions.shp"

#output files
aoi_rgn=gdir+"/AOI_regions.tif"
aoi_bff=gdir+"/AOI_buffered.tif"
aoi_gas=gdir+"/AOI_gasmask.tif"
dmsp_cln=gdir+"/clean_dmsp/DMSP{y}_cln.tif"
sim_dmsp_cln=gdir+"/downgrade_viirs_validation/simDMSP{y}_cln.tif"
dvnl=gdir+"/clean_dvnl/DVNL{y}.tif"
dmsp_ols=gdir+"/clean_dmsp_ols/DMSP{y}_ols.tif"
viirs_cln=gdir+"/clean_viirs/VIIRS{y}_cln.tif"
blfx_f=gdir+"/bloom_fix/DMSP{y}_blfix.tif"
tcfx_f=gdir+"/topcode_fix/DMSP{y}_tcfix.tif"
bltcfx_f=gdir+"/bloomtopcode_fix/DMSP{y}_bltcfix.tif"
val_f=gdir+"/downgrade_viirs_validation/DMSPhat{y}{c}_ETR.tif"

#Account username and password for EOG mines account

#Note: the EOG website where you can access this data requires a login. Please substitute in your username and password below
#Create an account here: https://eogauth.mines.edu/auth/realms/master/protocol/openid-connect/auth?response_type=code&scope=email%20openid&client_id=eogdata_oidc&state=7uZNQ8KZe1LhdmXzWBel6nrA-Rg&redirect_uri=https%3A%2F%2Feogdata.mines.edu%2Feog%2Foauth2callback&nonce=k8niAQRSjvqhI5fvPYj0wTDhqwHDzy_CsmXYfRTnFV0

eog_username = "created_username@email.com"
eog_password = "created_password"


#Choose regions for your AOI
AOI=['Antarctica',
 'Asiatic Russia',
 'Australia/New Zealand',
 'Caribbean',
 'Central America',
 'Central Asia',
 'Eastern Africa',
 'Eastern Asia',
 'Eastern Europe',
 'European Russia',
 'Melanesia',
 'Micronesia',
 'Middle Africa',
 'Northern Africa',
 'Northern America',
 'Northern Europe',
 'Polynesia',
 'South America',
 'Southeastern Asia',
 'Southern Africa',
 'Southern Asia',
 'Southern Europe',
 'Western Africa',
 'Western Asia',
 'Western Europe']

"""
Main dataset for world based on all regions except Antartica. Full list of world regions below:
    AOI=['Antarctica',
     'Asiatic Russia',
     'Australia/New Zealand',
     'Caribbean',
     'Central America',
     'Central Asia',
     'Eastern Africa',
     'Eastern Asia',
     'Eastern Europe',
     'European Russia',
     'Melanesia',
     'Micronesia',
     'Middle Africa',
     'Northern Africa',
     'Northern America',
     'Northern Europe',
     'Polynesia',
     'South America',
     'Southeastern Asia',
     'Southern Africa',
     'Southern Asia',
     'Southern Europe',
     'Western Africa',
     'Western Asia',
     'Western Europe']
"""

#Functions---------------------------------------------------------------------
def clear_junk(d):
    shutil.rmtree(d, ignore_errors=True) #clear directory
    os.mkdir(d) #make empty directory

#Run scripts-------------------------------------------------------------------

#(0a) download source data
if download_from_source==True:
    #empty out the source directory
    clear_junk(sdir)

    global_vars = {"sdir": sdir, "username": eog_username, "password": eog_password}
    runpy.run_path(code_dir+'source_data_download.py', init_globals=global_vars, run_name="__main__")

#(0b) clear out directories
clear_junk(gdir)
clear_junk(jdir)
os.mkdir(gdir+"/clean_dmsp") 
os.mkdir(gdir+"/downgrade_viirs_validation")  
os.mkdir(gdir+"/clean_dvnl") 
os.mkdir(gdir+"/clean_dmsp_ols") 
os.mkdir(gdir+"/clean_viirs")
os.mkdir(gdir+"/bloom_fix")  
os.mkdir(gdir+"/topcode_fix") 
os.mkdir(gdir+"/bloomtopcode_fix") 

#(1) Make global gas flare shapefile, make 'ubergrid' raster of AOI regions, make buffered regions
global_vars = {"gasf_dir": gasf_dir, "wrld_rgn": wrld_rgn, "gas_jdir": jdir+"/gas_flares/", 
               "aoi_rgn": aoi_rgn, "aoi_bff": aoi_bff, "aoi_gas": aoi_gas, "AOI_lst": AOI}
runpy.run_path(code_dir+'prep_inputs.py', init_globals=global_vars, run_name="__main__")
clear_junk(jdir)

#(2) clean DMSP: unzip, crop to AOI, apply buffered mask, apply gas mask, and save
global_vars = {"dmsp_viirs_zip": dmsp_viirs_zip, "jdir": jdir, "aoi_bff": aoi_bff, 
               "aoi_gas": aoi_gas, "cln_f": dmsp_cln, "sim_cln_f": sim_dmsp_cln}
runpy.run_path(code_dir+'clean_dmsp.py', init_globals=global_vars, run_name="__main__")
clear_junk(jdir)

#(2b) add a clean of the DMSP-like nightlights (DVNL)
global_vars = {"dvnl_d": dvnl_d, "jdir": jdir, "aoi_bff": aoi_bff, 
               "aoi_gas": aoi_gas, "cln_f": dvnl}
runpy.run_path(code_dir+'clean_dvnl.py', init_globals=global_vars, run_name="__main__")
clear_junk(jdir)

#(2c) add a clean of the 'raw' DMSP-ols nightlights
global_vars = {"dmsp_ols_d": dmsp_ols_d, "jdir": jdir, "aoi_bff": aoi_bff, 
               "aoi_gas": aoi_gas, "cln_f": dmsp_ols}
runpy.run_path(code_dir+'clean_dmsp_ols.py', init_globals=global_vars, run_name="__main__")
clear_junk(jdir)

#(3) clean VIIRS: unzip, crop to AOI, apply buffered mask, apply gas mask, and save
global_vars = {'viirs_d':viirs_d,'jdir':jdir, "aoi_bff": aoi_bff, 
               "aoi_gas": aoi_gas, "cln_f": viirs_cln}
runpy.run_path(code_dir+'clean_viirs.py', init_globals=global_vars, run_name="__main__")
clear_junk(jdir)

#(4) blooming correction
global_vars = {"dmsp_d": gdir+"/clean_dmsp/", "blfx_f": blfx_f, "aoi_rgn": aoi_rgn}
runpy.run_path(code_dir+'blooming_correction.py', init_globals=global_vars, run_name="__main__")
clear_junk(jdir)

#(5) topcoding correction
global_vars = {"dmsp_d": gdir+"/clean_dmsp/", "rc_d": rc_d, "viirs_d": viirs_d, "jdir": jdir,"tcfx_f": tcfx_f}
runpy.run_path(code_dir+'topcoding_correction.py', init_globals=global_vars, run_name="__main__")
clear_junk(jdir)


#(6) blooming + topcoding correction
global_vars = {"dmsp_d": gdir+"/bloom_fix/", "rc_d": rc_d,"viirs_d": viirs_d, "jdir": jdir,"tcfx_f": bltcfx_f}
runpy.run_path(code_dir+'topcoding_correction.py', init_globals=global_vars, run_name="__main__")
clear_junk(jdir)


#(7) downgrade viirs (raw DMSP)
global_vars = {"dmsp_f": dmsp_cln, "viirs_f": viirs_cln, "val_f": val_f, "jdir": jdir, 
               "aoi_rgn": aoi_rgn, "aoi_bff": aoi_bff, "aoi_gas": aoi_gas}
runpy.run_path(code_dir+'downgrade_viirs.py', init_globals=global_vars, run_name="__main__")
clear_junk(jdir)


#(8) downgrade viirs (blooming corrected)
global_vars = {"dmsp_f": blfx_f, "viirs_f": viirs_cln, "val_f": val_f, "jdir": jdir, 
               "aoi_rgn": aoi_rgn, "aoi_bff": aoi_bff, "aoi_gas": aoi_gas}
runpy.run_path(code_dir+'downgrade_viirs.py', init_globals=global_vars, run_name="__main__")
clear_junk(jdir)


#(9) downgrade viirs (topcode corrected)
global_vars = {"dmsp_f": tcfx_f, "viirs_f": viirs_cln, "val_f": val_f, "jdir": jdir, 
               "aoi_rgn": aoi_rgn, "aoi_bff": aoi_bff, "aoi_gas": aoi_gas}
runpy.run_path(code_dir+'downgrade_viirs.py', init_globals=global_vars, run_name="__main__")
clear_junk(jdir)


#(10) downgrade viirs (blooming and topcode corrected)
global_vars = {"dmsp_f": bltcfx_f, "viirs_f": viirs_cln, "val_f": val_f, "jdir": jdir, 
               "aoi_rgn": aoi_rgn, "aoi_bff": aoi_bff, "aoi_gas": aoi_gas}
runpy.run_path(code_dir+'downgrade_viirs.py', init_globals=global_vars, run_name="__main__")
clear_junk(jdir)

#END---------------------------------------------------------------------------