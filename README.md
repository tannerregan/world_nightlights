# Illuminating Africa?

This repository provides the code required to produce the dataset described and used the main text of:

Chiovelli, G., S. Michalopoulos, E. Papaioannou, and T. Regan, (2023). [Illuminating Africa?](https://tannerregan.github.io/tanner_regan/IlluminatingAfrica_Chiovelli_etal_unp2023.pdf)

This project processes satellite imagery data to generate a consistent time series of nightlight data from 1992 to 2023. Initially, the scripts clean and correct various issues, including blooming and topcoding, in data collected by the DMSP satellites from 1992 to 2012. Subsequently, the project handles VIIRS data from 2013 to 2023, downgrading its resolution to match that of the earlier DMSP series. The result is a harmonized and continuous panel of global nightlights, facilitating longitudinal studies and analyses.

This repository also serves as open source code for researchers to meet their specific research needs by:
1. Adjusting the cleaning processes (e.g. DMSP blooming and topcoding corrections, or VIIRS downgrading).
2. Using alternative input DMSP or VIIRS data to produce the corrected series.

The final dataset built with default settings is available for [download](https://drive.google.com/drive/folders/1smOB47MJra-vdDXyYvz5uXEA3NFsQj44?usp=sharing). However, we also strongly encourage those working with the data to read the source code provided in this repository. We welcome any constructive feedback that could help improve the code. 

## 1. Structure of the repository

The code folder is organized into an analysis pipeline and a package containing tools necessary to enable that pipeline.

1. `prep_inputs.py`
Prepares input datasets for processing. This script organizes and structures the raw data, making it ready for cleaning and correction processes.
2. `clean_dmsp.py`
Cleans data from the DMSP satellites. This involves filtering, artifact removal, and preliminary data corrections specific to the DMSP sensor characteristics.
3. `clean_viirs.py`
Cleans data from the VIIRS satellite. Adjusts for different anomalies and calibrates the data against known benchmarks to ensure consistency across different years.
4. `clean_dvnl.py`
Handles specific cleaning procedures for the Day/Night Band of the VIIRS satellite, focusing on issues unique to nightlight data collection during low light conditions.
5. `blooming_correction.py`
Mitigates the blooming effect seen in bright urban areas where light appears to bleed over into adjacent areas, distorting true light distributions.
6. `topcoding_correction.py`
Corrects topcoding errors where overly bright values are clipped at a maximum. This script redistributes such values to provide a more accurate representation of the light intensity.
7. `downgrade_viirs.py`
Adjusts the resolution of VIIRS data to match that of older sensors, allowing for consistent comparisons across the dataset's entire time span.
8. `0_runme.py`
Acts as the main executable that runs all the above scripts in sequence. This script coordinates the data flow between processes, ensuring each step is executed on the correctly prepared dataset.

### 1.1. Running the Project
To run the entire pipeline, execute the script [0_runme.py](https://github.com/tannerregan/world_nightlights/blob/main/code/0_runme.py) in python. 

Before running, adjust the high-level parameters in the 0_runme.py code:
1. the path names for your local machine
2. the geographical area of interest (AOI) for your project: default is the whole world (excluding Antarctica)

Make sure to run in an environment with the following prerequisties. 

### 1.2. Python Prerequisites
- Python 3.x
- Libraries:
  - numpy
  - pandas
  - scipy
  - matplotlib
  - geopandas
  - rasterio
  - sklearn
  - statsmodels
  - pyproj
  - os (standard library)
  - shutil (standard library)
  - time (standard library)
  - zipfile (standard library)

### 1.3 Computing Environment

You will need to install and activate our `illuminating-env` conda environment. Once you have [anaconda](https://www.anaconda.com/) installed on your machine, from the root directory of this repository, run:
```
conda env create -f code/environment.yml
conda activate illuminating-env
```


## 2 Data and their sources

Input (source) and output (gen) data are stored in a directory `.\world_nightlights` with sub-directories `.\world_nightlights\source` and `.\world_nightlights\gen`. It is necessary to download the source data and store it in the correct sub-directories for the code to run without changes, for details see below.

### 2.1 Obtaining source data
All data used in this analysis is from free, publicly available sources and is available for download (see below). While all data is freely available, the source data is under a variety of licenses that limit re-distribution of data in various ways. To accommodate these agreements, we do not host any of the raw data that falls under these restrictions. Instructions are provided below for obtaining each of the six input datasets. Save the downloaded data to their respective directories (see below) exactly as they come. 

1. `.\world_nightlights\source\DMSP_VIIRS_1992_2018\` contains data from the harmonisation of DMSP and VIIRS for 1992-2019 done by [Li et al. 2020](https://doi.org/10.3390/rs9060637). This was last downloaded 11/03/2021. It is available [here](https://figshare.com/articles/dataset/Harmonization_of_DMSP_and_VIIRS_nighttime_light_data_from_1992-2018_at_the_global_scale/9828827/2).

2. `.\world_nightlights\source\VIIRS\` contains data from the annual composites of VIIRS from 2012-2023 done by [Elvidge et al. 2021](https://doi.org/10.3390/rs13050922). We use the 'average masked' products. For (2013-2020) we use the series 'Annual VNL V2' available [here](https://eogdata.mines.edu/nighttime_light/annual/v20/), and last downloaded 10/03/2021. For (2021-2023) we use the series 'Annual VNL V2.1' available [here](https://eogdata.mines.edu/nighttime_light/annual/v21/), and last downloaded 01/05/2024. For the year 2012, VIIRS is only available for a portion of the year, in order to have a full year we use the prouct `VNL_v2_npp_201204-201212_global_vcmcfg_c202101211500` which uses data from April 2012 to March 2013. It is available [here](https://eogdata.mines.edu/nighttime_light/annual/v20/2012/), and last downloaded 10/03/2021.

3. `.\world_nightlights\source\DMSP_RC\` contains data for radiance calibrated DMSP (1996,1999,2000,2003,2004,2006, and 2010) done by [Elvidge et al. 1999](https://doi.org/10.1016/S0034-4257(98)00098-4) and [Hsu et al. 2015](https://doi.org/10.3390/rs70201855). This was last downloaded 22/02/2021. It is available [here](https://eogdata.mines.edu/products/dmsp/#rad_cal).

4. `.\world_nightlights\source\gas_flaring\` contains data for regions of the world with substantial gas flaring (to be masked out from nightlights). This was last downloaded 05/03/2021. It is available [here](https://ngdc.noaa.gov/eog/interest/gas_flares_countries_shapefiles.html).

5. `.\world_nightlights\source\DMSP\` contains data for Version 4 DMSP-OLS nightime lights done by [Baugh et al. 2010](https://dx.doi.org/10.7125/apan.30.17) and [Elvidge et al. 1997](https://www.asprs.org/wp-content/uploads/pers/97journal/june/1997_jun_727-734.pdf). For each year, take data from the most recent satelite, e.g. 1994 data is from sattelite F12 not F10. This was last downloaded 28/06/2021. It is available [here](https://eogdata.mines.edu/products/dmsp/#v4_dmsp_download).

6.`.\world_nightlights\source\admin_boundaries\` contains data for world regions boundaries from [ArcGIS online](https://www.arcgis.com/home/item.html?id=84dbc97915244e35808e87a881133d09). This was last downloaded 03/03/2021. It is available [here](https://drive.google.com/drive/folders/1CMxRy0qFAAtSv7-kFYAkNg4AvuLIEddi?usp=drive_link). 


## 
