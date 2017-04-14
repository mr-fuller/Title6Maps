from datetime import datetime

fips = {
    'Fulton':'39051',
    'Hancock':'39063',
    'Henry':'39069',
    'Lucas':'39095',
    'Ottawa':'39123',
    'Sandusky':'39143',
    'Seneca':'39147',
    'Wood':'39173',
    'Monroe':'26115'
}
#state_fips['TN']='47'

county_fips = {#what if I just combined county and state into one five digit code, then called fips[:1] or fips[2:]
    'Fulton':'051',
    'Hancock':'063',
    'Henry':'069',
    'Lucas':'095',
    'Ottawa':'123',
    'Sandusky':'143',
    'Seneca':'147',
    'Wood':'173',
    'Monroe':'115'
}
variable_list = ['B18101',#The table number for disability information
                 'B16004',#table number for english as a second language
                 'B17017',#table number for poverty stats
                 'B03002',#table number for race info
                 'B01001',#table with age information
                 'B25044'#table with info on no-car households
                 'B19013' # table with median income estimates
                 ]
#disability = 'B18101'
#esl = 'B16004'
#poverty = 'B17017'
#race = 'B03002'
#elder = 'B01001'
#noCar ='B25044'


counties = ['Fulton','Hancock','Henry','Lucas','Ottawa','Sandusky','Seneca','Wood','Monroe']
api_pull = dict()
for x in range(0,len(counties)):
    api_pull[counties[x]]=variable_list

print(api_pull)
#state fips codes
for loc in counties:
    print(loc, fips[loc][:2])
# county fips codes
for loc in counties:
    print(loc, fips[loc][2:])

year = datetime.now()

print(type(year.year))
print(year.year-1)