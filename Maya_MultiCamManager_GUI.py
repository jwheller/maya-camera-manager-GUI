#Maya Multi-Camera Manager plugin
#by Jaden Heller

import maya.cmds as cmds
import os
 
class MultiCamManager_Window(object):
    
    def __init__(self):
        
        self.window = "MultiCamManager"
        self.title = "Multi-Camera Manager"
        self.size = ( 400, 400)
        dir_path = os.path.dirname(os.path.realpath(__file__))
        #Incase there's an instance of the window already open, close it
        if cmds.window(self.window, exists = True):
            cmds.deleteUI(self.window, window = True)
        #Create a new instance of the window
        self.window = cmds.window(self.window, title = self.title, widthHeight=self.size)
        #Layout for the title and the seperator line
        titleLayout = cmds.columnLayout(adjustableColumn = True)
        cmds.rowLayout(parent = titleLayout, numberOfColumns = 2, adjustableColumn = 2)
        cmds.image("Logo", image = dir_path + "\Images\MCamM-Logo_v1.png")
        cmds.text (self.title)
        cmds.separator(height=20, style = "doubleDash", parent = titleLayout)
        #New layout for the Load Camera button (additional spacing between text and the button)
        cmds.columnLayout(adjustableColumn = True, rowSpacing = 20, parent = titleLayout)
        cmds.text("Load all cameras in the scene - Double-click to refresh")
        cmds.button(label = "Load All Cameras", command = self.selectCameras)
        #A collapsable menu called "Cameras" incase the user wishes to hide the list of cameras
        self.CamFrame = cmds.frameLayout("camFrame", label = "Cameras", collapsable = True, collapse = False, marginWidth = 20)
        cmds.columnLayout(adjustableColumn = True, columnOffset = ("both", 90), rowSpacing = 20) 

        cmds.showWindow()
    
    
    def selectCameras(self, *args):

        shapeString = "Shape"
        #List all the cameras in the scene
        allCameras = cmds.ls(cameras = True) 
        if len(allCameras) < 1:
            cmds.warning("No Cameras in scene")
        else:
            self.clearButtons()
            for cameraName in allCameras:
                print (cameraName + " is a camera in the scene")
                #Remove the word "-Shape" that Maya appends to the name of Camera objects:
                cameraNameLabel = cameraName.replace(shapeString, "")  
                lookThruCam = ("cmds.lookThru(\" %s \")") % (cameraName)
                #Create the buttons
                cmds.button(cameraName, label = cameraNameLabel, command = lookThruCam)


    def clearButtons(self, *args):
        
        #Clear the frame holding the buttons so that it can be re-filled with updated Cam info
        cmds.deleteUI(self.CamFrame, layout = True)
        self.CamFrame = cmds.frameLayout("camFrame", label = "Cameras", collapsable = True, collapse = False, marginWidth = 20)
        cmds.columnLayout(adjustableColumn = True, columnOffset = ("both", 90), rowSpacing = 20)