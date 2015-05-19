import arcpy
import pythonaddins
import ntpath
import os

imageFile = ""
pointCount = 0
dialogShown = False
mapExtent = ""
shapeFile = ""
saveDir = ""
dataDir = "Rectified Data"

class RunButtonClass(object):
    """Implementation for geoclip_addin.runButton (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        global pointCount
        if pointCount < 4:
            pythonaddins.MessageBox("Select four map points before running", "Error", 0)
        else:
            global imageFile
            global shapeFile
            global  mapExtent
            arcpy.env.overwriteOutput = True

            arcpy.env.outputCoordinateSystem = arcpy.Describe(shapeFile).spatialReference
            where = "IndexSht = '" + imageFile[:-4].lower() + "'"
            rows = arcpy.SearchCursor(shapeFile, where, "", "Shape; IndexSht", "")

            row = rows.next()
            extent = row.shape.extent
            parentDir = os.path.join(saveDir, dataDir)
            if not os.path.exists(parentDir):
                os.makedirs(parentDir)
            referencedFile = os.path.join(parentDir, imageFile[:-4] + "_referenced.tif")

            ##Define target control points
            target_pnt = "'" + str(extent.XMin) + " " + str(extent.YMax) + "';'" + str(extent.XMax) + " " + str(extent.YMax) + "';'" + str(extent.XMax) + " " + str(extent.YMin) + "';'" + str(extent.XMin) + " " + str(extent.YMin) + "'"

            print "Georeferencing: " + imageFile
            print "Target points: " + target_pnt
            print "Map extent: " + mapExtent
            print "Reference file: " + referencedFile
            arcpy.Warp_management(imageFile, mapExtent, target_pnt, referencedFile, "POLYORDER1",
                                      "NEAREST")

            clippedFile = os.path.join(parentDir, imageFile[:-4] + "_clipped.tif")
            extentStr = str(extent.XMin) + " " + str(extent.YMin) + " " + str(extent.XMax) + " " + str(extent.YMax)
            arcpy.Clip_management(referencedFile, extentStr, clippedFile, "#", "#", "NONE")

            #Reset variables
            pointCount = 0
            mapExtent = ""
class SelectImageBox(object):
    """Implementation for geoclip_addin.selectImageBox (ComboBox)"""
    def __init__(self):
        self.editable = True
        self.enabled = True
        self.dropdownWidth = 'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW'
        self.width = 'WWWWWWWWWWWWWWWWWWWWWWWWWWW'
        self.mxd = arcpy.mapping.MapDocument('current')
        layers = arcpy.mapping.ListLayers(self.mxd)
        self.items = []
        for layer in layers:
            self.items.append(layer.name)
    def onSelChange(self, selection):
        global imageFile
        global saveDir
        imageFile = selection
        self.mxd = arcpy.mapping.MapDocument('current')
        layers = arcpy.mapping.ListLayers(self.mxd, selection)
        for layer in layers:
            saveDir = ntpath.dirname(layer.dataSource)
        #reset selection tool
        global  mapExtent
        global dialogShown
        mapExtent = ""
        dialogShown = False
    def onFocus(self, focused):
        if focused:
            self.mxd = arcpy.mapping.MapDocument('current')
            layers = arcpy.mapping.ListLayers(self.mxd)
            self.items = []
            for layer in layers:
                self.items.append(layer.name)

class SelectPointsTool(object):
    """Implementation for geoclip_addin.selectPointsTool (Tool)"""
    def __init__(self):
        self.enabled = True
        self.shape = "NONE"
        self.cursor = 3
    def onMouseDownMap(self, x, y, button, shift):
        global mapExtent
        global pointCount
        pointCount += 1
        if pointCount < 4:
            mapExtent += "'" + str(x) + " " + str(y) + "';"
        else:
            mapExtent += "'" + str(x) + " " + str(y) + "'"
        if pointCount == 1:
            pythonaddins.MessageBox("Select the top right corner of the map", "Selected Map Points", 0)
        elif pointCount == 2:
            pythonaddins.MessageBox("Select the bottom right corner of the map", "Selected Map Points", 0)
        elif pointCount == 3:
            pythonaddins.MessageBox("Select the bottom left corner of the map", "Selected Map Points", 0)
    def onMouseMove(self, x, y, button, shift):
        global dialogShown
        if not dialogShown:
            pythonaddins.MessageBox("Select the top left corner of the map", "Selected Map Points", 0)
            dialogShown = True
    def deactivate(self):
        global mapExtent
        global pointCount
        pointCount = 0
        mapExtent = ""

class ShapeFileComboBox(object):
    def __init__(self):
        self.editable = True
        self.enabled = True
        self.dropdownWidth = 'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW'
        self.width = 'WWWWWWWWWWWWWWWWWWWWWWWWWWW'
        self.mxd = arcpy.mapping.MapDocument('current')
        layers = arcpy.mapping.ListLayers(self.mxd)
        self.items = []
        for layer in layers:
            self.items.append(layer.name)
    def onSelChange(self, selection):
        global shapeFile
        shapeFile = selection
        global  mapExtent
        global dialogShown
        mapExtent = ""
        dialogShown = False
    def onFocus(self, focused):
        if focused:
            self.mxd = arcpy.mapping.MapDocument('current')
            layers = arcpy.mapping.ListLayers(self.mxd)
            self.items = []
            for layer in layers:
                self.items.append(layer.name)
