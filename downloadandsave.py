import pandas as pd
import os
from variables import api_key, api_pull


##
# DOWNLOAD ACS DATA
##


def download_and_save_data(acs_dict, fips, location, api_key, api_url_base, base_dir):
    # Since there is a 50 variable maximum we need to see how many calls
    # to the API we need to make to get all the variables.
    api_calls_needed = (len(acs_dict) // 49) + 1
    api_calls_done = 0
    variable_range = 49
    while api_calls_done < api_calls_needed:
        get_string = ''
        print('        API Call Set ' + str(api_calls_done + 1) + ' of ' + str(api_calls_needed))
        variable_range_start = variable_range * api_calls_done
        variable_range_end = variable_range_start + variable_range
        for variable in acs_dict[variable_range_start:variable_range_end]:
            get_string = get_string + ',' + variable

        # Get Census Tract Level Data
        # Pull all Census Tracts in the TMACOG Planning Area
        api_url = api_url_base + get_string + '&for=tract:*&in=state:' + fips[location][:2] + \
                  '+county:' + fips[location][2:] + '&key=' + api_key
        #print(api_url)
        tract_data = pd.io.json.read_json(api_url)
        tract_data.columns = tract_data[:1].values.tolist()  # Rename columns based on first row
        tract_data['Geocode'] = tract_data['state'] + tract_data['county'] + tract_data['tract']
        tract_data = tract_data[1:]  # Drop first row

        # Pull all Block Groups in the TMACOG Planning Area
        api_url = api_url_base + get_string + '&for=block+group:*&in=state:' + fips[location][:2] + '+county:' + fips[
                                                                                                                     location][
                                                                                                                 2:] + '&key=' + api_key
        block_group_data = pd.io.json.read_json(api_url)
        block_group_data.columns = block_group_data[:1].values.tolist()  # Rename columns based on first row
        block_group_data['Geocode'] = block_group_data['state'] + block_group_data['county'] + block_group_data[
            'tract'] + block_group_data['block group']
        block_group_data = block_group_data[1:]  # Drop first row

        # Build long table by append rows
        temp_t = tract_data
        temp_b = block_group_data

        # Add columns if the final data frame is created
        if api_calls_done == 0:
            data_t = temp_t
            data_b = temp_b
        else:
            data_t = pd.concat([data_t, temp_t], axis=1)
            data_b = pd.concat([data_b, temp_b], axis=1)
        api_calls_done += 1

    csv_path_t = base_dir + '\\' + location + '\\Title6_t.csv'
    csv_path_b = base_dir + '\\' + location + '\\Title6_b.csv'

    # Pull out the Geocode and Name
    geocode_t = data_t['Geocode']
    geocode_b = data_b['Geocode']
    print(geocode_t)
    series = type(pd.Series())
    # if type(geocode_t) == 'pandas.core.series.Series':
    if isinstance(geocode_t, series):  # if geocode is a series class, change it to a dataframe class
        geocode_t = pd.DataFrame(geocode_t, columns=['Geocode'],dtype= 'str')
    else:  # otherwise slice it
        geocode_t = geocode_t.iloc[:, 0].astype('str')  # this should return the first column
    print(geocode_t)
    # if type(geocode_b) == 'pandas.core.series.Series':
    if isinstance(geocode_b, series):
        geocode_b = pd.DataFrame(geocode_b, columns=['Geocode'], dtype= 'str')
    else:
        geocode_b = geocode_b.iloc[:, 0].astype('str')  # this should return the first column

    name_t = data_t['NAME']
    name_b = data_b['NAME']
    if isinstance(name_t, series):
        name_t = pd.DataFrame(name_t, columns=['NAME'])
    else:
        name_t = name_t.iloc[:, 0]  # this should return the first column
    if isinstance(name_b, series):
        name_b = pd.DataFrame(name_b, columns=['NAME'])
    else:
        name_b = name_b.iloc[:, 0]  # this should return the first column
    # Drop unneeded columns in they exist
    data_t = data_t.drop(['state', 'county', 'tract'], axis=1)  # Drop the state, county, and tract column
    # data_t = data_t.drop(['county'], axis=1)  # Drop the county column
    # data_t = data_t.drop(['block group'], axis=1)  # Drop the place column
    # data_t = data_t.drop(['tract'], axis=1)  # Drop the county subdivision column

    data_b = data_b.drop(['state', 'county', 'block group', 'tract'], axis=1)  # Drop the state column
    # data_b = data_b.drop(['county'], axis=1)  # Drop the county column
    # data_b = data_b.drop(['block group'], axis=1)  # Drop the place column
    # data_b = data_b.drop(['tract'], axis=1)  # Drop the county subdivision column
    # Drop the location information
    data_t = data_t.drop(['Geocode', 'NAME'], axis=1)
    data_t = data_t.astype(dtype = 'float', na = 0)
    # data_t = data_t.drop(['NAME'], axis=1)
    data_b = data_b.drop(['Geocode', 'NAME'], axis=1)
    data_b = data_b.astype(dtype = 'float', na = 0)
    # data_b = data_b.drop(['NAME'], axis=1)
    # Build data frame with columns in the desired order
    data_t = pd.concat([geocode_t, name_t, data_t], axis=1)
    #data_t.to_csv(csv_path_t, index=False)
    data_b = pd.concat([geocode_b, name_b, data_b], axis=1)
    #data_b.to_csv(csv_path_b, index=False)
    return [data_b,data_t]
    print('      Table ' + location + ' Downloaded and Saved')


'''print('  Downloading tables for')
not_available_via_api = list()  # This will hold the tables we can't get via the API
i = 0
counties_t = pd.DataFrame()
counties_b = pd.DataFrame()
for location in api_pull:
    i += 1
    print('    ' + location + ' (Location ' + str(i) + ' of ' + str(len(api_pull)) + ')')
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
                df_t['65 and Over'] = (df_t['B01001_020E'] + df_t['B01001_021E'] + df_t['B01001_022E'] + df_t[
                    'B01001_023E'] + df_t['B01001_024E'] + df_t['B01001_025E'] + df_t['B01001_044E'] + df_t[
                                           'B01001_045E'] + df_t['B01001_046E'] + df_t['B01001_047E'] + df_t[
                                           'B01001_048E'] + df_t['B01001_049E']) / df_t['B01001_001E'] * 100
                df_t.to_csv(base_dir + '\\' + location + '\\' + table + '_t.csv')
                df2_t['Geocode'] = df_t['Geocode']
                df2_t['Name'] = df_t['NAME']
                df2_t['Total'] = df_t['B01001_001E']
                df2_t['Percent 65 and Over'] = df_t['65 and Over']
                df2_t.to_csv(base_dir + '\\' + location + '\\Title6_t.csv')

                df_b = pandas.read_csv(base_dir + '\\' + location + '\\' + table + '_b.csv')
                df_b['65 and Over'] = (df_b['B01001_020E'] + df_b['B01001_021E'] + df_b['B01001_022E'] + df_b[
                    'B01001_023E'] + df_b['B01001_024E'] + df_b['B01001_025E'] + df_b['B01001_044E'] + df_b[
                                           'B01001_045E'] + df_b['B01001_046E'] + df_b['B01001_047E'] + df_b[
                                           'B01001_048E'] + df_b['B01001_049E']) / df_b['B01001_001E'] * 100
                df_b.to_csv(base_dir + '\\' + location + '\\' + table + '_b.csv')
                df2_b['Geocode'] = df_b['Geocode']
                df2_b['Name'] = df_b['NAME']
                df2_b['Total'] = df_b['B01001_001E']
                df2_b['Percent 65 and Over'] = df_b['65 and Over']
                df2_b.to_csv(base_dir + '\\' + location + '\\Title6_b.csv')

            elif table == 'B03002':
                for frame in [df_t,df_b]:
                    frame = pandas.read_csv(base_dir + '\\' + location + '\\' + table + '_t.csv')
                    frame['Minority Percentage'] = (df_t['B03002_001E'] - df_t['B03002_003E']) / df_t['B03002_001E'] * 100
                df_t = pandas.read_csv(base_dir + '\\' + location + '\\' + table + '_t.csv')
                df_t['Minority Percentage'] = (df_t['B03002_001E'] - df_t['B03002_003E']) / df_t['B03002_001E'] * 100
                df_t.to_csv(base_dir + '\\' + location + '\\' + table + '_t.csv')

                df_b = pandas.read_csv(base_dir + '\\' + location + '\\' + table + '_b.csv')
                df_b['Minority Percentage'] = (df_b['B03002_001E'] - df_b['B03002_003E']) / df_b['B03002_001E'] * 100
                df_b.to_csv(base_dir + '\\' + location + '\\' + table + '_b.csv')

            elif table == 'B16004':
                df_t = pandas.read_csv(base_dir + '\\' + location + '\\' + table + '_t.csv')
                df_t['Percent English Less than Very Well'] = (df_t['B16004_001E'] - (
                            df_t['B16004_003E'] + df_t['B16004_005E'] + df_t['B16004_010E'] + df_t['B16004_015E'] +
                            df_t['B16004_020E'] + df_t['B16004_025E'] + df_t['B16004_027E'] + df_t['B16004_032E'] +
                            df_t['B16004_037E'] + df_t['B16004_042E'] + df_t['B16004_047E'] + df_t['B16004_049E'] +
                            df_t['B16004_054E'] + df_t['B16004_059E'] + df_t['B16004_064E'])) / df_t[
                                                                  'B16004_001E'] * 100
                df_t.to_csv(base_dir + '\\' + location + '\\' + table + '_t.csv')

                df_b = pandas.read_csv(base_dir + '\\' + location + '\\' + table + '_b.csv')
                df_b['Percent English Less than Very Well'] = (df_b['B16004_001E'] - (
                            df_b['B16004_003E'] + df_b['B16004_005E'] + df_b['B16004_010E'] + df_b['B16004_015E'] +
                            df_b['B16004_020E'] + df_b['B16004_025E'] + df_b['B16004_027E'] + df_b['B16004_032E'] +
                            df_b['B16004_037E'] + df_b['B16004_042E'] + df_b['B16004_047E'] + df_b['B16004_049E'] +
                            df_b['B16004_054E'] + df_b['B16004_059E'] + df_b['B16004_064E'])) / df_b[
                                                                  'B16004_001E'] * 100
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
                df_t['Percent with Disability'] = (df_t['B18101_004E'] + df_t['B18101_007E'] + df_t['B18101_010E'] +
                                                   df_t['B18101_013E'] + df_t['B18101_016E'] + df_t['B18101_019E'] +
                                                   df_t['B18101_023E'] + df_t['B18101_026E'] + df_t['B18101_029E'] +
                                                   df_t['B18101_032E'] + df_t['B18101_035E'] + df_t['B18101_038E']) / \
                                                  df_t['B18101_001E'] * 100
                df_t.to_csv(base_dir + '\\' + location + '\\' + table + '_t.csv')
                # df2['Disability Rate']=df['Disability Rate']
                # df2.to_csv(base_dir + '\\' + location + '\\Title6.csv')
                # df_b = pandas.read_csv(base_dir + '\\' + location + '\\' + table + '_b.csv')
                # df_b['Disability Rate']= (df_b['B18101_004E']+df_b['B18101_007E']+df_b['B18101_010E']+df_b['B18101_013E']+df_b['B18101_016E']+df_b['B18101_019E']+df_b['B18101_023E']+df_b['B18101_026E']+df_b['B18101_029E']+df_b['B18101_032E']+df_b['B18101_035E']+df_b['B18101_038E'])/df_b['B18101_001E']*100
                # df_b.to_csv(base_dir + '\\' + location + '\\' + table + '_b.csv')

            elif table == 'B25044':
                df_t = pandas.read_csv(base_dir + '\\' + location + '\\' + table + '_t.csv')
                df_t['No Car Household Percentage'] = (df_t['B25044_003E'] + df_t['B25044_010E']) / df_t[
                    'B25044_001E'] * 100
                df_t.to_csv(base_dir + '\\' + location + '\\' + table + '_t.csv')
                # df2['No Car Household Rate']=df['No Car Household Rate']
                # df2.to_csv(base_dir + '\\' + location + '\\Title6.csv')
                df_b = pandas.read_csv(base_dir + '\\' + location + '\\' + table + '_b.csv')
                df_b['No Car Household Percentage'] = (df_b['B25044_003E'] + df_b['B25044_010E']) / df_b[
                    'B25044_001E'] * 100
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
    df2t = pandas.read_csv(os.path.join(csv_path2,
                                        'B03002_t.csv'))  # df[x]=pandas.read_csv(os.path.join(csv_path2,"'"+variable_list[x]+'_t.csv')
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
    # for file in csv_path2:
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
    df00b = pandas.read_csv(csv_path2 + '\\Title6_b.csv')
    counties_b = counties_b.append(df00b)
    counties_b.to_csv(base_dir + '\\Title6_b.csv')
    print('\bDone')'''

if __name__ == '__main__':
    download_and_save_data()