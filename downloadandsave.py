import pandas as pd
from census import Census
from variables import api_pull, variable_list, year_int


##
# DOWNLOAD ACS DATA
##


def download_and_save_data(acs_dict, fips,  api_key, year_int):
    c = Census(api_key)
    # Since there is a 50 variable maximum we need to see how many calls
    # to the API we need to make to get all the variables.
    tract_data = pd.DataFrame()
    block_group_data = pd.DataFrame()
    i=0
    for county in fips:
        i += 1
        print('    ' + county + ' (Location ' + str(i) + ' of ' + str(len(fips)) + ')')
        
        temp_ct_df = pd.DataFrame(c.acs5.state_county_tract(acs_dict,fips[county][:2], fips[county][2:],'*', year = year_int))
        tract_data = tract_data.append(temp_ct_df)
        temp_bg_df = pd.DataFrame(c.acs5.state_county_blockgroup(acs_dict, fips[county][:2], fips[county][2:],'*', year = year_int))
        block_group_data = block_group_data.append(temp_bg_df)
        print('      Table ' + str(i) + ' Downloaded and Saved')
    # print(tract_data)
    # print(block_group_data)
    # csv_path_t = base_dir + '\\' + location + '\\Title6_t.csv'
    # csv_path_b = base_dir + '\\' + location + '\\Title6_b.csv'
    slice_index = ['GEO_ID']
    if year_int < 2017:
        slice_index.append('NAME')
    else:
        pass 
    
    tract_data = pd.concat([tract_data[slice_index],tract_data.drop(slice_index, axis=1).astype(dtype = 'float')],axis=1)
    # tract_data['geoid_join'] = tract_data['GEO_ID'][9:]
    block_group_data = pd.concat([block_group_data[slice_index], block_group_data.drop(slice_index, axis=1).astype(dtype = 'float')], axis=1)
    # block_group_data['geoid_join'] = block_group_data['GEO_ID'][9:]

    return [block_group_data,tract_data]


if __name__ == '__main__':
    download_and_save_data()