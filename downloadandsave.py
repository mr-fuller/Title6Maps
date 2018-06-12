import pandas as pd
import os
import requests, census
from variables import api_pull, variable_list


##
# DOWNLOAD ACS DATA
##


def download_and_save_data(acs_dict, fips, location, api_key, base_dir):
    c = census.Census(api_key)
    # Since there is a 50 variable maximum we need to see how many calls
    # to the API we need to make to get all the variables.
    # api_calls_needed = (len(acs_dict) // 49) + 1
    # api_calls_done = 0
    # variable_range = 49
    # while api_calls_done < api_calls_needed:
    #     get_string = ''
    #     print('        API Call Set ' + str(api_calls_done + 1) + ' of ' + str(api_calls_needed))
    #     variable_range_start = variable_range * api_calls_done
    #     variable_range_end = variable_range_start + variable_range
    #     for variable in acs_dict[variable_range_start:variable_range_end]:
    #         get_string = get_string + ',' + variable

        # Get Census Tract Level Data
        # Pull all Census Tracts in the TMACOG Planning Area
        # api_url = api_url_base + get_string + '&for=tract:*&in=state:' + fips[location][:2] + \
        #           '+county:' + fips[location][2:] + '&key=' + api_key
        # print(api_url)
        # tract_data = pd.DataFrame(requests.get(api_url).json())
    tract_data = pd.DataFrame()
    block_group_data = pd.DataFrame()
    for county in fips:
        temp_ct_df = pd.DataFrame(c.acs5.state_county_tract(variable_list,fips[county][:2], fips[county][2:],'*'))
        tract_data = tract_data.append(temp_ct_df)
        temp_bg_df = pd.DataFrame(c.acs5.state_county_blockgroup(variable_list,
                                                                   fips[county][:2], fips[county][2:],'*'))
        block_group_data = block_group_data.append(temp_bg_df)
        # tract_data.columns = tract_data[:1].values.tolist()  # Rename columns based on first row
        # tract_data['Geocode'] = tract_data['state'] + tract_data['county'] + tract_data['tract']
        # tract_data = tract_data[1:]  # Drop first row

        # Pull all Block Groups in the TMACOG Planning Area
        # api_url = api_url_base + get_string + '&for=block+group:*&in=state:' + fips[location][:2] + '+county:' + fips[
        #                                                                                                              location][
        #                                                                                                          2:] + '&key=' + api_key
        # block_group_data = pd.DataFrame(requests.get(api_url).json())

        # block_group_data.columns = block_group_data[:1].values.tolist()  # Rename columns based on first row
        # block_group_data['Geocode'] = block_group_data['state'] + block_group_data['county'] + block_group_data[
        #     'tract'] + block_group_data['block group']
        # block_group_data = block_group_data[1:]  # Drop first row

        # Build long table by append rows
        # temp_t = tract_data
        # temp_b = block_group_data

        # Add columns if the final data frame is created
        # if api_calls_done == 0:
        #     data_t = temp_t
        #     data_b = temp_b
        # else:
        #     data_t = pd.concat([data_t, temp_t], axis=1)
        #     data_b = pd.concat([data_b, temp_b], axis=1)
        # api_calls_done += 1
    print(tract_data)
    print(block_group_data)
    csv_path_t = base_dir + '\\' + location + '\\Title6_t.csv'
    csv_path_b = base_dir + '\\' + location + '\\Title6_b.csv'

    # # Pull out the Geocode and Name
    # geocode_t = data_t['Geocode']
    # geocode_b = data_b['Geocode']
    # print(geocode_t)
    # series = type(pd.Series())
    # # if type(geocode_t) == 'pandas.core.series.Series':
    # if isinstance(geocode_t, series):  # if geocode is a series class, change it to a dataframe class
    #     geocode_t = pd.DataFrame(geocode_t, columns=['Geocode'],dtype= 'str')
    # else:  # otherwise slice it
    #     geocode_t = geocode_t.iloc[:, 0].astype('str')  # this should return the first column
    # print(geocode_t)
    # # if type(geocode_b) == 'pandas.core.series.Series':
    # if isinstance(geocode_b, series):
    #     geocode_b = pd.DataFrame(geocode_b, columns=['Geocode'], dtype= 'str')
    # else:
    #     geocode_b = geocode_b.iloc[:, 0].astype('str')  # this should return the first column
    #
    # name_t = data_t['NAME']
    # name_b = data_b['NAME']
    # if isinstance(name_t, series):
    #     name_t = pd.DataFrame(name_t, columns=['NAME'])
    # else:
    #     name_t = name_t.iloc[:, 0]  # this should return the first column
    # if isinstance(name_b, series):
    #     name_b = pd.DataFrame(name_b, columns=['NAME'])
    # else:
    #     name_b = name_b.iloc[:, 0]  # this should return the first column
    # # Drop unneeded columns in they exist
    # data_t = data_t.drop(['state', 'county', 'tract'], axis=1)  # Drop the state, county, and tract column
    # # data_t = data_t.drop(['county'], axis=1)  # Drop the county column
    # # data_t = data_t.drop(['block group'], axis=1)  # Drop the place column
    # # data_t = data_t.drop(['tract'], axis=1)  # Drop the county subdivision column
    #
    # data_b = data_b.drop(['state', 'county', 'block group', 'tract'], axis=1)  # Drop the state column
    # # data_b = data_b.drop(['county'], axis=1)  # Drop the county column
    # # data_b = data_b.drop(['block group'], axis=1)  # Drop the place column
    # # data_b = data_b.drop(['tract'], axis=1)  # Drop the county subdivision column
    # # Drop the location information
    # data_t = data_t.drop(['Geocode', 'NAME'], axis=1)
    tract_data = tract_data.astype(dtype = 'float', na = 0)
    # # data_t = data_t.drop(['NAME'], axis=1)
    # data_b = data_b.drop(['Geocode', 'NAME'], axis=1)
    block_group_data = block_group_data.astype(dtype = 'float', na = 0)
    # # data_b = data_b.drop(['NAME'], axis=1)
    # # Build data frame with columns in the desired order
    # data_t = pd.concat([geocode_t, name_t, data_t], axis=1)
    # #data_t.to_csv(csv_path_t, index=False)
    # data_b = pd.concat([geocode_b, name_b, data_b], axis=1)
    # #data_b.to_csv(csv_path_b, index=False)

    print('      Table ' + location + ' Downloaded and Saved')
    return [block_group_data,tract_data]



if __name__ == '__main__':
    download_and_save_data()