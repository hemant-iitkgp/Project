# Project Instructions and Description

## INSTRUCTIONS TO RUN THE CODE

The provided makefile will run the code in the following order:

### 1. ImageDownloader.py
- Downloads all images listed in `locations.xlsx` file into the `Images` folder
- 40 images per Subdistrict will be downloaded (480 images total)
- **Important**: Replace the API key with your own Google Maps API key
- API key can be generated from Google Maps API

### 2. ImageLabel.py
- Labels all downloaded images and saves the labels in respective folders with the images
- Requires credentials JSON file (generate your own and edit file accordingly)

### 3. Tertile.py
- Divides Subdistricts into tertiles based on three metrics:
  - Transportation
  - Poverty
  - Nature
- Classification based on image labels

### 4. datacleaning.py
- Cleans the `OriginalDataset.csv`:
  - Removes duplicates
  - Fills limited NULL values with mean values
  - Removes rows with all NULL values
- Stores cleaned data in `cleaned.csv`

### 5. rate.py
- Divides values by respective population count of each subdistrict
- Standardizes values to z-score along rows
- Stores results in `cleaned_output.csv`

### 6. main.py > output.txt
- Processes data to apply adjusted linear regression for each health scheme
- Uses dependent and control variables from `variables.txt`
- Stores results in `result.csv`

## Required Libraries and Resources
- Pandas
- Numpy
- os
- re
- scipy
- statsmodels
- tabulate
- google.cloud
- requests
- Gomaps.pro

## PROJECT DESCRIPTION

### Abstract
We utilized Google Street View (GSV) images and computer vision to analyze neighborhood built environments across Mirzapur and its 12 Subdistricts. The study collected over 480 GSV images. Using computer vision for image labeling, we investigated associations between built environments and county health outcomes, while controlling for demographic and economic factors.

### Methods

#### Data Collection
- Used official state health scheme data to create database of Mirzapur's 12 Subdistricts
- Retrieved GSV images using Google Street View API
- Collected four 640x640 pixel images per intersection (N,S,E,W views)
- Total dataset: 480 images from 12 Subdistricts of Mirzapur

#### Image Processing
- Utilized Google Vision API for automated image labeling
- Focused on built environment characteristics:
  - Transportation
  - Poverty
  - Nature

#### Analysis
- Categorized built environment characteristics into tertiles
- Implemented adjusted linear regression models
- Controlled for:
  - Population density
  - Respective control variables for each dependent variable according to indicators in the OriginalDataSet.csv
