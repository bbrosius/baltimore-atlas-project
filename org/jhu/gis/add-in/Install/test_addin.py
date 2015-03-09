#Tool bar for arcmap that contains three combo boxes for setting the folders and shape file, and a button that runs the atlasRasterCrop python script
#The tool will then loop through the folders and clip the raster images to match the underlying grid.
import arcpy
import pythonaddins
import arcgisscripting
import os

baseImageDir = "G:/GPML/1StudentProjects/Historic Baltimore Atlas Georeference Project/1897 Atlas"
imageDir = "Rectified Data"
shapeFile ="G:/GPML/1StudentProjects/Historic Baltimore Atlas Georeference Project/OrthoIndexDissolved2Sheets.shp"
arcpy.env.overwriteOutput = True

class BaseImageDirClass(object):
    """Implementation for baltimore_atlas_toolbar.basedircombobox (ComboBox)"""
    def __init__(self):
        self.items = []
        self.value = baseImageDir
        self.editable = True
        self.enabled = True
        self.dropdownWidth = 'WWWWWWwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww'
        self.width = 'WWWWWWwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww'
    def onSelChange(self, selection):
        global baseImageDir
        baseImageDir = selection
    def onEditChange(self, text):
        global baseImageDir
        baseImageDir = text

class ImageDirClass(object):
    """Implementation for baltimore_atlas_toolbar.imagedircombobox (ComboBox)"""
    def __init__(self):
        self.items = []
        self.value = imageDir
        self.editable = True
        self.enabled = True
        self.dropdownWidth = 'WWWWWW'
        self.width = 'WWWWWWwwwwwwwwwwwwwwwwwwwwwww'
    def onSelChange(self, selection):
        global imageDir
        imageDir = selection
    def onEditChange(self, text):
        global imageDir
        imageDir = text

class RunClass(object):
    """Implementation for baltimore_atlas_toolbar.runbutton (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        for fn in os.listdir(baseImageDir):
            where = "IndexSht = '" + fn.lower() + "'"
            rows = arcpy.SearchCursor(shapeFile, where, "", "Shape; IndexSht", "")

            row = rows.next()
            extent = row.shape.extent
            extentStr = str(extent.XMin) + " " + str(extent.YMin) + " " + str(extent.XMax) + " " + str(extent.YMax)

            referencedImgDir = baseImageDir + "/" + fn + "/" + imageDir

            if os.path.exists(referencedImgDir) :
                for image in os.listdir(referencedImgDir) :
                    if image.endswith(".tif") and "clipped" not in image :
                        imageName = os.path.splitext(image)[0]
                        outFile = referencedImgDir + "/" + imageName + "clipped.tif"

                        raster = arcgisscripting.Raster(referencedImgDir + "/" + image)

                        print "Clipping: " + imageName
                        arcpy.Clip_management(raster, extentStr, outFile, "#", "#", "NONE")

class ShapeFileClass(object):
    """Implementation for baltimore_atlas_toolbar.shpfilecombobox (ComboBox)"""
    def __init__(self):
        self.items = []
        self.value = shapeFile
        self.editable = True
        self.enabled = True
        self.dropdownWidth = 'WWWWWW'
        self.width = 'WWWWWWwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww'
    def onSelChange(self, selection):
        global shapeFile
        shapeFile = selection
    def onEditChange(self, text):
        global shapeFile
        shapeFile = text
