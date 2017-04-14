# -*- coding: utf-8 -*-
"""
Created on Tue Mar 01 15:53:59 2016

@author: fullerm
"""

import pandas
import pandas as pd
import os

#set workspace/directory

workspace = "Z:/fullerm/Census Bureau/American Community Survey/2010-14/Fulton/"
csv_path =workspace + '\\'  + table + '.csv'
df0= pandas.read_csv(os.path.join(workspace,'Title6.csv'))
df1= pandas.read_csv(os.path.join(workspace,'B01001.csv'))
df2= pandas.read_csv(os.path.join(workspace,'B03002.csv'))
df3= pandas.read_csv(os.path.join(workspace,'B16004.csv'))
df4= pandas.read_csv(os.path.join(workspace,'B17017.csv'))
df5= pandas.read_csv(os.path.join(workspace,'B18101.csv'))
df6= pandas.read_csv(os.path.join(workspace,'B25044.csv'))

df0['Geocode']=df1['Geocode']
df0['Name']=df1['NAME']
df0['65 and Over']=df1['65 and Over']
df0['Minority Percentage']=df2['Minority Percentage']
df0['English Less than Very Well']=df3['English Less than Very Well']
df0['Household Poverty Rate']=df4['Household Poverty Rate']
df0['Disability Rate']=df5['Disability Rate'] 
df0['No Car Household Rate']=df6['No Car Household Rate']

df0.to_csv(workspace + '\\Title6.csv')
    