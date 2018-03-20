# scrape the release date of ACS, then test that against current date
# if released, download Title XI related tables and create updated maps

# Download Title 6 data from the ACS
# updated for use in arcgis Pro

import requests
import pandas
import os
import pandas as pd
from variables import year_int,api_pull,api_key,fips
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
    j = 0
    for table in api_pull[location]:
        j += 1
        print('      Table ' + table + '(' + str(j) + ' of ' + str(len(api_pull[location])) + ')')
        api_url_base = 'http://api.census.gov/data/' + str(year_int) + '/acs/acs5?get=NAME'
        if table in table_list:
            download_and_save_data(acs_dict, fips, location, api_key, api_url_base, base_dir, table)
            df2_t = pd.DataFrame() 
            df2_b = pd.DataFrame()

            if table == 'B01001':
                df_t = pandas.read_csv(base_dir + '\\' + location + '\\' + table + '_t.csv')
                df_t['65 and Over'] = (df_t['B01001_020E'] + df_t['B01001_021E'] + df_t['B01001_022E'] + df_t['B01001_023E'] + df_t['B01001_024E'] + df_t['B01001_025E'] + df_t['B01001_044E'] + df_t['B01001_045E'] + df_t['B01001_046E'] + df_t['B01001_047E'] + df_t['B01001_048E'] + df_t['B01001_049E']) / df_t['B01001_001E'] * 100
                df_t.to_csv(base_dir + '\\' + location + '\\' + table + '_t.csv')
                df2_t['Geocode'] = df_t['Geocode']
                df2_t['Name'] = df_t['NAME']
                df2_t['Total'] = df_t['B01001_001E']
                df2_t['Percent 65 and Over'] = df_t['65 and Over']
                df2_t.to_csv(base_dir + '\\' + location + '\\Title6_t.csv')
                
                df_b = pandas.read_csv(base_dir + '\\' + location + '\\' + table + '_b.csv')
                df_b['65 and Over'] = (df_b['B01001_020E'] + df_b['B01001_021E'] + df_b['B01001_022E'] + df_b['B01001_023E'] + df_b['B01001_024E'] + df_b['B01001_025E'] + df_b['B01001_044E'] + df_b['B01001_045E'] + df_b['B01001_046E'] + df_b['B01001_047E'] + df_b['B01001_048E'] + df_b['B01001_049E']) / df_b['B01001_001E'] * 100
                df_b.to_csv(base_dir + '\\' + location + '\\' + table + '_b.csv')
                df2_b['Geocode'] = df_b['Geocode']
                df2_b['Name'] = df_b['NAME']
                df2_b['Total'] = df_b['B01001_001E']
                df2_b['Percent 65 and Over'] = df_b['65 and Over']
                df2_b.to_csv(base_dir + '\\' + location + '\\Title6_b.csv')
                
            elif table == 'B03002':
                '''for frame in [df_t,df_b]:
                    frame = pandas.read_csv(base_dir + '\\' + location + '\\' + table + '_t.csv')
                    frame['Minority Percentage'] = (df_t['B03002_001E'] - df_t['B03002_003E']) / df_t['B03002_001E'] * 100'''
                df_t = pandas.read_csv(base_dir + '\\' + location + '\\' + table + '_t.csv')                
                df_t['Minority Percentage'] = (df_t['B03002_001E'] - df_t['B03002_003E']) / df_t['B03002_001E'] * 100
                df_t.to_csv(base_dir + '\\' + location + '\\' + table + '_t.csv')

                df_b = pandas.read_csv(base_dir + '\\' + location + '\\' + table + '_b.csv')
                df_b['Minority Percentage'] = (df_b['B03002_001E'] - df_b['B03002_003E']) / df_b['B03002_001E'] * 100
                df_b.to_csv(base_dir + '\\' + location + '\\' + table + '_b.csv')
                
            elif table == 'B16004':
                df_t = pandas.read_csv(base_dir + '\\' + location + '\\' + table + '_t.csv')                
                df_t['Percent English Less than Very Well'] = (df_t['B16004_001E'] - (df_t['B16004_003E'] + df_t['B16004_005E'] + df_t['B16004_010E'] + df_t['B16004_015E'] + df_t['B16004_020E'] + df_t['B16004_025E'] + df_t['B16004_027E'] + df_t['B16004_032E'] + df_t['B16004_037E'] + df_t['B16004_042E'] + df_t['B16004_047E'] + df_t['B16004_049E'] + df_t['B16004_054E'] + df_t['B16004_059E'] + df_t['B16004_064E'])) / df_t['B16004_001E'] * 100
                df_t.to_csv(base_dir + '\\' + location + '\\' + table + '_t.csv')

                df_b = pandas.read_csv(base_dir + '\\' + location + '\\' + table + '_b.csv')
                df_b['Percent English Less than Very Well'] = (df_b['B16004_001E'] - (df_b['B16004_003E'] + df_b['B16004_005E'] + df_b['B16004_010E'] + df_b['B16004_015E'] + df_b['B16004_020E'] + df_b['B16004_025E'] + df_b['B16004_027E'] + df_b['B16004_032E'] + df_b['B16004_037E'] + df_b['B16004_042E'] + df_b['B16004_047E'] + df_b['B16004_049E'] + df_b['B16004_054E'] + df_b['B16004_059E'] + df_b['B16004_064E'])) / df_b['B16004_001E'] * 100
                df_b.to_csv(base_dir + '\\' + location + '\\' + table + '_b.csv')
                
            elif table == 'B17017':
                df_t = pandas.read_csv(base_dir + '\\' + location + '\\' + table + '_t.csv')
                df_t['Household Poverty Percentage'] = df_t['B17017_002E'] / df_t['B17017_001E'] * 100
                df_t.to_csv(base_dir + '\\' + location + '\\' + table + '_t.csv')

                df_b = pandas.read_csv(base_dir + '\\' + location + '\\' + table + '_b.csv')
                df_b['Household Poverty Percentage'] = df_b['B17017_002E'] / df_b['B17017_001E'] * 100
                df_b.to_csv(base_dir + '\\' + location + '\\' + table + '_b.csv')
                
            elif table == 'B18101':
                df_t = pandas.read_csv(base_dir + '\\' + location + '\\' + table + '_t.csv')                
                df_t['Percent with Disability'] = (df_t['B18101_004E'] + df_t['B18101_007E'] + df_t['B18101_010E'] + df_t['B18101_013E'] + df_t['B18101_016E'] + df_t['B18101_019E'] + df_t['B18101_023E'] + df_t['B18101_026E'] + df_t['B18101_029E'] + df_t['B18101_032E'] + df_t['B18101_035E'] + df_t['B18101_038E']) / df_t['B18101_001E'] * 100
                df_t.to_csv(base_dir + '\\' + location + '\\' + table + '_t.csv')
                # df2['Disability Rate']=df['Disability Rate']
                # df2.to_csv(base_dir + '\\' + location + '\\Title6.csv')
                # df_b = pandas.read_csv(base_dir + '\\' + location + '\\' + table + '_b.csv')
                # df_b['Disability Rate']= (df_b['B18101_004E']+df_b['B18101_007E']+df_b['B18101_010E']+df_b['B18101_013E']+df_b['B18101_016E']+df_b['B18101_019E']+df_b['B18101_023E']+df_b['B18101_026E']+df_b['B18101_029E']+df_b['B18101_032E']+df_b['B18101_035E']+df_b['B18101_038E'])/df_b['B18101_001E']*100
                # df_b.to_csv(base_dir + '\\' + location + '\\' + table + '_b.csv')

            elif table == 'B25044':
                df_t = pandas.read_csv(base_dir + '\\' + location + '\\' + table + '_t.csv')
                df_t['No Car Household Percentage'] = (df_t['B25044_003E'] + df_t['B25044_010E']) / df_t['B25044_001E'] * 100
                df_t.to_csv(base_dir + '\\' + location + '\\' + table + '_t.csv')
                # df2['No Car Household Rate']=df['No Car Household Rate']
                # df2.to_csv(base_dir + '\\' + location + '\\Title6.csv')
                df_b = pandas.read_csv(base_dir + '\\' + location + '\\' + table + '_b.csv')
                df_b['No Car Household Percentage'] = (df_b['B25044_003E'] + df_b['B25044_010E']) / df_b['B25044_001E'] * 100
                df_b.to_csv(base_dir + '\\' + location + '\\' + table + '_b.csv')

            
            else: 
                pass
                  
            
        else:
            if table not in not_available_via_api:
                not_available_via_api.append(table)
            print('      WARNING: Table ' + table + ' is not available via the API!')
    print('  Assembling Title6 Stats...'), 
    # for census tracts
    csv_path2 = base_dir + '\\' + location 
    df0t = pandas.read_csv(os.path.join(csv_path2, 'Title6_t.csv'))
    df1t = pandas.read_csv(os.path.join(csv_path2, 'B01001_t.csv'))  # for x in range(0,len(api_pull)):
    df2t = pandas.read_csv(os.path.join(csv_path2, 'B03002_t.csv'))  # df[x]=pandas.read_csv(os.path.join(csv_path2,"'"+variable_list[x]+'_t.csv')
    df3t = pandas.read_csv(os.path.join(csv_path2, 'B16004_t.csv'))
    df4t = pandas.read_csv(os.path.join(csv_path2, 'B17017_t.csv'))
    df5t = pandas.read_csv(os.path.join(csv_path2, 'B18101_t.csv'))
    df6t = pandas.read_csv(os.path.join(csv_path2, 'B19013_t.csv'))
    df7t = pandas.read_csv(os.path.join(csv_path2, 'B25044_t.csv'))

    df0t['Geocode'] = df1t['Geocode']
    # df0['Name']=df1['NAME']
    # df0['65 and Over']=df1['65 and Over']
    df0t['Minority Percentage'] = df2t['Minority Percentage']
    df0t['Percent English Less than Very Well'] = df3t['Percent English Less than Very Well']
    df0t['Household Poverty Percentage'] = df4t['Household Poverty Percentage']
    df0t['Percent with Disability'] = df5t['Percent with Disability']
    df0t['Median Household Income'] = df6t['B19013_001E']
    df0t['No Car Household Percentage'] = df7t['No Car Household Percentage']

    df0t.to_csv(csv_path2 + '\\Title6_t.csv')
    # for block groups
    #for file in csv_path2:
     #   for i in range(0,7,1):
      #      df + i + b = pandas.read_csv(os.path.join(csv_path2,file))
    df0b = pandas.read_csv(os.path.join(csv_path2, 'Title6_b.csv'))
    df1b = pandas.read_csv(os.path.join(csv_path2, 'B01001_b.csv'))
    df2b = pandas.read_csv(os.path.join(csv_path2, 'B03002_b.csv'))
    df3b = pandas.read_csv(os.path.join(csv_path2, 'B16004_b.csv'))
    df4b = pandas.read_csv(os.path.join(csv_path2, 'B17017_b.csv'))
    df5b = pandas.read_csv(os.path.join(csv_path2, 'B18101_b.csv'))
    df6b = pandas.read_csv(os.path.join(csv_path2, 'B19013_b.csv'))
    df7b = pandas.read_csv(os.path.join(csv_path2, 'B25044_b.csv'))

    df0b['Geocode'] = df1b['Geocode']
    # df0['Name']=df1['NAME']
    # df0['65 and Over']=df1['65 and Over']
    df0b['Minority Percentage'] = df2b['Minority Percentage']
    df0b['Percent English Less than Very Well'] = df3b['Percent English Less than Very Well']
    df0b['Household Poverty Percentage'] = df4b['Household Poverty Percentage']
    df0b['Median Household Income'] = df6b['B19013_001E']
    df0b['No Car Household Percentage'] = df7b['No Car Household Percentage']

    df0b.to_csv(csv_path2 + '\\Title6_b.csv')
    print('\bDone')
    print('  Appending Title 6 Stats...'),
    # csv_path = base_dir + '\\' + location + '\\Title6.csv'

    df00t = pandas.read_csv(csv_path2 + '\\Title6_t.csv')
    counties_t = counties_t.append(df00t)
    counties_t.to_csv(base_dir + '\\Title6_t.csv')
    # for block groups
    df00b = pandas.read_csv(csv_path2 +'\\Title6_b.csv')
    counties_b = counties_b.append(df00b)
    counties_b.to_csv(base_dir + '\\Title6_b.csv')
    print('\bDone')

spatialize(base_dir)
# This section joins tables to respective geographies

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
