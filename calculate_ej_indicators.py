# print('  Assembling Title6 Stats...'),
def calculate_ej_indicators(dfs, year_int):
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
        try:
            df_t['Mobile Only Household'] = round((df_t['B28001_006E']+df_t['B28001_008E'])/ df_t['B28001_001E']*100,0)
        except:
            print(f'No Mobile Only Household data for {str(year_int)}')
            pass
        try:
            df_t['No Internet Household'] = round(df_t['B28002_013E']/df_t['B28002_001E']*100,0)
        except:
            print(f'No No-Internet Household data for {str(year_int)}')
            pass    
        df_t['geoid_join'] = df_t.GEO_ID.str[9:]
        if year_int < 2017:
            df_t.set_index('NAME',inplace=True)
        else:
            df_t.set_index('GEO_ID', inplace=True)
    # return(dfs)
# print('\bDone')
