# Calculate summary/overall stats for Public Involvement Process document updates
# the study area includes Lucas, Wood, Ottawa, and Sandusky counties as well as the
# southern portion of Monroe county
import pandas as pd
from calculate_regional_rates import calculate_regional_rates
#from variables import poverty_level
from collections import namedtuple
from sqlalchemy import create_engine
import os
from variables import pg_password,pg_username

def summarize_region(counties_b, counties_t, base_dir, year_int,poverty_level):
    # engine = create_engine("postgresql://postgres:" + os.getenv('postgres_password') + "@localhost/title6")
    engine = create_engine(f"postgresql://{pg_username}:{pg_password}@localhost/title6")
    geotuple = namedtuple('geotuple',['b','t'])
    dfs = geotuple(counties_b,counties_t)
    counties = ['Lucas', 'Monroe', 'Wood']
    writer = pd.ExcelWriter(base_dir + '\\' + 'summary_table' + str(year_int) + '.xlsx', engine='xlsxwriter')
    for doc, study_area in {'pip': counties +['Ottawa', 'Sandusky'], 'tip': counties}.items():
        region_rates = calculate_regional_rates(study_area)
        # determine ej status for TIP and PIP study areas in the same data set
        for fld in dfs._fields:
            item = getattr(dfs,fld)
            item[doc +'_ej'] = 'neither'
            # income has to be greater than zero to catch bad data
            low_income = item['B19013_001E'] < poverty_level
            income = item['B19013_001E'] > 0
            no_income = item['B19013_001E'] < 0

            poc = item['Minority Percentage'] > region_rates[8]
            item.loc[low_income & income,doc + '_ej'] = 'low income'
            item.loc[no_income, doc + '_ej'] = 'no data'
            item.loc[poc,doc + '_ej'] = 'people of color'
            item.loc[low_income & income & poc, doc + '_ej'] = 'both'
            # print(item)
            item.to_csv(base_dir + '\\Title6_' + fld + '.csv')
            item.to_sql("title6_"+ fld +"_" + str(year_int), engine,if_exists='replace')
        # but the summary table only needs to happen at the document level
        dict = {'Environmental Justice Group':['Regional Count','Regional Percent'],
                'Minority':[region_rates[8],region_rates[0]],
                'Low Income':[region_rates[9],region_rates[1]],
                'Age 65 and Older':[region_rates[11],region_rates[2]],
                'Disabled':[region_rates[12],region_rates[3]],
                'Zero Car':[region_rates[13],region_rates[4]],
                'Limited English Proficiency':[region_rates[14],region_rates[5]],
                'Median Income':['','N/A'],
                'Total Population Estimate':[region_rates[6],region_rates[6]/region_rates[6]*100],
                'Total Households':[region_rates[7],region_rates[7]/region_rates[7]*100],
                'Population of non-institutionalized civilians':['',''],
                'Population for Whom Poverty Status is Determined':[region_rates[10],region_rates[10]/region_rates[10]*100]
                }
        df = pd.DataFrame(dict).transpose()
        df = df.reindex(index=['Environmental Justice Group',
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
        # print(df)
        # does it make sense to create separate spreadsheets for each document?

        df.to_excel(writer,doc)
    writer.save()
    writer.close()


if __name__ == "__main__":
    summarize_region()
