import requests



def buildacsdict(year_int):

    ##
    # PULLING THE VARIABLE LIST FROM API
    ##

    # Now that we know what year of data the user wants we need to pull the
    # variable list.

    print('  Pulling JSON variable list...'),

    # Build the API URL
    variables_url = 'https://api.census.gov/data/' + str(year_int) + '/acs/acs5/variables.json'
    # Read in the data
    data = requests.get(url=variables_url)
    # Check to make sure we could pull variables
    # while data.status_code == 404:
    #
    #     print('\bNo data for ' + str(year_int) + '. Trying previous year')
    #     year_int= year_int - 1
    #     # Build the API URL
    #     variables_url = 'https://api.census.gov/data/' + str(year_int) + '/acs/acs5/variables.json'
    #     # Read in the data
    #     data = requests.get(url=variables_url)
    #     # import sys
    #
    #     # sys.exit('You entered an invalid ACS year.  Please try again.')
    # else:
    data = data.json()
    print('\bDone retrieving data for ' + str(year_int))

    ##
    # BUILDING ACS TABLE VARIABLE LIST DICTIONARY
    ##

    # We now will iterate through the data and build a dictionary that has all
    # the variables associated with the table.

    print('  Building table list...'),
    table_list = list()  # This will hold all the tables. also, []
    acs_dict = dict()  # This will hold the variables by table. also, {}
    # Iterate through the variables
    for variable in data['variables']:
        s = variable.split('_')  # Break the string apart by the underscore.
        table = s[0]  # This is the table name.

        if not table in table_list:
            table_list.append(table)  # Add it to the table list
            var_list = list()  # Create an empty list for the acs_dict
            var_list.append(variable)  # Put the variable name in the list
            acs_dict[table] = var_list  # Add the variable list to the dictionary
        else:
            var_list = acs_dict[table]  # Pull the existing variable list
            var_list.append(variable)  # Add in the new variable
            var_list.sort()  # Sort it (so the estimates are followed by the MOE)
            acs_dict[table] = var_list  # Replace the list with the updated one
    print('\bDone')
    return [acs_dict, table_list]
    # Now that this has been complete we can call acs_dict['B10001'] to get all
    # the variables in the table

if __name__ == '__main__':
    buildacsdict()
