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

print "Georeferencing: " + imageFile
print "Target points: " + target_pnt
arcpy.Warp_management(raster, source_pnt, target_pnt, referencedFile, "POLYORDER1",\
                          "NEAREST")

clippedFile = baseImageDir + "/" + imageFile + "clipped.tif"
arcpy.Clip_management(referencedFile, extentStr, clippedFile, "#", "#", "NONE")