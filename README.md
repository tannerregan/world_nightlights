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

### Input Data and Their Sources
ensure they are pre-downloaded and structured as expected by the scripts

## Installation Instructions
Clone the repository and install requirements.


## 
