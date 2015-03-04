
import arcpy, arcgisscripting

# Open a searchcursor
#  Input: C:/Data/Counties.shp
#  FieldList: NAME; STATE_NAME; POP2000
#  SortFields: STATE_NAME A; POP2000 D
#
rows = arcpy.SearchCursor("C:/Workspace/Baltimore_Atlas/OrthoIndexDissolved2Sheets.shp", "IndexSht = '1n-1e'", "", "Shape; IndexSht",
                          "")
currentState = ""

# Iterate through the rows in the cursor
#
for row in rows:

    # Print out the state name, county, and population
    #
    print "IndexSht: " + row.IndexSht

    extent = row.shape.extent
    print extent.XMin,extent.YMin,extent.XMax,extent.YMax

raster = arcgisscripting.Raster('1N-1E1.tif')

print raster.extent

extentStr = str(extent.XMin) + " " + str(extent.YMin) + " " + str(extent.XMax) + " " + str(extent.YMax)
print extentStr
arcpy.Clip_management(raster, extentStr, "C:/Workspace/Baltimore_Atlas/1N-1E1-Clipped.tif", "#", "#", "NONE")