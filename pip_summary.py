# Calculate summary/overall stats for Public Involvement Process document updates
import pandas as pd

def pip_summary(counties_b):
    losw_filter = counties_b['Geocode'].str[:5].isin(['39095','39123','39143','39173'])
    m_filter = counties_b['Geocode'].str[:8] == '26115833'

    lmosw_b = counties_b.loc[losw_filter | m_filter,]

    total_pop_est = sum(lmosw_b['B03002_001E'])
    total_hhs_est = sum(lmosw_b['B25044_001E'])
    total_poc_est = (sum(lmosw_b['B03002_001E']) - sum(lmosw_b['B03002_003E']))
    total_pov_est = sum(lmosw_b['B17001_002E'])
    total_pov_pop_est = sum(lmosw_b['B17001_001E'])
    total_old_est = sum(lmosw_b['B01001_020E']+lmosw_b['B01001_021E']+lmosw_b['B01001_022E']+
                 lmosw_b['B01001_023E']+lmosw_b['B01001_024E']+lmosw_b['B01001_025E']+
                 lmosw_b['B01001_044E']+lmosw_b['B01001_045E']+lmosw_b['B01001_046E']+
                 lmosw_b['B01001_047E']+lmosw_b['B01001_048E']+lmosw_b['B01001_049E'])
    total_disabled_est = sum(lmosw_b['B18101_004E']+lmosw_b['B18101_007E']+lmosw_b['B18101_010E']+lmosw_b['B18101_013E']+
                 lmosw_b['B18101_016E']+lmosw_b['B18101_019E']+lmosw_b['B18101_023E']+lmosw_b['B18101_026E']+
                 lmosw_b['B18101_029E']+lmosw_b['B18101_032E']+lmosw_b['B18101_035E']+lmosw_b['B18101_038E'])
    total_nocar_est = sum(lmosw_b['B25044_003E']) + sum(lmosw_b['B25044_010E'])
    total_lep_est = sum(lmosw_b['B16004_001E'])-sum(lmosw_b['B16004_003E']+lmosw_b['B16004_005E']+lmosw_b['B16004_010E']+
                 lmosw_b['B16004_015E']+lmosw_b['B16004_020E']+lmosw_b['B16004_025E']+lmosw_b['B16004_027E']+
                 lmosw_b['B16004_032E']+lmosw_b['B16004_037E']+lmosw_b['B16004_042E']+lmosw_b['B16004_047E']+
                 lmosw_b['B16004_049E']+lmosw_b['B16004_054E']+lmosw_b['B16004_059E']+lmosw_b['B16004_064E'])
    # median_income = (lmosw_b['B19013_001E']*lmosw_b['B03002_001E'])
    dict = {'Environmental Justice Group':['Regional Count','Regional Percent'],
            'Minority':[total_poc_est,total_poc_est/total_pop_est*100],
            'Low Income':[total_pov_est,total_pov_est/total_pov_pop_est*100],
            'Age 65 and Older':[total_old_est,total_old_est/total_pop_est*100],
            'Disabled':[total_disabled_est,total_disabled_est/total_pop_est*100],
            'Zero Car':[total_nocar_est,total_nocar_est/total_hhs_est*100],
            'Limited English Proficiency':[total_lep_est,total_lep_est/total_pop_est*100],
            'Median Income':['','N/A'],
            'Total Population Estimate':[total_pop_est,total_pop_est/total_pop_est*100],
            'Total Households':[total_hhs_est,total_hhs_est/total_hhs_est*100],
            'Population of non-institutionalized civilians':['',''],
            'Population for Whom Poverty Status is Determined':[total_pov_pop_est,total_pov_pop_est/total_pov_pop_est*100]
            }
    df = pd.DataFrame(dict).transpose()
    df=df.reindex(index=['Environmental Justice Group',
            'Minority',
            'Low Income',
            'Age 65 and Older',
            'Disabled',
            'Zero Car',
            'Limited English Proficiency',
            'Median Income',
            'Total Population Estimate',
            'Total Households',
            'Population of non-institutionalized civilians',
            'Population for Whom Poverty Status is Determined'])
    print(df)
    writer = pd.ExcelWriter('C:/Users/fullerm/Desktop/pip_summary_table.xlsx',engine='xlsxwriter')
    df.to_excel(writer)
    # overall_poc =  total_poc_est/ sum(lmosw_b['B03002_001E']) * 100
    # print(overall_poc)
    # income has to be greater than zero to catch bad data
    # low_income = counties_b['B19013_001E'] < poverty_level
    # income = counties_b['B19013_001E'] > 0
    # no_income = counties_b['B19013_001E'] < 0
    #
    # poc = counties_b['Minority Percentage'] > overall_poc
    # counties_b.loc[low_income & income,'ej'] = 'low income'
    # counties_b.loc[no_income, 'ej'] = 'no data'
    # counties_b.loc[poc,'ej'] = 'people of color'
    # counties_b.loc[low_income & income & poc, 'ej'] = 'both'

if __name__ == "__main__":
    pip_summary()
