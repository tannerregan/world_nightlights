# Satellite Nightlight Data Processing (1992-2023)

## Overview
This project processes satellite imagery data to generate a consistent time series of nightlight data from 1992 to 2023. Initially, the scripts clean and correct various issues, including blooming and topcoding, in data collected by the DMSP satellites from 1992 to 2012. Subsequently, the project handles VIIRS data from 2013 to 2023, downgrading its resolution to match that of the earlier DMSP series. The result is a harmonized and continuous panel of global nightlights, facilitating longitudinal studies and analyses.

## Prerequisites
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
- Satellite image data files (ensure they are pre-downloaded and structured as expected by the scripts)

## Installation Instructions
Clone the repository and install requirements.

## Input Data and Their Sources

## Project Structure

### 1. `prep_inputs.py`
Prepares input datasets for processing. This script organizes and structures the raw data, making it ready for cleaning and correction processes.

### 2. `clean_dmsp.py`
Cleans data from the DMSP satellites. This involves filtering, artifact removal, and preliminary data corrections specific to the DMSP sensor characteristics.

### 3. `clean_viirs.py`
Cleans data from the VIIRS satellite. Adjusts for different anomalies and calibrates the data against known benchmarks to ensure consistency across different years.

### 4. `clean_dvnl.py`
Handles specific cleaning procedures for the Day/Night Band of the VIIRS satellite, focusing on issues unique to nightlight data collection during low light conditions.

### 5. `downgrade_viirs.py`
Adjusts the resolution of VIIRS data to match that of older sensors, allowing for consistent comparisons across the dataset's entire time span.

### 6. `topcoding_correction.py`
Corrects topcoding errors where overly bright values are clipped at a maximum. This script redistributes such values to provide a more accurate representation of the light intensity.

### 7. `blooming_correction.py`
Mitigates the blooming effect seen in bright urban areas where light appears to bleed over into adjacent areas, distorting true light distributions.

### 8. `0_runme.py`
Acts as the main executable that runs all the above scripts in sequence. This script coordinates the data flow between processes, ensuring each step is executed on the correctly prepared dataset.

## Running the Project
To run the entire pipeline, execute the following command:
```bash
python 0_runme.py
