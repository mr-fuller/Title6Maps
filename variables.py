from datetime import datetime
import json
#def variables():

year_int = datetime.now().year
#year_int = 2017
with open('/media/mike/OS/Users/fullerm/OneDrive/Documents/Work Computer Files/PycharmProjects/Title6Maps/credentials.json') as creds:
    credentials = json.load(creds)
pg_username = credentials['pg_username']
pg_password = credentials['pg_password']
email_id = credentials['email_id']
email_password = credentials['email_password']
email_server = credentials['email_server']
email_port = credentials['email_port']
api_key = credentials['api_key']

fips = {
    'Fulton': '39051',
    'Hancock': '39063',
    'Henry': '39069',
    'Huron': '39077',
    'Lucas': '39095',
    'Ottawa': '39123',
    'Putnam': '39137',
    'Sandusky': '39143',
    'Seneca': '39147',
    'Wood': '39173',
    'Lenawee': '26091',
    'Monroe': '26115'
}

variable_list = [#'B18101',  # The table number for disability information
                 #'B16004',  # table number for english as a second language
                 #'B17017',  # table number for poverty stats
                 #'B03002',  # table number for race info
                 #'B01001',  # table with age information
                 #'B25044',  # table with info on no-car households
                 #'B19013'   # table with median income estimates
                 
                 'GEO_ID','NAME',
                 #no car households
                 'B25044_003E','B25044_010E','B25044_001E',
                 #median income
                 'B19013_001E',
                 # median age
                 'B01002_001E',
                 # no computer households or mobile only households
                 'B28001_001E',  # total households
                 'B28001_006E',  # smart phone only
                 'B28001_008E',  # tablet only
                 'B28001_011E',  # no computers
                 # household internet access
                 'B28002_001E',  # total households
                 'B28002_013E',  # no internet access
                 #disability
                 'B18101_004E','B18101_007E','B18101_010E','B18101_013E',
                 'B18101_016E','B18101_019E','B18101_023E','B18101_026E',
                 'B18101_029E','B18101_032E','B18101_035E','B18101_038E','B18101_001E',
                 #poverty
                 'B17017_002E','B17017_001E','B17021_001E','B17021_002E',
                 'B17001H_002E', #poverty status (count) of persons white alone, non-hispanic
                 #esl
                 'B16004_001E','B16004_003E','B16004_005E','B16004_010E',
                 'B16004_015E','B16004_020E','B16004_025E','B16004_027E',
                 'B16004_032E','B16004_037E','B16004_042E','B16004_047E',
                 'B16004_049E','B16004_054E','B16004_059E','B16004_064E',
                 #race
                 'B03002_001E',  # total
                 'B03002_003E',  # white, non-hispanic
                 # over 65
                 'B01001_020E','B01001_021E','B01001_022E',
                 'B01001_023E','B01001_024E','B01001_025E',
                 'B01001_044E','B01001_045E','B01001_046E',
                 'B01001_047E','B01001_048E','B01001_049E',
                 'B01001_001E'  # total population estimate
                 ]
#over 65 variables; is this an improvement over hard coding variables?
# for i in range(20,26):
#     variable_list.append(f"B01001_0{str(i).zfill(2)}E")

# for i in range(44,50):
#     variable_list.append(f"B01001_0{str(i).zfill(2)}E")

counties = ['Fulton', 'Hancock', 'Henry','Huron', 'Lucas', 'Ottawa', 'Putnam', 'Sandusky', 'Seneca', 'Wood', 'Lenawee','Monroe']
api_pull = {}
for x in range(0, len(counties)):
    api_pull[counties[x]] = variable_list

# print(api_pull)

#if __name__ == '__main__':
    #variables()
