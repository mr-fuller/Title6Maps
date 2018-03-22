# scrape the release date of ACS, then test that against current date
# if released, download Title XI related tables and create updated maps

# Download Title 6 data from the ACS
# updated for use in arcgis Pro

import requests
import pandas
import os
import pandas as pd
from variables import year_int,api_pull,api_key,fips, variable_list, poverty_level
from builddirectory import builddirectory
from buildacsdict import buildacsdict
from downloadandsave import download_and_save_data
from spatialize import spatialize
from datetime import datetime
start_time = datetime.now()


base_dir = builddirectory()

acs_dict = buildacsdict()[0]
table_list = buildacsdict()[1]
##
# DOWNLOAD ACS DATA
##

print('  Downloading tables for')
not_available_via_api = list()  # This will hold the tables we can't get via the API
i = 0
counties_t = pd.DataFrame()
counties_b = pd.DataFrame()
for location in api_pull:
    i += 1
    print('    '+location+' (Location '+str(i)+' of '+str(len(api_pull))+')')
    #j = 0
    #for table in api_pull[location]:
    #j += 1
    #print('      Table (' + str(j) + ' of ' + str(len(api_pull[location])) + ')')
    api_url_base = 'http://api.census.gov/data/' + str(year_int) + '/acs/acs5?get=NAME'
    #if table in table_list:
    dfs = download_and_save_data(variable_list, fips, location, api_key, api_url_base, base_dir)
    df2_t = pd.DataFrame()
    df2_b = pd.DataFrame()

    #if table == 'B01001':
    for df_t in dfs:
        #print(df_t.info())
        #df_t = pandas.read_csv(base_dir + '\\' + location + '\\' + table + geo)
        df_t['Percent 65 and Over'] = (df_t['B01001_020E'] + df_t['B01001_021E'] + df_t['B01001_022E'] +
                                       df_t['B01001_023E'] + df_t['B01001_024E'] + df_t['B01001_025E'] +
                                       df_t['B01001_044E'] + df_t['B01001_045E'] + df_t['B01001_046E'] +
                                       df_t['B01001_047E'] + df_t['B01001_048E'] + df_t['B01001_049E']) / df_t['B01001_001E'] * 100

        df_t['Minority Percentage'] = (df_t['B03002_001E'] - df_t['B03002_003E']) / df_t['B03002_001E'] * 100

        df_t['Percent English Less than Very Well'] = (df_t['B16004_001E'] - (df_t['B16004_003E'] + df_t['B16004_005E'] +
                                                                              df_t['B16004_010E'] + df_t['B16004_015E'] +
                                                                              df_t['B16004_020E'] + df_t['B16004_025E'] +
                                                                              df_t['B16004_027E'] + df_t['B16004_032E'] +
                                                                              df_t['B16004_037E'] + df_t['B16004_042E'] +
                                                                              df_t['B16004_047E'] + df_t['B16004_049E'] +
                                                                              df_t['B16004_054E'] + df_t['B16004_059E'] +
                                                                              df_t['B16004_064E'])) / df_t['B16004_001E'] * 100

        df_t['Household Poverty Percentage'] = df_t['B17017_002E'] / df_t['B17017_001E'] * 100

        df_t['Percent with Disability'] = (df_t['B18101_004E'] + df_t['B18101_007E'] + df_t['B18101_010E'] +
                                           df_t['B18101_013E'] + df_t['B18101_016E'] + df_t['B18101_019E'] +
                                           df_t['B18101_023E'] + df_t['B18101_026E'] + df_t['B18101_029E'] +
                                           df_t['B18101_032E'] + df_t['B18101_035E'] + df_t['B18101_038E']) / df_t['B18101_001E'] * 100

        df_t['No Car Household Percentage'] = (df_t['B25044_003E'] + df_t['B25044_010E']) / df_t['B25044_001E'] * 100

    print('  Assembling Title6 Stats...'), 
    # for census tracts

    csv_path2 = base_dir + '\\' + location
    #dfs[1].to_csv(os.path.join(csv_path2, 'Title6_t.csv'))

    # for block groups
    #dfs[0].to_csv(os.path.join(csv_path2,'Title6_b.csv'))
    #for file in csv_path2:
     #   for i in range(0,7,1):
      #      df + i + b = pandas.read_csv(os.path.join(csv_path2,file))

    print('\bDone')
    print('  Appending Title 6 Stats...'),
    # csv_path = base_dir + '\\' + location + '\\Title6.csv'

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
counties_b['ej'] = 'neither'
print(counties_b)

#filter to planning area to calculate the averages

lw_filter = counties_b['Geocode'].str[:5].isin(['39095','39173'])
m_filter = counties_b['Geocode'].str[:8] == '26115833'

lmw_b = counties_b.loc[lw_filter | m_filter,['B03002_001E','B03002_003E']]
overall_poc = (sum(lmw_b['B03002_001E']) - sum(lmw_b['B03002_003E'])) / sum(lmw_b['B03002_001E']) * 100
print(overall_poc)

low_income = counties_b['B19013_001E'] < poverty_level
poc = counties_b['Minority Percentage'] > overall_poc
counties_b.loc[low_income,'ej'] = 'low income'
counties_b.loc[poc,'ej'] = 'people of color'
counties_b.loc[low_income & poc, 'ej'] = 'both'
counties_b.to_csv(base_dir + '\\Title6_b.csv')

# This section joins tables to respective geographies
spatialize(base_dir)

# manipulate layers to display data

# export to pdf
print('\bDone')
print('All data is now stored on the Z drive!')
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

print('\bDone')

import smtplib
from email.mime.text import MIMEText
SUBJECT = 'Title6 Script Complete'
FROM = 'mikerfuller@live.com'
TO = 'fuller@tmacog.org'
msg = MIMEText(str(year_int-1)+ " ACS Data now available on the Z Drive and ArcGIS Online")
msg['From'] = FROM
msg['To'] = TO
msg['Subject'] = SUBJECT
with smtplib.SMTP('smtp-mail.outlook.com',587) as s:
    s.starttls()
    s.login('mikerfuller@live.com','zkecjvqtvcplzysx')
    s.send_message(msg)
'''
end_time = datetime.now()
elapsed = end_time - start_time
print("Script complete in " + str(elapsed))
