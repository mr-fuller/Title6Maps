# This section joins tables to respective geographies
import arcpy
from datetime import datetime

# , os
# from arcpy import env
# from datetime import date
# base_dir = "Z:/fullerm/Census Bureau/American Community Survey/2010-14"

def spatialize(base_dir,):

    arcpy.env.overwriteOutput = True

    print('  Preparing data in ArcMap...'),

    TimeDate = datetime.now()
    TimeDateStr = "Title6" + TimeDate.strftime('%Y%m%d%H%M')
    outputGDB = arcpy.CreateFileGDB_management(base_dir,TimeDateStr + ".gdb")
    arcpy.env.workspace = base_dir
    tractdata = base_dir + '\\Title6_t.csv'
    bgdata = base_dir + '\\Title6_b.csv'

    cttable = arcpy.TableToTable_conversion(tractdata,outputGDB,"Tract_Data")
    bgtable = arcpy.TableToTable_conversion(bgdata,outputGDB,"Block_Group_Data")

    mi_gdb = "Z:/fullerm/GIS_Data/MI/tlgdb_2015_a_26_mi.gdb/"
    mi_ct = arcpy.FeatureClassToFeatureClass_conversion(mi_gdb + "Census_Tract", outputGDB, "MI_Census_Tract")

    mi_bg = arcpy.FeatureClassToFeatureClass_conversion(mi_gdb + "Block_Group", outputGDB, "MI_Block_Group")
    oh_gdb = "Z:/fullerm/GIS_Data/OH/tlgdb_2015_a_39_oh.gdb/"
    oh_ct = arcpy.FeatureClassToFeatureClass_conversion(oh_gdb + "Census_Tract", outputGDB, "OH_Census_Tract")

    oh_bg = arcpy.FeatureClassToFeatureClass_conversion(oh_gdb + "Block_Group", outputGDB, "OH_Block_Group")

    merge_ct = str(outputGDB) + '\\TMACOG_ct'
    merge_bg = str(outputGDB) + '\\TMACOG_bg'
    mpo_ct = arcpy.Merge_management([mi_ct, oh_ct], merge_ct)
    mpo_bg = arcpy.Merge_management([mi_bg, oh_bg], merge_bg)

    arcpy.AddField_management(bgtable, "Geocode_STR", "TEXT")
    arcpy.CalculateField_management(bgtable, "Geocode_STR", "str('{:f}'.format(!Geocode!)).rstrip('.0')","PYTHON")

    arcpy.AddField_management(cttable, "Geocode_STR", "TEXT")
    arcpy.CalculateField_management(cttable, "Geocode_STR", "str('{:f}'.format(!Geocode!))[:-7]","PYTHON")
    # create temporary layers so that the AddJoin tool works
    mpo_ct_lyr = arcpy.MakeFeatureLayer_management(mpo_ct, "mpo_ct_lyr")
    mpo_bg_lyr = arcpy.MakeFeatureLayer_management(mpo_bg, "mpo_bg_lyr")

    mpo_ctjoin = arcpy.AddJoin_management(mpo_ct_lyr, "GEOID", cttable, "Geocode_STR", "KEEP_COMMON")
    mpo_bgjoin = arcpy.AddJoin_management(mpo_bg_lyr, "GEOID", bgtable, "Geocode_STR", "KEEP_COMMON")

    ohmi_ctout = arcpy.FeatureClassToFeatureClass_conversion(mpo_ctjoin, str(outputGDB), "TMACOG_Title_6_ct")
    ohmi_bgout = arcpy.FeatureClassToFeatureClass_conversion(mpo_bgjoin, str(outputGDB), "TMACOG_Title_6_bg")

    # clip data to county boundaries
    stencil = arcpy.MakeFeatureLayer_management("Z:/fullerm/GIS_Data/TMACOG.gdb/County_boundaries_stencil3857", "stencil")
    ohmi_ctout_lyr = arcpy.MakeFeatureLayer_management(ohmi_ctout, "ohmi_ct_lyr")
    ohmi_bgout_lyr = arcpy.MakeFeatureLayer_management(ohmi_bgout, "ohmi_bg_lyr")
    print(' \bDone')
    print('  Clipping features...')

    ohmi_bg_clipped = arcpy.Clip_analysis(ohmi_bgout_lyr, stencil, str(outputGDB) + '\\TMACOG_Title_6_bg_clipped')
    ohmi_ct_clipped = arcpy.Clip_analysis(ohmi_ctout_lyr, stencil, str(outputGDB) + '\\TMACOG_Title_6_ct_clipped')
    # arcpy.mp.LayerFile()
    ohmi_bg_clipped_lyr = arcpy.MakeFeatureLayer_management(ohmi_bg_clipped, "ohmi_bg_clipped_lyr")
    ohmi_ct_clipped_lyr = arcpy.MakeFeatureLayer_management(ohmi_ct_clipped, "ohmi_ct_clipped_lyr")
    # create layer objects for block groups and census tracts
    pn = "American_Community_Survey_Data"
    proj_loc = "C:/Users/fullerm/Documents/ArcGIS/Projects/" + pn + "/"
    bg_lyrx = arcpy.SaveToLayerFile_management(ohmi_bg_clipped_lyr, proj_loc + 'ohmi_bg_clipped.lyrx')
    ct_lyrx = arcpy.SaveToLayerFile_management(ohmi_ct_clipped_lyr, proj_loc + 'ohmi_ct_clipped.lyrx')
    # open existing ArcMap Document and add data
    aprx = arcpy.mp.ArcGISProject("C:/Users/fullerm/Documents/ArcGIS/Projects/" + pn + '\\' + pn + ".aprx")
    m = aprx.listMaps('Map')[0]
    bg_lyrFile = arcpy.mp.LayerFile(bg_lyrx)
    m.addLayer(bg_lyrFile)
    ct_lyrFile = arcpy.mp.LayerFile(ct_lyrx)
    m.addLayer(ct_lyrFile)
    aprx.save()
# manipulate layers to display data

if __name__ == '__main__':
    spatialize()
