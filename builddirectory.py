from datetime import datetime
import os
from variables import api_pull
from pathlib import Path
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
    print('  Building directory structure on OneDrive...'),  # add a line to handle exceptions?
    acs_year = str(year_int-4) + 'to' + str(year_int)[-2:]
    
    # TO DO: this path will change depending on machine, so how do we do that?
    base_dir = Path(f"/home/fullerm/OneDrive - Toledo Metropolitan Area Council of Governments/Documents/Census_Bureau/American_Community_Survey/{acs_year}")
    
    # Create base directory if it doesn't exist
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    # Create subdirectories if they don't exist
    # for geo in api_pull:
    #     directory = base_dir.joinpath(geo)
    #     if not os.path.exists(directory):
    #         os.makedirs(directory)
    print('\bDone')

    return base_dir

if __name__ == '__main__':
    builddirectory(2017)