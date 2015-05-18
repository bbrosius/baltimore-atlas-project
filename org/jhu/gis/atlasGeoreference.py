__author__ = 'Ben'
# Loops through a collection of folders for atlas images and crops the raster images to match the shape file grid
import arcpy, arcgisscripting, os

baseImageDir = "C:/workspace/Baltimore_Atlas/1897_Atlas/1N-1E/Original Image and Files/"
imageFile = "1N-1E"
shapeFile ="C:/Workspace/Baltimore_Atlas/OrthoIndexDissolved2Sheets.shp"
arcpy.env.overwriteOutput = True

arcpy.env.outputCoordinateSystem = arcpy.Describe(shapeFile).spatialReference
where = "IndexSht = '" + imageFile.lower() + "'"
rows = arcpy.SearchCursor(shapeFile, where, "", "Shape; IndexSht", "")

row = rows.next()
extent = row.shape.extent
extentStr = str(extent.XMin) + " " + str(extent.YMin) + " " + str(extent.XMax) + " " + str(extent.YMax)

imagePath = baseImageDir + imageFile + ".tif"


referencedFile = baseImageDir + imageFile + "_referenced.tif"

raster = arcgisscripting.Raster(imagePath)

##Define source control points
source_pnt = "'2.372 29.044';'28.782 29.032';'28.797 2.59';'2.382 2.606'"

##Define target control points
target_pnt = "'" + str(extent.XMin) + " " + str(extent.YMax) + "';'" + str(extent.XMax) + " " + str(extent.YMax) + "';'" + str(extent.XMax) + " " + str(extent.YMin) + "';'" + str(extent.XMin) + " " + str(extent.YMin) + "'"
extentStr = str(extent.XMin) + " " + str(extent.YMin) + " " + str(extent.XMax) + " " + str(extent.YMax)

print "Georeferencing: " + imageFile
print "Target points: " + target_pnt

arcpy.Warp_management("1N-1E.tif", "'2.38208950617 29.0419241255';'28.7841728395 29.0210907922';'28.8050061728 2.58671579218';'2.38521450617 2.59713245885'", "'1421102.0 599458.0';'1426382.0 599458.0';'1426382.0 594178.0';'1421102.0 594178.0'\
", referencedFile, "POLYORDER1",\
                          "NEAREST")

clippedFile = baseImageDir + "/" + imageFile + "clipped.tif"
arcpy.Clip_management(referencedFile, extentStr, clippedFile, "#", "#", "NONE")