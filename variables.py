from datetime import datetime
#def variables():
api_key = 'b7da053b9e664586b9e559dba9e73780602f0aab'  # CGR's API key
year_int = datetime.now().year - 2
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

variable_list = ['B18101',  # The table number for disability information
                 'B16004',  # table number for english as a second language
                 'B17017',  # table number for poverty stats
                 'B03002',  # table number for race info
                 'B01001',  # table with age information
                 'B25044',  # table with info on no-car households
                 'B19013'   # table with median income estimates
                 ]


counties = ['Fulton', 'Hancock', 'Henry','Huron', 'Lucas', 'Ottawa', 'Putnam', 'Sandusky', 'Seneca', 'Wood', 'Lenawee','Monroe']
api_pull = {}
for x in range(0, len(counties)):
    api_pull[counties[x]] = variable_list

print(api_pull)

#if __name__ == '__main__':
    #variables()