# ILLUMINATING AFRICA?

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
2. the geographical area of interest (AOI) for your project: default is the whole world (excluding Antartica)

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
  - os (standard library)
  - shutil (standard library)
  - time (standard library)
  - zipfile (standard library)

Requirements file (conda / pip install file)

## 2 Data and their sources

Input (source) and output (gen) data are stored in a directory `.\world_nightlights` with sub-directories `.\world_nightlights\source` and `.\world_nightlights\gen`. It is necessary to download the source data and store it in the correct sub-directories for the code to run wihtout changes

### 2.1 Obtaining source data
All data used in this analysis is from free, publicly available sources and is available for download (see below). While all data is freely available, the source data is under a variety of licenses that limit re-distribution of data in various ways. To accommodate these agreements, we do not host any of the raw data that falls under these restrictions. Instructions are provided below for obtaining each of the six input datasets.

1. `.\world_nightlights\source\DMSP_VIIRS_1992_2018` contains data from the harmonisation of DMSP and VIIRS for 1992-2019 done by Li et al. 2020 in Nature. This was last downloaded 11/03/2021. It is available [here](https://figshare.com/articles/dataset/Harmonization_of_DMSP_and_VIIRS_nighttime_light_data_from_1992-2018_at_the_global_scale/9828827/2).

2) VIIRS
	-Data from the annual composites of VIIRS from 2012-2021 (i.e. Annual VNL V2) done by Elvidge et al. 2021 in Remote Sensing
	-Data from the annual composites of VIIRS from 2022-2023 (i.e. Annual VNL V2.2) done by Elvidge et al. 2021 in Remote Sensing
	-The files come either masked or not. The masked files rounds low-light pixels down to zero and are much smaller files. I believe we should use the masked files.
	-I downloaded the 'average' products, we may also be interested in the 'median'.
	-First (2012-2020)downloaded 10/03/2021, second (2021-2023)downloaded 01/05/2024 
	-Available at https://eogdata.mines.edu/products/vnl/

3) DMSP_RC
	-Data for radiance calibrated DMSP (1996,1999,2000,2003,2004,2006, and 2010) done by Elvidge et al. 1999 in Remote Sensing of Environment and Hsu et al. 2015 in Remote Sensing.
	-Last downloaded 22/02/2021 
	-Available at https://eogdata.mines.edu/products/dmsp/

4) gas_flaring
	-Shapefiles of gasflaring areas by country
	-NB: I had to also manually edit mauritania, cote d'ivoire, and ghana (these are labelled by [filenmae]_fixed)
	-Last downloaded 05/03/2021 
	-Available at https://ngdc.noaa.gov/eog/interest/gas_flares_countries_shapefiles.html

5) DMSP
	-Version 4 DMSP-OLS nightime lights
	-Took data for each year from the most recent satelite, e.g. 1994 data is from sattelite F12 not F10
	-Downloaded on July 28, 2021
	-Downloaded from https://eogdata.mines.edu/products/dmsp/#v4_dmsp_download

6) "admin_boundaries/world_regions.shp"
	This data is available (in gbd form) from ArcGIS
	downloaded from: https://www.arcgis.com/home/item.html?id=84dbc97915244e35808e87a881133d09
	downloaded on: March 3, 2021

## Installation Instructions
Clone the repository and install requirements.


## 
