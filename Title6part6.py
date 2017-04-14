# -*- coding: utf-8 -*-
"""
Created on Fri Mar 04 15:42:59 2016

@author: fullerm
"""
import arcpy
bg_data= #feature class with block group data from previous part of script
ct_data= #feature class with tract data from previous part of script
workspace = "Z:/GIS Data/Ohio/Census/Janet Demographic Data/Maps"
#open existing ArcMap Documents and add data
mxdej = arcpy.mapping.MapDocument(workspace +"\\EJ Areas.mxd")
arcpy.mapping.AddLayer("Layers",bg_data, "TOP")

mxdold = arcpy.mapping.MapDocument(workspace +"\\Elderly Population.mxd")
arcpy.mapping.AddLayer("Layers",bg_data, "TOP")

mxdable = arcpy.mapping.MapDocument(workspace +"\\Disabled Population.mxd")
arcpy.mapping.AddLayer("Layers",ct_data, "TOP")

mxdlep = arcpy.mapping.MapDocument(workspace +"\\Limited English Proficiency_Edits.mxd")
arcpy.mapping.AddLayer("Layers",bg_data, "TOP")

mxdcar = arcpy.mapping.MapDocument(workspace +"\\No Vehicle Households.mxd")
arcpy.mapping.AddLayer("Layers",bg_data, "TOP")
#manipulate layers to display data

#export to pdf