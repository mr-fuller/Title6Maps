# Title6Maps
Get ACS data from the appropriate API and join them to Census Tract and Block Group feature classes used for Title 6 and Environmental Justice analyses.

# How to use
This project is run in a python environment using conda that comes with ArcGIS Pro. The most important packages needed are:
* python 3.4.4
* pandas 0.20.1 
* requests 2.14.2

1. Create python environment with aforementioned packages
2. Save all python files to same directory
3. Update the *base_dir* variable with a file location from your computer
4. Navigate to the directory where you saved all the files with command prompt
5. type 'python main.py'
6. troubleshoot any errors and fix them or report an issue on github
7. check the directory you specified in step 3 
8. profit?

And I suppose you need ArcMap for joining the data to the geographies part. You can use QGIS and get spatial files from the Census Website or API. I will work to perform spatial operations with gdal bindings or geopandas so that the script can be run without ArcMap from soup to nuts.
