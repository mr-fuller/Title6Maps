# calculate regional rates for each variable, using the more reliable county/subdivision level estimates
import pandas as pd
from census import Census
from variables import api_key, fips,variable_list

# input a list of counties, Lucas, Monroe, and Wood by default
def calculate_regional_rates(counties):
    # flds = ['GEO_ID','NAME'] + variable_list
    # counties = ['Lucas','Ottawa','Monroe','Sandusky','Wood']
    filtered_dict = {county:fips[county] for county in counties}
    c = Census(api_key)
    df = pd.DataFrame()
    for county in filtered_dict:
        if county == 'Monroe':
            temp_df = pd.DataFrame(c.acs5.state_county_subdivision(variable_list, fips[county][:2], fips[county][2:], '*'))
            temp_df = temp_df.loc[temp_df['county subdivision'].isin(['49700',  # Luna Pier
                                                                      '06740',  # Bedford
                                                                      '26320',  # Erie
                                                                      '86740'  # Whiteford
                                                                      ])]
            df = df.append(temp_df, sort=False)
        else:
            temp_df = pd.DataFrame(c.acs5.state_county(variable_list, fips[county][:2], fips[county][2:]))
            df = df.append(temp_df,sort=False)

    total_pop_est = sum(df['B03002_001E'])
    total_hhs_est = sum(df['B25044_001E'])
    total_poc_est = (sum(df['B03002_001E']) - sum(df['B03002_003E']))
    total_pov_est = sum(df['B17021_002E'])
    total_pov_pop_est = sum(df['B17021_001E'])
    total_old_est = sum(df['B01001_020E'] + df['B01001_021E'] + df['B01001_022E'] + df['B01001_023E'] +
                        df['B01001_024E'] + df['B01001_025E'] + df['B01001_044E'] + df['B01001_045E'] +
                        df['B01001_046E'] + df['B01001_047E'] + df['B01001_048E'] + df['B01001_049E'])
    total_disabled_est = sum(
        df['B18101_004E'] + df['B18101_007E'] + df['B18101_010E'] + df['B18101_013E'] + df['B18101_016E'] +
        df['B18101_019E'] + df['B18101_023E'] + df['B18101_026E'] + df['B18101_029E'] + df['B18101_032E'] +
        df['B18101_035E'] + df['B18101_038E'])
    total_nocar_est = sum(df['B25044_003E']) + sum(df['B25044_010E'])
    total_lep_est = sum(df['B16004_001E']) - sum(
        df['B16004_003E'] + df['B16004_005E'] + df['B16004_010E'] + df['B16004_015E'] + df['B16004_020E'] +
        df['B16004_025E'] + df['B16004_027E'] + df['B16004_032E'] + df['B16004_037E'] + df['B16004_042E'] +
        df['B16004_047E'] + df['B16004_049E'] + df['B16004_054E'] + df['B16004_059E'] + df['B16004_064E'])
    total_ej_est = sum(df['B03002_001E'] - df['B03002_003E'] + df['B17001H_002E'])
    
    # median_income = (df['B19013_001E']*df['B03002_001E'])
    pip_poc_pct = total_poc_est / total_pop_est * 100
    pip_pov_pct = total_pov_est / total_pov_pop_est * 100
    pip_old_pct = total_old_est / total_pop_est * 100
    pip_disabled_pct = total_disabled_est / total_pop_est * 100
    pip_nocar_pct = total_nocar_est / total_hhs_est * 100
    pip_lep_pct = total_lep_est / total_pop_est * 100
    ej_pop_pct = round(total_ej_est/total_pop_est*100,0)
    return [pip_poc_pct,  # 0
            pip_pov_pct,  # 1
            pip_old_pct,  # 2
            pip_disabled_pct,  # 3
            pip_nocar_pct,  # 4
            pip_lep_pct,  # 5
            total_pop_est, # 6
            total_hhs_est,  # 7
            total_poc_est, # 8
            total_pov_est, # 9
            total_pov_pop_est, # 10
            total_old_est, # 11
            total_disabled_est, # 12
            total_nocar_est, # 13
            total_lep_est, # 14
            total_ej_est, #15
            ej_pop_pct #16
            ] 
    # dict = {'Environmental Justice Group': ['Regional Count', 'Regional Percent'],
    #         'Minority': [total_poc_est, pip_poc_pct],
    #         'Low Income': [total_pov_est, pip_pov_pct],
    #         'Age 65 and Older': [total_old_est, pip_old_pct],
    #         'Disabled': [total_disabled_est, pip_disabled_pct],
    #         'Zero Car': [total_nocar_est, pip_nocar_pct],
    #         'Limited English Proficiency': [total_lep_est, pip_lep_pct],
    #         'Median Income': ['', 'N/A'],
    #         'Total Population Estimate': [total_pop_est, total_pop_est / total_pop_est * 100],
    #         'Total Households': [total_hhs_est, total_hhs_est / total_hhs_est * 100],
    #         'Population of non-institutionalized civilians': ['', ''],
    #         'Population for Whom Poverty Status is Determined': [total_pov_pop_est,
    #                                                              total_pov_pop_est / total_pov_pop_est * 100]
    #         }
    # df = pd.DataFrame(dict).transpose()
    # df = df.reindex(index=['Environmental Justice Group',
    #                        'Minority',
    #                        'Low Income',
    #                        'Age 65 and Older',
    #                        'Disabled',
    #                        'Zero Car',
    #                        'Limited English Proficiency',
    #                        'Median Income',
    #                        'Total Population Estimate',
    #                        'Total Households',
    #                        'Population of non-institutionalized civilians',
    #                        'Population for Whom Poverty Status is Determined'])
    # print(df)
    # writer = pd.ExcelWriter('C:/Users/fullerm/Desktop/pip_summary_table.xlsx', engine='xlsxwriter')
    # df.to_excel(writer)
