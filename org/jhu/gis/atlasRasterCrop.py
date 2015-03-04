# Loops through a collection of folders for atlas images and crops the raster images to match the shape file grid
import arcpy, arcgisscripting, os

baseImageDir = "C:/Workspace/Baltimore_Atlas/1897_Atlas"
imageDir = "Rectified Data"
shapeFile ="C:/Workspace/Baltimore_Atlas/OrthoIndexDissolved2Sheets.shp"


for fn in os.listdir(baseImageDir):
    where = "IndexSht = '" + fn.lower() + "'"
    rows = arcpy.SearchCursor(shapeFile, where, "", "Shape; IndexSht", "")

    row = rows.next()
    extent = row.shape.extent
    extentStr = str(extent.XMin) + " " + str(extent.YMin) + " " + str(extent.XMax) + " " + str(extent.YMax)

    referencedImgDir = baseImageDir + "/" + fn + "/" + imageDir

    if os.path.exists(referencedImgDir) :
        for image in os.listdir(referencedImgDir) :
            if image.endswith(".tif") :
                imageName = os.path.splitext(image)[0]
                outFile = referencedImgDir + "/" + imageName + "clipped.tif"

                raster = arcgisscripting.Raster(referencedImgDir + "/" + image)

                print "Clipping: " + imageName
                arcpy.Clip_management(raster, extentStr, outFile, "#", "#", "NONE")