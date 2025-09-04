#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 13:01:46 2024

@author: malloryperillo

"""

import os
from urllib.request import urlretrieve
import requests
import json
from google_drive_downloader import GoogleDriveDownloader as gdd


#SCRIPT------------------------------------------------------------------------
if __name__ == "__main__":
    
    ###1. \world_nightlights\source\Li_etal_2021_series\
    
    ###Create folder 'Li_etal_2021_series' to hold data from the hoarmonisation of DMSP and VIIRS for 1992-2019 done by Li et al. 2020.
    

    directory_path1 = sdir+"/Li_etal_2021_series"

    
    directory_path1 = sdir+"/Li_etal_2021_series/"

    os.makedirs(directory_path1, exist_ok = True)
    
    
    ###Downlaod harmonisation data and place in the created folder
    
    url1 = (
           
            "https://figshare.com/ndownloader/articles/9828827/versions/2"
           
           )
    
    file1 = sdir +"/Li_etal_2021_series/DMSP_VIIRS_1992_2018.zip"
    
    urlretrieve(url1, file1)
    file_url = os.path.basename(url1)
    print(file_url + " has been downloaded")
    
    
    ###2. \world_nightlights\source\VIIRS\
        
    ###Create folder 'VIIRS' to hold data from the annual composites of VIIRS from 2012-2023 done by Elvidge et al. 2021. 
    
    directory_path2 = sdir+"/VIIRS"
    os.makedirs(directory_path2, exist_ok = True)
    
    ###Downlaod each year of data and place in the created folder
    
    ###2012
    
    url2a = (
           
            "https://eogdata.mines.edu/nighttime_light/annual/v20/2012/VNL_v2_npp_201204-201303_global_vcmcfg_c202102150000.average_masked.tif.gz"
           
           )
    
    file2a = sdir +"/VIIRS/VNL_v2_npp_201204-201303_global_vcmcfg_c202102150000.average_masked.tif.gz"
    
    urlretrieve(url2a, file2a)
    file_url = os.path.basename(url2a)
    print(file_url + " has been downloaded")
    
    ###2013
    
    url2b = (
           
            "https://eogdata.mines.edu/nighttime_light/annual/v20/2013/VNL_v2_npp_2013_global_vcmcfg_c202102150000.average_masked.tif.gz"
           
           )
    
    file2b = sdir +"/VIIRS/VNL_v2_npp_2013_global_vcmcfg_c202102150000.average_masked.tif.gz"
    
    urlretrieve(url2b, file2b)
    file_url = os.path.basename(url2b)
    print(file_url + " has been downloaded")
    
    ###2014
    
    url2c = (
           
            "https://eogdata.mines.edu/nighttime_light/annual/v20/2014/VNL_v2_npp_2014_global_vcmslcfg_c202102150000.average_masked.tif.gz"
           
           )
    
    file2c = sdir +"/VIIRS/VNL_v2_npp_2014_global_vcmslcfg_c202102150000.average_masked.tif.gz"
    
    urlretrieve(url2c, file2c)
    file_url = os.path.basename(url2c)
    print(file_url + " has been downloaded")
    
    ###2015
    
    url2d = (
           
            "https://eogdata.mines.edu/nighttime_light/annual/v20/2015/VNL_v2_npp_2015_global_vcmslcfg_c202102150000.average_masked.tif.gz"
           
           )
    
    file2d = sdir +"/VIIRS/VNL_v2_npp_2015_global_vcmslcfg_c202102150000.average_masked.tif.gz"
    
    urlretrieve(url2d, file2d)
    file_url = os.path.basename(url2d)
    print(file_url + " has been downloaded")
    
    ###2016
    
    url2e = (
           
            "https://eogdata.mines.edu/nighttime_light/annual/v20/2016/VNL_v2_npp_2016_global_vcmslcfg_c202102150000.average_masked.tif.gz"
           
           )
    
    file2e = sdir +"/VIIRS/VNL_v2_npp_2016_global_vcmslcfg_c202102150000.average_masked.tif.gz"
    
    urlretrieve(url2e, file2e)
    file_url = os.path.basename(url2e)
    print(file_url + " has been downloaded")
    
    ###2017
    
    url2f = (
           
            "https://eogdata.mines.edu/nighttime_light/annual/v20/2017/VNL_v2_npp_2017_global_vcmslcfg_c202102150000.average_masked.tif.gz"
           
           )
    
    file2f = sdir +"/VIIRS/VNL_v2_npp_2017_global_vcmslcfg_c202102150000.average_masked.tif.gz"
    
    urlretrieve(url2f, file2f)
    file_url = os.path.basename(url2f)
    print(file_url + " has been downloaded")
    
    ###2018
    
    url2g = (
           
            "https://eogdata.mines.edu/nighttime_light/annual/v20/2018/VNL_v2_npp_2018_global_vcmslcfg_c202102150000.average_masked.tif.gz"
           
           )
    
    file2g = sdir +"/VIIRS/VNL_v2_npp_2018_global_vcmslcfg_c202102150000.average_masked.tif.gz"
    
    urlretrieve(url2g, file2g)
    file_url = os.path.basename(url2g)
    print(file_url + " has been downloaded")
    
    ###2019
    
    url2h = (
           
            "https://eogdata.mines.edu/nighttime_light/annual/v20/2019/VNL_v2_npp_2019_global_vcmslcfg_c202102150000.average_masked.tif.gz"
           
           )
    
    file2h = sdir +"/VIIRS/VNL_v2_npp_2019_global_vcmslcfg_c202102150000.average_masked.tif.gz"
    
    urlretrieve(url2h, file2h)
    file_url = os.path.basename(url2h)
    print(file_url + " has been downloaded")
    
    ###2020
    
    url2i = (
           
            "https://eogdata.mines.edu/nighttime_light/annual/v20/2020/VNL_v2_npp_2020_global_vcmslcfg_c202102150000.average_masked.tif.gz"
           
           )
    
    file2i = sdir +"/VIIRS/VNL_v2_npp_2020_global_vcmslcfg_c202102150000.average_masked.tif.gz"
    
    urlretrieve(url2i, file2i)
    file_url = os.path.basename(url2i)
    print(file_url + " has been downloaded")
    
    ###2021
    
    url2j = (
           
            "https://eogdata.mines.edu/nighttime_light/annual/v20/2021/VNL_v2_npp_2021_global_vcmslcfg_c202203152300.average_masked.tif.gz"
           
           )
    
    file2j = sdir +"/VIIRS/VNL_v2_npp_2021_global_vcmslcfg_c202203152300.average_masked.tif.gz"
    
    urlretrieve(url2j, file2j)
    file_url = os.path.basename(url2j)
    print(file_url + " has been downloaded")
    
    ###2022
    
    url2k = (
           
            "https://eogdata.mines.edu/nighttime_light/annual/v22/2022/VNL_v22_npp-j01_2022_global_vcmslcfg_c202303062300.average_masked.dat.tif.gz"
           
           )
    
    file2k = sdir +"/VIIRS/VNL_v22_npp-j01_2022_global_vcmslcfg_c202303062300.average_masked.dat.tif.gz"
    
    urlretrieve(url2k, file2k)
    file_url = os.path.basename(url2k)
    print(file_url + " has been downloaded")
    
    ###2023
    
    url2l = (
           
            "https://eogdata.mines.edu/nighttime_light/annual/v22/2023/VNL_npp_2023_global_vcmslcfg_v2_c202402081600.average_masked.dat.tif.gz"
           
           )
    
    file2l = sdir +"/VIIRS/VNL_npp_2023_global_vcmslcfg_v2_c202402081600.average_masked.dat.tif.gz"
    
    urlretrieve(url2l, file2l)
    file_url = os.path.basename(url2l)
    print(file_url + " has been downloaded")
    
    
    ###3. \world_nightlights\source\DMSP_RC\
    
    ###Create folder 'DMSP_RC' to hold data for radiance calibrated DMSP done by Elvidge et al. 1999 and Hsu et al. 2014. 
    
    directory_path3 = sdir+"/DMSP_RC"
    os.makedirs(directory_path3, exist_ok = True)
    
    
    ###Downlaod radiance calibrated DMSP data and place in the created folder
    
    # Retrieve access token
    params = {
        'client_id': 'eogdata_oidc',
        'client_secret': '2677ad81-521b-4869-8480-6d05b9e57d48',
        'username': username,
        'password': password,
        'grant_type': 'password'
    }
    token_url = 'https://eogauth.mines.edu/auth/realms/master/protocol/openid-connect/token'
    #NB: the link may have changed to: 'https://eogauth-new.mines.edu/realms/eog/protocol/openid-connect/token'
    
    # Request token
    response = requests.post(token_url, data=params)
    access_token_dict = json.loads(response.text)
    access_token = access_token_dict.get('access_token')
    
    # Submit request for 2010 file 1 with token bearer
    
    ## Change data_url variable to the file you want to download
    data_url2 = 'https://eogdata.mines.edu/wwwdata/dmsp/rad_cal/F16_20100111-20101209_rad_v4.geotiff.tgz'
    auth = 'Bearer ' + access_token
    headers = {'Authorization': auth}
    response = requests.get(data_url2, headers = headers)
    
    # Get the filename from the data_url
    output_file2 = os.path.basename(data_url2)
    output_path2 = os.path.join(directory_path3, output_file2)
    
    #Write the file
    with open(output_path2, 'wb') as f:
       f.write(response.content)
    print(output_file2 + " has been downloaded")
    
    # Submit request for 2005 with token bearer
    
    ## Change data_url variable to the file you want to download
    data_url3 = 'https://eogdata.mines.edu/wwwdata/dmsp/rad_cal/F16_20051128-20061224_rad_v4.geotiff.tgz'
    auth = 'Bearer ' + access_token
    headers = {'Authorization': auth}
    response = requests.get(data_url3, headers = headers)
    
    # Get the filename from the data_url
    output_file3 = os.path.basename(data_url3)
    output_path3 = os.path.join(directory_path3, output_file3)
    
    #Write the file
    with open(output_path3, 'wb') as f:
       f.write(response.content)
    print(output_file3 + " has been downloaded")
    
    # Submit request for 2004 with token bearer
    
    ## Change data_url variable to the file you want to download
    data_url4 = 'https://eogdata.mines.edu/wwwdata/dmsp/rad_cal/F14_20040118-20041216_rad_v4.geotiff.tgz'
    auth = 'Bearer ' + access_token
    headers = {'Authorization': auth}
    response = requests.get(data_url4, headers = headers)
    
    # Get the filename from the data_url
    output_file4 = os.path.basename(data_url4)
    output_path4 = os.path.join(directory_path3, output_file4)
    
    #Write the file
    with open(output_path4, 'wb') as f:
       f.write(response.content)
    print(output_file4 + " has been downloaded")
    
    # Submit request for 2002 with token bearer
    
    ## Change data_url variable to the file you want to download
    data_url5 = 'https://eogdata.mines.edu/wwwdata/dmsp/rad_cal/F14-F15_20021230-20031127_rad_v4.geotiff.tgz'
    auth = 'Bearer ' + access_token
    headers = {'Authorization': auth}
    response = requests.get(data_url5, headers = headers)
    
    # Get the filename from the data_url
    output_file5 = os.path.basename(data_url5)
    output_path5 = os.path.join(directory_path3, output_file5)
    
    #Write the file
    with open(output_path5, 'wb') as f:
       f.write(response.content)
    print(output_file5 + " has been downloaded")
    
    # Submit request for 2000 with token bearer
    
    ## Change data_url variable to the file you want to download
    data_url6 = 'https://eogdata.mines.edu/wwwdata/dmsp/rad_cal/F12-F15_20000103-20001229_rad_v4.geotiff.tgz'
    auth = 'Bearer ' + access_token
    headers = {'Authorization': auth}
    response = requests.get(data_url6, headers = headers)
    
    # Get the filename from the data_url
    output_file6 = os.path.basename(data_url6)
    output_path6 = os.path.join(directory_path3, output_file6)
    
    #Write the file
    with open(output_path6, 'wb') as f:
       f.write(response.content)
    print(output_file6 + " has been downloaded")
    
    # Submit request for 1999 with token bearer
    
    ## Change data_url variable to the file you want to download
    data_url7 = 'https://eogdata.mines.edu/wwwdata/dmsp/rad_cal/F12_19990119-19991211_rad_v4.geotiff.tgz'
    auth = 'Bearer ' + access_token
    headers = {'Authorization': auth}
    response = requests.get(data_url7, headers = headers)
    
    # Get the filename from the data_url
    output_file7 = os.path.basename(data_url7)
    output_path7 = os.path.join(directory_path3, output_file7)
    
    #Write the file
    with open(output_path7, 'wb') as f:
       f.write(response.content)
    print(output_file7 + " has been downloaded")
    
    # Submit request for 1996 with token bearer
    
    ## Change data_url variable to the file you want to download
    data_url8 = 'https://eogdata.mines.edu/wwwdata/dmsp/rad_cal/F12_19960316-19970212_rad_v4.geotiff.tgz'
    auth = 'Bearer ' + access_token
    headers = {'Authorization': auth}
    response = requests.get(data_url8, headers = headers)
    
    # Get the filename from the data_url
    output_file8 = os.path.basename(data_url8)
    output_path8 = os.path.join(directory_path3, output_file8)
    
    #Write the file
    with open(output_path8, 'wb') as f:
       f.write(response.content)
    print(output_file8 + " has been downloaded")
    
    
    ###4. \world_nightlights\source\gas_flaring\
    
    ###Create folder 'gas_flaring' to hold data for regions of the world with substantial gas flaring (to be masked out from nightlights).
    
    directory_path4 = sdir+"/gas_flaring"
    os.makedirs(directory_path4, exist_ok = True)
    
    
    ###Downlaod radiance calibrated DMSP data and place in the created folder
    
    #Algeria
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_Algeria_1.tgz"
           
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #Angola
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_Angola_1.tgz"       
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #Argentina
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_Argentina_1.tgz"
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #Australia
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_Australia_1.tgz"
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #Azerbaijan
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_Azerbaijan_1.tgz"
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #Belgium
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_Belgium_1.tgz"
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #Bolivia
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_Bolivia_1.tgz"
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #Brazil
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_Brazil_1.tgz"
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #Brunei
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_Brunei_1.tgz"
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #Cameroon
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_Cameroon_1.tgz"
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #Canada
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_Canada_1.tgz"
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #Chad
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_Chad_1.tgz"
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #Chile
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_Chile_1.tgz"
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #China
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_China_1.tgz"
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #Colombia
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_Colombia_1.tgz"
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #Congo
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_Congo_1.tgz"
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #Cote dIvoire
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_Cote_dIvoire_1.tgz"
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #Dem Rep Congo
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_Dem_Rep_Congo_1.tgz"
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #Denmark
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_Denmark_1.tgz"
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #East Timor
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_East_Timor_1.tgz"
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #Ecuador
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_Ecuador_1.tgz"
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #Egypt
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_Egypt_1.tgz"
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #Eq Guinea
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_Eq_Guinea_1.tgz"
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #Gabon
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_Gabon_1.tgz"
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #Germany
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_Germany_1.tgz"
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #Ghana
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_Ghana_1.tgz"
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #India
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_India_1.tgz"
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #Indonesia
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_Indonesia_1.tgz"
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #Iran
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_Iran_1.tgz"
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #Iraq
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_Iraq_1.tgz"
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #Kazakhstan
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_Kazakhstan_1.tgz"
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #Kuwait
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_Kuwait_1.tgz"
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #Libya
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_Libya_1.tgz"
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #Malaysia
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_Malaysia_1.tgz"
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #Mauritania
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_Mauritania_1.tgz"
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #Mexico
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_Mexico_1.tgz"
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #Myanmar
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_Myanmar_1.tgz"
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #Netherlands
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_Netherlands_1.tgz"
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #Nigeria
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_Nigeria_1.tgz"
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #Norway
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_Norway_1.tgz"
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #Oman
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_Oman_1.tgz"
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #Peru
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_Peru_1.tgz"
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #Philippines
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_Philippines_1.tgz"
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #PNG
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_PNG_1.tgz"
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #Qatar
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_Qatar_1.tgz"
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #Romania
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_Romania_1.tgz"
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #Russia KM
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_Russia_KM_1.tgz"
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #Russia not KM
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_Russia_not_KM_1.tgz"
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #Saudi Arabia
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_Saudi_Arabia_1.tgz"
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #South Africa
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_South_Africa_1.tgz"
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #Sudan
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_Sudan_1.tgz"
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #Syria
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_Syria_1.tgz"
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #Thailand
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_Thailand_1.tgz"
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #Trinidad
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_Trinidad_1.tgz"
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #Tunisia
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_Tunisia_1.tgz"
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #Turkmenistan
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_Turkmenistan_1.tgz"
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #UAE
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_UAE_1.tgz"
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #UK
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_UK_1.tgz"
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #USA-Alaska
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_USA_Alaska_1.tgz"
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #USA-CONUS
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_USA_CONUS_1.tgz"
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #Uzbekistan
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_Uzbekistan_1.tgz"
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #Venezuela
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_Venezuela_1_point.tgz"
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #Vietnam
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_Vietnam_1.tgz"
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #Yemen
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_Yemen_1.tgz"
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    #New Zealand
    
    urlflare = (
           
            "https://www.ngdc.noaa.gov/eog/data/web_data/gasflares_v2/country_vectors_20090618/Flares_New_Zealand.tgz"
           )
    
    fileflare = os.path.basename(urlflare)
    outputflare = os.path.join(directory_path4, fileflare)
    
    urlretrieve(urlflare, outputflare)
    print(fileflare + " has been downloaded")
    
    
    ###5. \world_nightlights\source\DMSP\
    
    ###Create folder 'DMSP' to hold data for Version 4 DMSP-OLS nighttime lights done by Baugh et al. 2010 and Elvidge et al. 1997.
    
    directory_path5 = sdir+"/DMSP"
    os.makedirs(directory_path5, exist_ok = True)
    
    ###Downlaod nighttime light data and place in the created folder
    #Note: this data also comes from the EOG website and requires use of the account made for #3
    
    #1992 Satellite
    
    ## Change data_url variable to the file you want to download
    nl_url = 'https://eogdata.mines.edu/wwwdata/dmsp/v4composites_rearrange/F10_1992/F101992.v4b.global.stable_lights.avg_vis.tif.gz'
    auth = 'Bearer ' + access_token
    headers = {'Authorization': auth}
    response = requests.get(nl_url, headers = headers)
    
    # Get the filename from the data_url
    output_file = os.path.basename(nl_url)
    output_path = os.path.join(directory_path5, output_file)
    
    #Write the file
    with open(output_path, 'wb') as f:
       f.write(response.content)
    print(output_file + " has been downloaded")
    
    #1993 Satellite
    
    ## Change data_url variable to the file you want to download
    nl_url = 'https://eogdata.mines.edu/wwwdata/dmsp/v4composites_rearrange/F10_1993/F101993.v4b.global.stable_lights.avg_vis.tif.gz'
    auth = 'Bearer ' + access_token
    headers = {'Authorization': auth}
    response = requests.get(nl_url, headers = headers)
    
    # Get the filename from the data_url
    output_file = os.path.basename(nl_url)
    output_path = os.path.join(directory_path5, output_file)
    
    #Write the file
    with open(output_path, 'wb') as f:
       f.write(response.content)
    print(output_file + " has been downloaded")
    
    #1994 Satellite
    
    ## Change data_url variable to the file you want to download
    nl_url = 'https://eogdata.mines.edu/wwwdata/dmsp/v4composites_rearrange/F12_1994/F121994.v4b.global.stable_lights.avg_vis.tif.gz'
    auth = 'Bearer ' + access_token
    headers = {'Authorization': auth}
    response = requests.get(nl_url, headers = headers)
    
    # Get the filename from the data_url
    output_file = os.path.basename(nl_url)
    output_path = os.path.join(directory_path5, output_file)
    
    #Write the file
    with open(output_path, 'wb') as f:
       f.write(response.content)
    print(output_file + " has been downloaded")
    
    #1995 Satellite
    
    ## Change data_url variable to the file you want to download
    nl_url = 'https://eogdata.mines.edu/wwwdata/dmsp/v4composites_rearrange/F12_1995/F121995.v4b.global.stable_lights.avg_vis.tif.gz'
    auth = 'Bearer ' + access_token
    headers = {'Authorization': auth}
    response = requests.get(nl_url, headers = headers)
    
    # Get the filename from the data_url
    output_file = os.path.basename(nl_url)
    output_path = os.path.join(directory_path5, output_file)
    
    #Write the file
    with open(output_path, 'wb') as f:
       f.write(response.content)
    print(output_file + " has been downloaded")
    
    #1996 Satellite
    
    ## Change data_url variable to the file you want to download
    nl_url = 'https://eogdata.mines.edu/wwwdata/dmsp/v4composites_rearrange/F12_1996/F121996.v4b.global.stable_lights.avg_vis.tif.gz'
    auth = 'Bearer ' + access_token
    headers = {'Authorization': auth}
    response = requests.get(nl_url, headers = headers)
    
    # Get the filename from the data_url
    output_file = os.path.basename(nl_url)
    output_path = os.path.join(directory_path5, output_file)
    
    #Write the file
    with open(output_path, 'wb') as f:
       f.write(response.content)
    print(output_file + " has been downloaded")
    
    #1997 Satellite
    
    ## Change data_url variable to the file you want to download
    nl_url = 'https://eogdata.mines.edu/wwwdata/dmsp/v4composites_rearrange/F14_1997/F141997.v4b.global.stable_lights.avg_vis.tif.gz'
    auth = 'Bearer ' + access_token
    headers = {'Authorization': auth}
    response = requests.get(nl_url, headers = headers)
    
    # Get the filename from the data_url
    output_file = os.path.basename(nl_url)
    output_path = os.path.join(directory_path5, output_file)
    
    #Write the file
    with open(output_path, 'wb') as f:
       f.write(response.content)
    print(output_file + " has been downloaded")
    
    #1998 Satellite
    
    ## Change data_url variable to the file you want to download
    nl_url = 'https://eogdata.mines.edu/wwwdata/dmsp/v4composites_rearrange/F14_1998/F141998.v4b.global.stable_lights.avg_vis.tif.gz'
    auth = 'Bearer ' + access_token
    headers = {'Authorization': auth}
    response = requests.get(nl_url, headers = headers)
    
    # Get the filename from the data_url
    output_file = os.path.basename(nl_url)
    output_path = os.path.join(directory_path5, output_file)
    
    #Write the file
    with open(output_path, 'wb') as f:
       f.write(response.content)
    print(output_file + " has been downloaded")
    
    #1999 Satellite
    
    ## Change data_url variable to the file you want to download
    nl_url = 'https://eogdata.mines.edu/wwwdata/dmsp/v4composites_rearrange/F14_1999/F141999.v4b.global.stable_lights.avg_vis.tif.gz'
    auth = 'Bearer ' + access_token
    headers = {'Authorization': auth}
    response = requests.get(nl_url, headers = headers)
    
    # Get the filename from the data_url
    output_file = os.path.basename(nl_url)
    output_path = os.path.join(directory_path5, output_file)
    
    #Write the file
    with open(output_path, 'wb') as f:
       f.write(response.content)
    print(output_file + " has been downloaded")
    
    #2000 Satellite
    
    ## Change data_url variable to the file you want to download
    nl_url = 'https://eogdata.mines.edu/wwwdata/dmsp/v4composites_rearrange/F15_2000/F152000.v4b.global.stable_lights.avg_vis.tif.gz'
    auth = 'Bearer ' + access_token
    headers = {'Authorization': auth}
    response = requests.get(nl_url, headers = headers)
    
    # Get the filename from the data_url
    output_file = os.path.basename(nl_url)
    output_path = os.path.join(directory_path5, output_file)
    
    #Write the file
    with open(output_path, 'wb') as f:
       f.write(response.content)
    print(output_file + " has been downloaded")
    
    #2001 Satellite
    
    ## Change data_url variable to the file you want to download
    nl_url = 'https://eogdata.mines.edu/wwwdata/dmsp/v4composites_rearrange/F15_2001/F152001.v4b.global.stable_lights.avg_vis.tif.gz'
    auth = 'Bearer ' + access_token
    headers = {'Authorization': auth}
    response = requests.get(nl_url, headers = headers)
    
    # Get the filename from the data_url
    output_file = os.path.basename(nl_url)
    output_path = os.path.join(directory_path5, output_file)
    
    #Write the file
    with open(output_path, 'wb') as f:
       f.write(response.content)
    print(output_file + " has been downloaded")
    
    #2002 Satellite
    
    ## Change data_url variable to the file you want to download
    nl_url = 'https://eogdata.mines.edu/wwwdata/dmsp/v4composites_rearrange/F15_2002/F152002.v4b.global.stable_lights.avg_vis.tif.gz'
    auth = 'Bearer ' + access_token
    headers = {'Authorization': auth}
    response = requests.get(nl_url, headers = headers)
    
    # Get the filename from the data_url
    output_file = os.path.basename(nl_url)
    output_path = os.path.join(directory_path5, output_file)
    
    #Write the file
    with open(output_path, 'wb') as f:
       f.write(response.content)
    print(output_file + " has been downloaded")
    
    #2003 Satellite
    
    ## Change data_url variable to the file you want to download
    nl_url = 'https://eogdata.mines.edu/wwwdata/dmsp/v4composites_rearrange/F15_2003/F152003.v4b.global.stable_lights.avg_vis.tif.gz'
    auth = 'Bearer ' + access_token
    headers = {'Authorization': auth}
    response = requests.get(nl_url, headers = headers)
    
    # Get the filename from the data_url
    output_file = os.path.basename(nl_url)
    output_path = os.path.join(directory_path5, output_file)
    
    #Write the file
    with open(output_path, 'wb') as f:
       f.write(response.content)
    print(output_file + " has been downloaded")
    
    #2004 Satellite
    
    ## Change data_url variable to the file you want to download
    nl_url = 'https://eogdata.mines.edu/wwwdata/dmsp/v4composites_rearrange/F16_2004/F162004.v4b.global.stable_lights.avg_vis.tif.gz'
    auth = 'Bearer ' + access_token
    headers = {'Authorization': auth}
    response = requests.get(nl_url, headers = headers)
    
    # Get the filename from the data_url
    output_file = os.path.basename(nl_url)
    output_path = os.path.join(directory_path5, output_file)
    
    #Write the file
    with open(output_path, 'wb') as f:
       f.write(response.content)
    print(output_file + " has been downloaded")
    
    #2005 Satellite
    
    ## Change data_url variable to the file you want to download
    nl_url = 'https://eogdata.mines.edu/wwwdata/dmsp/v4composites_rearrange/F16_2005/F162005.v4b.global.stable_lights.avg_vis.tif.gz'
    auth = 'Bearer ' + access_token
    headers = {'Authorization': auth}
    response = requests.get(nl_url, headers = headers)
    
    # Get the filename from the data_url
    output_file = os.path.basename(nl_url)
    output_path = os.path.join(directory_path5, output_file)
    
    #Write the file
    with open(output_path, 'wb') as f:
       f.write(response.content)
    print(output_file + " has been downloaded")
    
    #2006 Satellite
    
    ## Change data_url variable to the file you want to download
    nl_url = 'https://eogdata.mines.edu/wwwdata/dmsp/v4composites_rearrange/F16_2006/F162006.v4b.global.stable_lights.avg_vis.tif.gz'
    auth = 'Bearer ' + access_token
    headers = {'Authorization': auth}
    response = requests.get(nl_url, headers = headers)
    
    # Get the filename from the data_url
    output_file = os.path.basename(nl_url)
    output_path = os.path.join(directory_path5, output_file)
    
    #Write the file
    with open(output_path, 'wb') as f:
       f.write(response.content)
    print(output_file + " has been downloaded")
    
    #2007 Satellite
    
    ## Change data_url variable to the file you want to download
    nl_url = 'https://eogdata.mines.edu/wwwdata/dmsp/v4composites_rearrange/F16_2007/F162007.v4b.global.stable_lights.avg_vis.tif.gz'
    auth = 'Bearer ' + access_token
    headers = {'Authorization': auth}
    response = requests.get(nl_url, headers = headers)
    
    # Get the filename from the data_url
    output_file = os.path.basename(nl_url)
    output_path = os.path.join(directory_path5, output_file)
    
    #Write the file
    with open(output_path, 'wb') as f:
       f.write(response.content)
    print(output_file + " has been downloaded")
    
    #2008 Satellite
    
    ## Change data_url variable to the file you want to download
    nl_url = 'https://eogdata.mines.edu/wwwdata/dmsp/v4composites_rearrange/F16_2008/F162008.v4b.global.stable_lights.avg_vis.tif.gz'
    auth = 'Bearer ' + access_token
    headers = {'Authorization': auth}
    response = requests.get(nl_url, headers = headers)
    
    # Get the filename from the data_url
    output_file = os.path.basename(nl_url)
    output_path = os.path.join(directory_path5, output_file)
    
    #Write the file
    with open(output_path, 'wb') as f:
       f.write(response.content)
    print(output_file + " has been downloaded")
    
    #2009 Satellite
    
    ## Change data_url variable to the file you want to download
    nl_url = 'https://eogdata.mines.edu/wwwdata/dmsp/v4composites_rearrange/F16_2009/F162009.v4b.global.stable_lights.avg_vis.tif.gz'
    auth = 'Bearer ' + access_token
    headers = {'Authorization': auth}
    response = requests.get(nl_url, headers = headers)
    
    # Get the filename from the data_url
    output_file = os.path.basename(nl_url)
    output_path = os.path.join(directory_path5, output_file)
    
    #Write the file
    with open(output_path, 'wb') as f:
       f.write(response.content)
    print(output_file + " has been downloaded")
    
    #2010 Satellite
    
    ## Change data_url variable to the file you want to download
    nl_url = 'https://eogdata.mines.edu/wwwdata/dmsp/v4composites_rearrange/F18_2010/F182010.v4d.global.stable_lights.avg_vis.tif.gz'
    auth = 'Bearer ' + access_token
    headers = {'Authorization': auth}
    response = requests.get(nl_url, headers = headers)
    
    # Get the filename from the data_url
    output_file = os.path.basename(nl_url)
    output_path = os.path.join(directory_path5, output_file)
    
    #Write the file
    with open(output_path, 'wb') as f:
       f.write(response.content)
    print(output_file + " has been downloaded")
    
    #2011 Satellite
    
    ## Change data_url variable to the file you want to download
    nl_url = 'https://eogdata.mines.edu/wwwdata/dmsp/v4composites_rearrange/F18_2011/F182011.v4c.global.stable_lights.avg_vis.tif.gz'
    auth = 'Bearer ' + access_token
    headers = {'Authorization': auth}
    response = requests.get(nl_url, headers = headers)
    
    # Get the filename from the data_url
    output_file = os.path.basename(nl_url)
    output_path = os.path.join(directory_path5, output_file)
    
    #Write the file
    with open(output_path, 'wb') as f:
       f.write(response.content)
    print(output_file + " has been downloaded")
    
    #2012 Satellite
    
    ## Change data_url variable to the file you want to download
    nl_url = 'https://eogdata.mines.edu/wwwdata/dmsp/v4composites_rearrange/F18_2012/F182012.v4c.global.stable_lights.avg_vis.tif.gz'
    auth = 'Bearer ' + access_token
    headers = {'Authorization': auth}
    response = requests.get(nl_url, headers = headers)
    
    # Get the filename from the data_url
    output_file = os.path.basename(nl_url)
    output_path = os.path.join(directory_path5, output_file)
    
    #Write the file
    with open(output_path, 'wb') as f:
       f.write(response.content)
    print(output_file + " has been downloaded")
    
    #2013 Satellite
    
    ## Change data_url variable to the file you want to download
    nl_url = 'https://eogdata.mines.edu/wwwdata/dmsp/v4composites_rearrange/F18_2013/F182013.v4c.global.stable_lights.avg_vis.tif.gz'
    auth = 'Bearer ' + access_token
    headers = {'Authorization': auth}
    response = requests.get(nl_url, headers = headers)
    
    # Get the filename from the data_url
    output_file = os.path.basename(nl_url)
    output_path = os.path.join(directory_path5, output_file)
    
    #Write the file
    with open(output_path, 'wb') as f:
       f.write(response.content)
    print(output_file + " has been downloaded")
    
    
    ###6. \world_nightlights\source\admin_boundaries\
        
    ###Create folder 'admin_boundaries' to hold data for world region boundaries from ArcGIS online. 
    
    directory_path6 = sdir+"/admin_boundaries"
    os.makedirs(directory_path6, exist_ok = True)
    
    ###Downlaod world regional boundary data and place in the created folder
    
    #world_regions.cpg
    
    gdd.download_file_from_google_drive(file_id='19yy-U5Ur4D4o0eYl6Ol7sQmT8ETfn37-',
                                        dest_path= directory_path6 + '/world_regions.cpg',
                                        unzip=False)
    print("world_regions.cpg has been downloaded")
    
    #world_regions.dbf
    
    gdd.download_file_from_google_drive(file_id='1tc3ZQKeswoi2Vl_P0bW9wKCgJ9zCd115',
                                        dest_path= directory_path6 + '/world_regions.dbf',
                                        unzip=False)
    print("world_regions.dbf has been downloaded")
    
    #world_regions.lpk
    
    gdd.download_file_from_google_drive(file_id='1Xhx48MeMlAzR8rnNc5zTDEBIdhiI2DGV',
                                        dest_path= directory_path6 + '/world_regions.lpk',
                                        unzip=False)
    print("world_regions.lpk has been downloaded")
    
    #world_regions.prj
    
    gdd.download_file_from_google_drive(file_id='1djt-rIfN7MPy1NE1hhmHIEnBJNzmBlZW',
                                        dest_path= directory_path6 + '/world_regions.prj',
                                        unzip=False)
    print("world_regions.prj has been downloaded")
    
    #world_regions.shp
    
    gdd.download_file_from_google_drive(file_id='17TOG-CoosRBE84ObLbds1O1tq14lAklr',
                                        dest_path= directory_path6 + '/world_regions.shp',
                                        unzip=False)
    print("world_regions.shp has been downloaded")
    
    #world_regions.shx
    
    gdd.download_file_from_google_drive(file_id='1ylDPxHnreqdtGIADtPfXj5s0GsPsAvDB',
                                        dest_path= directory_path6 + '/world_regions.shx',
                                        unzip=False)
    print("world_regions.shx has been downloaded")
    
    
    
    
    ###7. \world_nightlights\source\DVNL\
    
    ###Create folder 'DVNL' to hold data for DMSP-like Nighttime Lights Derived from VIIRS (DVNL) done by Nechaev et al. 2021.
    
    directory_path7 = sdir+"/DVNL"
    os.makedirs(directory_path7, exist_ok = True)
    
    ###Downlaod DMSP-like nighttime lights derived data and place in the created folder
    
    #2013
    
    url_dvnl = (
           
            "https://eogdata.mines.edu/wwwdata/viirs_products/dvnl/DVNL_2013.tif"
           )
    
    filedvnl = os.path.basename(url_dvnl)
    outputdvnl = os.path.join(directory_path7, filedvnl)
    urlretrieve(url_dvnl, outputdvnl)
    print(filedvnl + " has been downloaded")
    
    #2014
    
    url_dvnl = (
           
            "https://eogdata.mines.edu/wwwdata/viirs_products/dvnl/DVNL_2014.tif"
           )
    
    filedvnl = os.path.basename(url_dvnl)
    outputdvnl = os.path.join(directory_path7, filedvnl)
    urlretrieve(url_dvnl, outputdvnl)
    print(filedvnl + " has been downloaded")
    
    #2015
    
    url_dvnl = (
           
            "https://eogdata.mines.edu/wwwdata/viirs_products/dvnl/DVNL_2015.tif"
           )
    
    filedvnl = os.path.basename(url_dvnl)
    outputdvnl = os.path.join(directory_path7, filedvnl)
    urlretrieve(url_dvnl, outputdvnl)
    print(filedvnl + " has been downloaded")
    
    #2016
    
    url_dvnl = (
           
            "https://eogdata.mines.edu/wwwdata/viirs_products/dvnl/DVNL_2016.tif"
           )
    
    filedvnl = os.path.basename(url_dvnl)
    outputdvnl = os.path.join(directory_path7, filedvnl)
    urlretrieve(url_dvnl, outputdvnl)
    print(filedvnl + " has been downloaded")
    
    #2017
    
    url_dvnl = (
           
            "https://eogdata.mines.edu/wwwdata/viirs_products/dvnl/DVNL_2017.tif"
           )
    
    filedvnl = os.path.basename(url_dvnl)
    outputdvnl = os.path.join(directory_path7, filedvnl)
    urlretrieve(url_dvnl, outputdvnl)
    print(filedvnl + " has been downloaded")
    
    #2018
    
    url_dvnl = (
           
            "https://eogdata.mines.edu/wwwdata/viirs_products/dvnl/DVNL_2018.tif"
           )
    
    filedvnl = os.path.basename(url_dvnl)
    outputdvnl = os.path.join(directory_path7, filedvnl)
    urlretrieve(url_dvnl, outputdvnl)
    print(filedvnl + " has been downloaded")
    
    #2019
    
    url_dvnl = (
           
            "https://eogdata.mines.edu/wwwdata/viirs_products/dvnl/DVNL_2019.tif"
           )
    
    filedvnl = os.path.basename(url_dvnl)
    outputdvnl = os.path.join(directory_path7, filedvnl)
    urlretrieve(url_dvnl, outputdvnl)
    print(filedvnl + " has been downloaded")
    
    
    print("All source data has been downloaded")
    

