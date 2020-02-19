#calculate/estimate the ej population percentage for Lucas and Wood Counties (TIP related)
import pandas as pd
from census import Census
from variables import api_key, fips,variable_list

# input a list of counties, Lucas, Monroe, and Wood by default
def luc_woo_ej_pop_pct(counties):
    # flds = ['GEO_ID','NAME'] + variable_list
    # counties = ['Lucas','Ottawa','Monroe','Sandusky','Wood']
    filtered_dict = {county:fips[county] for county in counties}
    c = Census(api_key)
    df = pd.DataFrame()
    for county in filtered_dict:
        temp_df = pd.DataFrame(c.acs5.state_county(variable_list, fips[county][:2], fips[county][2:]))
        df = df.append(temp_df,sort=False)
    total_pop_est = sum(df['B03002_001E'])
    tot_ej_pop = sum(df['B03002_001E'] - df['B03002_003E'] + df['B17001H_002E'])
    ej_pop_pct = round(tot_ej_pop/total_pop_est*100,0)
    return ej_pop_pct