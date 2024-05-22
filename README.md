# Nighttime Satellite Image Processing
This code compiles data for  Chiovelli et al. (2023)

This project processes and cleans nighttime satellite imagery from various sources such as DMSP, VIIRS, and DVNL. It includes steps for correcting blooming and topcoding artifacts, downgrading data resolutions, and preparing data for analysis.

## Project Structure

- `0_runme.py`: Main script orchestrating the data processing workflow.
- `blooming_correction.py`: Corrects blooming artifacts in the satellite images.
- `clean_dmsp.py`: Processes and cleans DMSP data.
- `clean_dvnl.py`: Cleans and preprocesses DVNL data.
- `clean_viirs.py`: Cleans and preprocesses VIIRS data.
- `downgrade_viirs.py`: Downgrades VIIRS data to match DMSP resolution.
- `prep_inputs.py`: Prepares input data for processing.
- `topcoding_correction.py`: Corrects topcoding issues in the data.
- `config.json`: Configuration file for setting paths and other parameters.

## Setup

### Prerequisites

- Python 3.6 or higher
- Required Python packages: `arcpy`, `shutil`, `runpy`, `os`, `logging`, `json`, `pathlib`

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/nighttime-satellite-image-processing.git
    cd nighttime-satellite-image-processing
    ```

2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

### Configuration

1. Update the `config.json` file with the appropriate paths for your data and output directories.

    ```json
    {
        "base_dir": "C:/Users/tanner_regan/data_main/world_nightlights",
        "directories": {
            "to_clear": [
                "gen",
                "__junk"
            ],
            "to_create": [
                "gen/clean_dmsp",
                "gen/downgrade_viirs_validation"
            ]
        },
        "paths": {
            "dmsp_viirs_zip": "source/Li_etal_2021_series/DMSP_VIIRS_1992_2018.zip",
            "gas_flaring": "source/gas_flaring/",
            "world_regions": "source/admin_boundaries/world_regions.shp"
        },
        "output": {
            "aoi_regions": "gen/AOI_regions.tif",
            "aoi_buffered": "gen/AOI_buffered.tif",
            "aoi_gasmask": "gen/AOI_gasmask.tif"
        },
        "scripts": {
            "prep_inputs": "C:/Users/tanner_regan/Documents/GitHub/world_nightlights/code/prep_inputs.py",
            "clean_dmsp": "C:/Users/tanner_regan/Documents/GitHub/world_nightlights/code/clean_dmsp.py"
        }
    }
    ```

## Usage

1. Run the main script to start the data processing workflow:

    ```bash
    python 0_runme.py
    ```

2. The script will execute the following steps:
    - Clear and set up necessary directories
    - Run preprocessing scripts
    - Clean DMSP data
    - Apply blooming and topcoding corrections
    - Downgrade VIIRS data

## Logging

The script uses Python's logging module to provide detailed execution logs. Logs are printed to the console and can be redirected to a file if needed.

## Contributing

Contributions are welcome! Please create an issue to discuss any changes or improvements before submitting a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

Special thanks to the contributors and the open-source community for their valuable support and tools.

