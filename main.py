# scrape the release date of ACS, then test that against current date
# if released, download Title XI related tables and create updated maps

# Download Title 6 data from the ACS
# updated for use in arcgis Pro

import requests, json
import pandas
import os
import pandas as pd
from variables import year_int,api_pull,api_key,fips, variable_list, email_id, email_password, email_server, email_port
from builddirectory import builddirectory
from calculate_ej_indicators import calculate_ej_indicators
# from buildacsdict import buildacsdict
from downloadandsave import download_and_save_data
# from spatialize import spatialize
from pip_summary import summarize_region
from pathlib import Path
# from add_to_agol import add_to_agol


from datetime import datetime
start_time = datetime.now()
print('  Testing year input...'),

# Build the API URL
variables_url = 'https://api.census.gov/data/' + str(year_int) + '/acs/acs5/variables.json'
# Read in the data
response = requests.get(url=variables_url)
# Check to make sure we could pull variables
while response.status_code == 404:

    print('\bNo data for ' + str(year_int) + '. Trying previous year')
    year_int= year_int - 1
    # Build the API URL
    variables_url = 'https://api.census.gov/data/' + str(year_int) + '/acs/acs5/variables.json'
    # Read in the data
    response = requests.get(url=variables_url)
print(year_int)
base_dir = builddirectory(year_int)
poverty_level = 0

#
print("Getting poverty level data... ")
#HHS value for a family of four for 2016, THIS has to be updated annually; can i scrape this value?
poverty_dict = {
    '2021': 26500,
    '2020': 26200,
    '2019': 25750,
    '2018': 25100,
    '2017': 24600,
    '2016': 24300,
    '2015': 24250,
    '2014': 23850,
    '2013': 23550,
    '2012': 23050,
    '2011': 22350,
    '2010': 22050
                }
if str(year_int) not in poverty_dict.keys():
    print('No Poverty Level data available for that year. Please update it, Mike.')
    quit()
else:
    poverty_level = poverty_dict[str(year_int)]
    print('Poverty Level for a family of 4 in ' + str(year_int) + ' is $' + str(poverty_level))
# [acs_dict, table_list] = buildacsdict(year_int)
 # = buildacsdict()[1]
##
# DOWNLOAD ACS DATA
##

data_str = response.json().get('variables')
# json_data = json.loads(data_str)
# print(data_str.keys())
not_available_via_api = list()  # This will hold the tables we can't get via the API
# eliminate/skip variables not available in api for that year
for i in variable_list[:]:
    if i not in data_str.keys():
        not_available_via_api.append(i)
        variable_list.remove(i)
print(f'Variables {not_available_via_api} not available.')
print('  Downloading tables for')

i = 0
counties_t = pd.DataFrame()
counties_b = pd.DataFrame()
dfs = []
# try:
dfs = download_and_save_data(variable_list, fips, api_key, year_int)
# except:
    
    # dfs = download_and_save_data(variable_list, fips, api_key, year_int)

print('  Assembling Title6 Stats...'),

calculate_ej_indicators(dfs, year_int)


print('\bDone')
print('  Appending Title 6 Stats...'),
# csv_path = base_dir + '\\' + location + '\\Title6.csv'

## I can consolidate the following lines(?) to a couple lines in the for loop if I use df.name or namedtuple

df00t = dfs[1] #pandas.read_csv(csv_path2 + '\\Title6_t.csv')
counties_t = counties_t.append(df00t)
counties_t.to_csv(base_dir.joinpath('Title6_t.csv'))
# for block groups
df00b = dfs[0] #pandas.read_csv(csv_path2 +'\\Title6_b.csv')
counties_b = counties_b.append(df00b)
counties_b.to_csv(base_dir.joinpath('Title6_b.csv'))
print('\bDone')

# Determine EJ status of block groups
print(' Determining EJ Areas ... ')

summarize_region(counties_b,counties_t,base_dir, year_int, poverty_level)
# pip_summary(counties_b,counties_t,base_dir,'pip')
# This section joins tables to respective geographies
# spatialize(base_dir)

# manipulate layers to display data

# export to pdf
print('\bDone')
print('All data is now stored on OneDrive and Postgres!')
print('\rThe following tables were not downloaded:')
for table in not_available_via_api:
    print('  ' + table)
'''
print('  Uploading to ArcGIS Online...')

# add_to_agol()

maup = m.listLayers()[0:2]
for item in maup:
    print(item.name)

sddraft = proj_loc + "TMACOG_Title6_bg_ct_clipped.sddraft"
sd = proj_loc + "TMACOG_Title6_bg_ct_clipped.sd"
sdd = arcpy.mp.CreateWebLayerSDDraft(maup, sddraft, 'New_title_0','MY_HOSTED_SERVICES','FEATURE_ACCESS')
print(arcpy.GetMessages())

arcpy.StageService_server(sddraft, sd)
arcpy.UploadServiceDefinition_server(sd,'My Hosted Services')
print(' Uploaded!')

print('\bDone')'''
print(' Sending Email Notification...')
import smtplib
from email.mime.text import MIMEText
SUBJECT = 'Title6 Script Complete'
FROM = email_id
TO = 'mrfuller460@gmail.com'
msg = MIMEText(f"{str(year_int)} ACS Data now available on Postgres and in {str(base_dir)}")
msg['From'] = FROM
msg['To'] = TO
msg['Subject'] = SUBJECT
with smtplib.SMTP(email_server, email_port) as s:
    s.starttls()
    s.login(email_id,email_password)
    s.send_message(msg)
print('\bDone')
end_time = datetime.now()
elapsed = end_time - start_time
print("Script complete in " + str(elapsed))
