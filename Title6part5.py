# -*- coding: utf-8 -*-
"""
Created on Wed Mar 02 14:31:51 2016

@author: fullerm
"""
import arcpy, os
from arcpy import env
from datetime import date
base_dir = "Z:/fullerm/Census Bureau/American Community Survey/2010-14"

arcpy.env.overwriteOutput = True

print('Preparing data in ArcMap...'),

TimeDate=datetime.datetime.now()
TimeDateStr = "Title6"+TimeDate.strftime('%Y%m%d%H%M')  
outputGDB = arcpy.CreateFileGDB_management(base_dir,TimeDateStr)
tractdata= base_dir+'\\Title6_t.csv'
bgdata= base_dir+'\\Title6_b.csv'

cttable = arcpy.TableToTable_conversion(tractdata,outputGDB,"Tract_Data")
bgtable = arcpy.TableToTable_conversion(bgdata,outputGDB,"Block_Group_Data")

#ct = arcpy.MakeFeatureLayer_management("Z:fullerm/Demographics.gdb/tl_2015_tract_TMACOG",os.path.join(base_dir,TimeDateStr+".gdb\ctlayer"))
#bg = arcpy.MakeFeatureLayer_management("Z:fullerm/TMACOG FLOWS HMHS Census.gdb/Block_Group_2010",os.path.join(base_dir,TimeDateStr+".gdb\bglayer"))

ct = "Z:fullerm/Demographics.gdb/tl_2015_tract_TMACOG"
bg = "Z:fullerm/TMACOG FLOWS HMHS Census.gdb/Block_Group_2010"

arcpy.AddField_management(bgtable,"Geocode_STR","TEXT")
arcpy.CalculateField_management(bgtable,"Geocode_STR","str('{:f}'.format(!Geocode!)).rstrip('.0')","PYTHON")

ctjoin = arcpy.JoinField_management(ct,"GEOID",cttable,"Geocode")
bgjoin = arcpy.JoinField_management(bg,"GEOID10",bgtable,"Geocode_STR")

ctout = arcpy.FeatureClassToFeatureClass_conversion(ctjoin,outputGDB,"TMACOG_Title_6_ct")
bgout = arcpy.FeatureClassToFeatureClass_conversion(bgjoin,outputGDB,"TMACOG_Title_6_bg")

print ('\bDone')
