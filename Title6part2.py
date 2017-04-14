# -*- coding: utf-8 -*-
"""
Created on Mon Feb 29 08:31:40 2016

@author: fullerm
"""
import pandas
import pandas as pd
import os

#set workspace/directory
"Z:/fullerm/Census Bureau/American Community Survey/"
workspace = "Z:/fullerm/Census Bureau/American Community Survey/2010-14/Fulton/"
#os.makedirs(workspace)
#api_pull = dict() # This will hold all the tables needed per county
#api_pull['Fulton'] = [os.path.join(workspace,"/Fulton/B01001.csv"),os.path.join(workspace,"/Fulton/B03002.csv")]
#api_pull['Hancock'] = [os.path.join(workspace,"/Fulton/B01001.csv"),os.path.join(workspace,"/Fulton/B03002.csv")]
#api_pull['Henry'] = [os.path.join(workspace,"/Fulton/B01001.csv"),os.path.join(workspace,"/Fulton/B03002.csv")]
#api_pull['Lucas'] = [os.path.join(workspace,"/Fulton/B01001.csv"),os.path.join(workspace,"/Fulton/B03002.csv")]
#api_pull['Ottawa'] = [os.path.join(workspace,"/Fulton/B01001.csv"),os.path.join(workspace,"/Fulton/B03002.csv")]
#api_pull['Sandusky'] = [os.path.join(workspace,"/Fulton/B01001.csv"),os.path.join(workspace,"/Fulton/B03002.csv")]
#api_pull['Seneca'] = [os.path.join(workspace,"/Fulton/B01001.csv"),os.path.join(workspace,"/Fulton/B03002.csv")]
#api_pull['Wood'] = [os.path.join(workspace,"/Fulton/B01001.csv"),os.path.join(workspace,"/Fulton/B03002.csv")]
#api_pull['Monroe'] = [os.path.join(workspace,"/Fulton/B01001.csv"),os.path.join(workspace,"/Fulton/B03002.csv")]

# This will hold all the COLUMNS needed per TABLE
column_pull = dict()
column_pull['B01001'] = ['NAME','B01001_001E','B01001_020E','B01001_021E','B01001_022E','B01001_023E','B01001_024E','B01001_025E','B01001_044E','B01001_045E','B01001_046E','B01001_047E','B01001_048E','B01001_049E']
column_pull['B03002'] = ['NAME','B03002_001E','B03002_003E']
column_pull['B16004'] = ['NAME','B16004_001E','B16004_003E','B16004_005E','B16004_010E','B16004_015E','B16004_020E','B16004_025E','B16004_027E','B16004_032E','B16004_037E','B16004_042E','B16004_047E','B16004_049E','B16004_054E','B16004_059E','B16004_064E']
column_pull['B17017'] = ['NAME','B17017_001E','B17017_002E']
column_pull['B18101'] = ['NAME','B18101_001E','B18101_004E','B18101_007E','B18101_010E','B18101_013E','B18101_016E','B18101_019E','B18101_023E','B18101_026E','B18101_029E','B18101_032E','B18101_035E','B18101_038E']
column_pull['B25044'] = ['NAME','B25044_001E','B25044_003E','B25044_010E']

table=list()
columns=list()
#newcsv =pandas.DataFrame(table,columns=api_pull[table])
for table in column_pull:
    oldcsv = pandas.DataFrame.from_csv(workspace + table + '.csv')
    #columns=table+columns    
    #newcsv =pandas.DataFrame(table,columns=api_pull[table])    
    #create a list of all the desired columns
    #df=pd.read_csv(workspace + table +'.csv')
    #for columns in api_pull[table]:#cycle through columns
         
        #newcsv[columns]=df.table+'_'+columns
    csv_path =workspace + '\\'  + table + '_new.csv'    
    oldcsv.to_csv(csv_path, columns = column_pull[table])
    df = pd.read_csv(csv_path)
    if table == 'B01001':
        df['65 and Over']= (df['B01001_020E']+df['B01001_021E']+df['B01001_022E']+df['B01001_023E']+df['B01001_024E']+df['B01001_025E']+df['B01001_044E']+df['B01001_045E']+df['B01001_046E']+df['B01001_047E']+df['B01001_048E']+df['B01001_049E'])/df['B01001_001E']*100
        df.to_csv(csv_path )
    elif table == 'B03002':
        df['Minority Percentage']=(df['B03002_001E']-df['B03002_003E'])/df['B03002_001E']*100
        df.to_csv(csv_path )
    elif table == 'B16004':
        df['English Less than Very Well']=(df['B16004_001E']-(df['B16004_003E']+df['B16004_005E']+df['B16004_010E']+df['B16004_015E']+df['B16004_020E']+df['B16004_025E']+df['B16004_027E']+df['B16004_032E']+df['B16004_037E']+df['B16004_042E']+df['B16004_047E']+df['B16004_049E']+df['B16004_054E']+df['B16004_059E']+df['B16004_064E']))/df['B16004_001E']*100
        df.to_csv(csv_path )
    elif table == 'B17017':
        df['Household Poverty Rate']=df['B17017_002E']/df['B17017_001E']*100
        df.to_csv(csv_path )
    elif table == 'B18101':
        df['Disability Rate']= (df['B18101_004E']+df['B18101_007E']+df['B18101_010E']+df['B18101_013E']+df['B18101_016E']+df['B18101_019E']+df['B18101_023E']+df['B18101_026E']+df['B18101_029E']+df['B18101_032E']+df['B18101_035E']+df['B18101_038E'])/df['B18101_001E']*100
        df.to_csv(csv_path )
    elif table == 'B25044':
        df['No Car Household Rate']=(df['B25044_003E']+df['B25044_010E'])/df['B25044_001E']*100 
        df.to_csv(csv_path )
    else: 
        pass        
    