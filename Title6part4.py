# -*- coding: utf-8 -*-
"""
Created on Wed Mar 02 08:43:28 2016

@author: fullerm
"""

import requests, pandas, os
import pandas as pd

disability = 'B18101' #The table number for disability information
esl = 'B16004' #table number for english as a second language
poverty = 'B17017' #table number for poverty stats
race = 'B03002' #table number for race info
elder = 'B01001' #table with age information
noCar ='B25044' #table with info on no-car households

api_pull = dict() # This will hold all the tables needed per county
api_pull['Fulton'] = [disability, esl, poverty, race, elder, noCar]
api_pull['Hancock'] = [disability, esl, poverty, race, elder, noCar]
api_pull['Henry'] = [disability, esl, poverty, race, elder, noCar]
api_pull['Lucas'] = [disability, esl, poverty, race, elder, noCar]
api_pull['Ottawa'] = [disability, esl, poverty, race, elder, noCar]
api_pull['Sandusky'] = [disability, esl, poverty, race, elder, noCar]
api_pull['Seneca'] = [disability, esl, poverty, race, elder, noCar]
api_pull['Wood'] = [disability, esl, poverty, race, elder, noCar]
api_pull['Monroe'] = [disability, esl, poverty, race, elder, noCar]

#def function1(location):
    #pass
    #location = list()
#function1(location)
#location = dict()
base_dir = "Z:/fullerm/Census Bureau/American Community Survey/2010-14"
counties=pd.DataFrame()
for location in api_pull:
    csv_path = base_dir + '\\' + location + '\\Title6.csv'

    df= pandas.read_csv(csv_path)
    counties=counties.append(df)
    counties.to_csv(base_dir+'\\Title6.csv')


