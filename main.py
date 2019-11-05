# scrape the release date of ACS, then test that against current date
# if released, download Title XI related tables and create updated maps

# Download Title 6 data from the ACS
# updated for use in arcgis Pro

import requests
import pandas
import os
import pandas as pd
from variables import year_int,api_pull,api_key,fips, variable_list, email_id, email_password, email_server, email_port
from builddirectory import builddirectory
# from buildacsdict import buildacsdict
from downloadandsave import download_and_save_data
# from spatialize import spatialize
from pip_summary import summarize_region


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

print('  Downloading tables for')
not_available_via_api = list()  # This will hold the tables we can't get via the API
# eliminate/skip variables not available in api for that year
for i in variable_list[:]:
    if i not in response.json():
        not_available_via_api.append(i)
        variable_list.remove(i)
i = 0
counties_t = pd.DataFrame()
counties_b = pd.DataFrame()

dfs = download_and_save_data(variable_list, fips, api_key, year_int)

print('  Assembling Title6 Stats...'),
for df_t in dfs:
    # print(df_t)
    #df_t = pandas.read_csv(base_dir + '\\' + location + '\\' + table + geo)
    df_t['Percent 65 and Over'] = round((df_t['B01001_020E'] + df_t['B01001_021E'] + df_t['B01001_022E'] +
                                   df_t['B01001_023E'] + df_t['B01001_024E'] + df_t['B01001_025E'] +
                                   df_t['B01001_044E'] + df_t['B01001_045E'] + df_t['B01001_046E'] +
                                   df_t['B01001_047E'] + df_t['B01001_048E'] + df_t['B01001_049E']) / df_t['B01001_001E'] * 100,0)

    df_t['Minority Percentage'] = round((df_t['B03002_001E'] - df_t['B03002_003E']) / df_t['B03002_001E'] * 100,0)

    df_t['Percent English Less than Very Well'] = round((df_t['B16004_001E'] - (df_t['B16004_003E'] + df_t['B16004_005E'] +
                                                                          df_t['B16004_010E'] + df_t['B16004_015E'] +
                                                                          df_t['B16004_020E'] + df_t['B16004_025E'] +
                                                                          df_t['B16004_027E'] + df_t['B16004_032E'] +
                                                                          df_t['B16004_037E'] + df_t['B16004_042E'] +
                                                                          df_t['B16004_047E'] + df_t['B16004_049E'] +
                                                                          df_t['B16004_054E'] + df_t['B16004_059E'] +
                                                                          df_t['B16004_064E'])) / df_t['B16004_001E'] * 100,0)

    df_t['Household Poverty Percentage'] = round(df_t['B17017_002E'] / df_t['B17017_001E'] * 100,0)
    df_t['Individual Poverty Percentage'] = round(df_t['B17021_002E'] / df_t['B17021_001E'] * 100,0)

    df_t['Percent with Disability'] = round((df_t['B18101_004E'] + df_t['B18101_007E'] + df_t['B18101_010E'] +
                                       df_t['B18101_013E'] + df_t['B18101_016E'] + df_t['B18101_019E'] +
                                       df_t['B18101_023E'] + df_t['B18101_026E'] + df_t['B18101_029E'] +
                                       df_t['B18101_032E'] + df_t['B18101_035E'] + df_t['B18101_038E']) / df_t['B18101_001E'] * 100,0)

    df_t['No Car Household Percentage'] = round((df_t['B25044_003E'] + df_t['B25044_010E']) / df_t['B25044_001E'] * 100,0)
    df_t['Median Age'] = df_t['B01002_001E']
    df_t['Mobile Only Household'] = round((df_t['B28001_006E']+df_t['B28001_008E'])/ df_t['B28001_001E']*100,0)
    df_t['No Internet Household'] = round(df_t['B28002_013E']/df_t['B28002_001E']*100,0)
    df_t['geoid_join'] = df_t.GEO_ID.str[9:]
    df_t.set_index('NAME',inplace=True)

print('\bDone')
print('  Appending Title 6 Stats...'),
# csv_path = base_dir + '\\' + location + '\\Title6.csv'

## I can consolidate lines 115-122 to a couple lines in the for loop if I use df.name or namedtuple

df00t = dfs[1] #pandas.read_csv(csv_path2 + '\\Title6_t.csv')
counties_t = counties_t.append(df00t)
counties_t.to_csv(base_dir + '\\Title6_t.csv')
# for block groups
df00b = dfs[0] #pandas.read_csv(csv_path2 +'\\Title6_b.csv')
counties_b = counties_b.append(df00b)
counties_b.to_csv(base_dir + '\\Title6_b.csv')
print('\bDone')

# Determine EJ status of block groups
print(' Determining EJ Areas ... ')

summarize_region(counties_b,counties_t,base_dir, year_int,poverty_level)
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
msg = MIMEText(str(year_int) + " ACS Data now available on Postgres and in " + base_dir)
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
