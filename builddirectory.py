from datetime import datetime
import os
from variables import api_pull
def builddirectory(year_int):
    ##
    # GET THE USER'S INPUT ON WHAT DATA TO PULL
    ##
    #year = datetime.now()
    # year = input('What ACS 5 year data set (enter 2013 for 2009-13)? ')#input function creates a string
     # for the 2017 run, this will return 2016 ACS Data
    print('Fetching Data for ' + str(year_int))
    ##
    # BUILD DIRECTORIES ON Z TO HOLD CSV FILES
    ##
    print('  Building directory structure on Z:\...'),  # add a line to handle exceptions?
    acs_year = str(year_int-4) + 'to' + str(year_int)[-2:]
    base_dir = "//DELLSERVER2/UserData/fullerm/Census_Bureau/American_Community_Survey/" + acs_year
    # Create base directory if it doesn't exist
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    # Create subdirectories if they don't exist
    for geo in api_pull:
        directory = base_dir + '\\' + geo
        if not os.path.exists(directory):
            os.makedirs(directory)
    print('\bDone')

    return base_dir

if __name__ == '__main__':
    builddirectory()