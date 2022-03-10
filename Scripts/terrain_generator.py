import maya.cmds as cmds
from random import uniform as rand
import time

# --- Initial Defaults for Variables---
terrainWidth = 50
terrainHeight = 50
terrainSubdivisions = 10
sliderValueFreq = 3
sliderValueX = 1.0
sliderValueZ = 1.0
sliderValueDepth = -1.0
sliderValueHeight = 1.0
componentType = 0
rockName = "rock"
rockAmmount = 10
rockMinRad = 1
rockMaxRad = 10
softSelectionEnablePrompt = 1

# --- Function Definitions ---
# Creatting a Plane
def SoftSelectionSet():
    
    #Softselection: set radius, and enable or disable it 
    softSelectionFallofRadius = terrainSubdivisions/5
    cmds.softSelect(softSelectEnabled = softSelectionEnablePrompt, softSelectDistance = softSelectionFallofRadius)
    
def GenerateTerrain():
    
    # Query user values
    GenerateTerrain.terrainName = cmds.textFieldGrp(textGrpInputNameTerrain, q = True, text = True)
    
    SoftSelectionSet()

   #Create the polyplane 
    GenerateTerrain.proceduralTerrain = cmds.polyPlane(
        name = GenerateTerrain.terrainName,
        width = terrainWidth,
        height = terrainHeight,
        subdivisionsWidth = terrainSubdivisions,
        subdivisionsHeight = terrainSubdivisions,
    )
    
    
    # Identifying the component type that we'll modify
    if componentType == 0:
        cmds.ConvertSelectionToVertices()
        selectedComponents = cmds.ls(sl = True, fl = True)
    elif componentType == 1:
        cmds.ConvertSelectionToEdges()
        selectedComponents = cmds.ls(sl = True, fl = True)
    elif componentType == 2:
        cmds.ConvertSelectionToFaces()
        selectedComponents = cmds.ls(sl = True, fl = True)

    for i in range(0, len(selectedComponents), sliderValueFreq):
        singleRandSelection = int(rand(0, len(selectedComponents)))
        cmds.select(clear = True)
        
        singleComponent = selectedComponents[singleRandSelection]
        cmds.select(singleComponent)
        
        randX = rand(-sliderValueX, sliderValueX)
        randZ  = rand(-sliderValueZ, sliderValueZ)
        randY = rand(sliderValueDepth, sliderValueHeight)
        
        cmds.move(randX, randY, randZ, r = True)
    cmds.select(clear = True)

def GenerateRocks():
    currentFrame = 1
    
    # Query user Values
    rockName = cmds.textFieldGrp(textGrpInputNameRock, q = True, text = True)
    
    SoftSelectionSet.softSelectionFallofRadius = terrainSubdivisions/5
    SoftSelectionSet() 
    
    #Rock Generator Loop
    for i in range(1, rockAmmount + 1):
        
        # Generate Random Values and then Generate Polyspheres
        randomRadius = rand(rockMinRad, rockMaxRad)
        randomTranslateX = rand(-(terrainWidth/2), (terrainWidth/2))
        randomTranslateZ = rand(-(terrainHeight/2), (terrainHeight/2))
        rockSubDivX = int(rand(13, 17)) 
        rockSubDivY= int(rand(13, 17))
        
        newRock = cmds.polySphere(
            radius = randomRadius, 
            name = rockName + "_%s" %i, 
            subdivisionsX = rockSubDivX, 
            subdivisionsY = rockSubDivY)
        
        # Move rock pivot to the bottom of the rock
        cmds.xform(centerPivots = True)
        cmds.move(0,0,0, rotatePivotRelative = True)
        
        # Get a random vertix's position of the plane
        cmds.select(GenerateTerrain.proceduralTerrain)
        cmds.ConvertSelectionToVertices()
        selectedComponents = cmds.ls(sl = True, fl = True)
        randomPlaneVertix = int(rand(0, len(selectedComponents)))
        planeVertixPosition = cmds.pointPosition(selectedComponents[randomPlaneVertix])

        cmds.select(newRock)
        cmds.move(planeVertixPosition[0], planeVertixPosition[1], planeVertixPosition[2])
        
        # Deform spheres faces
        cmds.select(newRock)
        cmds.ConvertSelectionToVertices()
        selectedComponents = cmds.ls(sl = True, flatten = True)
        
        for i in range(len(selectedComponents)):
            cmds.select(selectedComponents[i])
            
            randomModX = rand(-1, 1)
            randomModY = rand(-1, 1)
            randomModZ = rand(-1, 1)
            
            cmds.move(randomModX,randomModY, randomModZ, relative = True)
        
        cmds.currentTime(currentFrame)
        currentFrame += 1
        time.sleep(0.01)

    cmds.select(rockName + "_*")
    cmds.group(name = "Rocks")

# --- Window Creation ---
try:
    if cmds.window(terrainMakerWindow, exists = True):
        cmds.deleteUI(terrainMakerWindow)
except:
    pass

terrainMakerWindow = cmds.window("Terrain Maker Window", title = "Terrain Generator", w = 450, h = 350)
form = cmds.formLayout()
tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
cmds.formLayout( form, edit=True, attachForm=((tabs, 'top', 0), (tabs, 'left', 0), (tabs, 'bottom', 0), (tabs, 'right', 0)) )

# -- Terrain --
child1 = cmds.rowColumnLayout(numberOfColumns = 1)

# Ask for polyPlane Terrain Initial Values
textGrpInputNameTerrain = cmds.textFieldGrp(label = "Name:", placeholderText = "Terrain",
forceChangeCommand = True)

intGrpWidth = cmds.intSliderGrp(label = "Width:", field = True, min = 1, max = 500, value = 50,
changeCommand = "terrainWidth = cmds.intSliderGrp(intGrpWidth, q = True, value = True)")

intGrpHeight = cmds.intSliderGrp(label = "Height:", field = True, min = 1, max = 500, value = 50,
changeCommand = "terrainHeight = cmds.intSliderGrp(intGrpHeight, q = True, value = True)")

intGrpSubdivisions = cmds.intSliderGrp(label = "Subdivisions:", field = True, min = 1, max = 250, value = 10,
changeCommand = "terrainSubdivisions = cmds.intSliderGrp(intGrpSubdivisions, q = True, value = True)")

#Mountain Properties
intRangeX = cmds.floatSliderGrp(label = "Range for X", field = True, min = 0, max = 15, value = 1,
changeCommand = "sliderValueX = cmds.floatSliderGrp(intRangeX, q = True, value = True)")

intRangeZ = cmds.floatSliderGrp(label = "Range for Z", field = True, min = 0, max = 15, value = 1, 
changeCommand = "sliderValueZ = cmds.floatSliderGrp(intRangeZ, q = True, value = True)")

intRangeDepth = cmds.floatSliderGrp(label = "Range for Depth", field = True, min = -50, max = 0, value = -1,
changeCommand = "sliderValueDepth = cmds.floatSliderGrp(intRangeDepth, q = True, value = True)")

intRangeHeight = cmds.floatSliderGrp(label = "Range for Height", field = True, min = 0, max = 50, value = 1,
changeCommand = "sliderValueHeight = cmds.floatSliderGrp(intRangeHeight, q = True, value = True)")

cmds.text("Please Indicate the Frequency of Noise. The higher the value, the higer the gap")
userFrequencySldr = cmds.intSliderGrp(label = "Fequency Indicator", field = True, min = 1, max = 10, value = 3,
changeCommand = "sliderValueFreq = cmds.intSliderGrp(userFrequencySldr, q = True, value = True)")
cmds.separator(w = 450)

#Selecting the Component to Modify
cmds.text("Choose based on what component of the plne you would like to deform to generate terrain")
cmds.radioCollection()
cmds.radioButton(label = "Vertix", changeCommand = "componentType = 0", sl = True)
cmds.radioButton(label = "Edges", changeCommand = "componentType = 1")
cmds.radioButton(label = "Faces", changeCommand = "componentType = 2")
cmds.separator(w = 450)

#Soft Select Button
cmds.text("Use Soft Selection?")
cmds.radioCollection()
cmds.radioButton(label = "Yes", changeCommand = "softSelectionEnablePrompt = 1", sl = True)
cmds.radioButton(label = "No", changeCommand = "softSelectionEnablePrompt = 0")
cmds.separator(w = 450)

cmds.button(label = "Generate", w = 100, h = 50, command = "GenerateTerrain()")
cmds.setParent( '..' )

# -- Rocks --
child2 = cmds.rowColumnLayout(numberOfColumns = 1, columnAlign = (1, "center"))
textGrpInputNameRock = cmds.textFieldGrp(label = "Rock Name:", placeholderText = "Rock", forceChangeCommand = True)

userRockSldr = cmds.intSliderGrp(label = "Number of Rocks", field = True, min = 1, max = 100, value = 10,
changeCommand = "rockAmmount = cmds.intSliderGrp(userRockSldr, q = True, value = True)")

userRockMinRadSldr = cmds.intSliderGrp(label = "Min Size of Rocks", field = True, min = 1, max = 9, value = 1,
changeCommand = "rockMinRad = cmds.intSliderGrp(userRockMinRadSldr, q = True, value = True)")

userRockMaxRadSldr = cmds.intSliderGrp(label = "Max Size of Rocks", field = True, min = 2, max = 10, value = 10,
changeCommand = "rockMaxRad = cmds.intSliderGrp(userRockMaxRadSldr, q = True, value = True)")

cmds.separator(w = 450)

#Soft Select Button
cmds.text("Use Soft Selection?")
cmds.radioCollection()
cmds.radioButton(label = "Yes", changeCommand = "softSelectionEnablePrompt = 1", sl = True)
cmds.radioButton(label = "No", changeCommand = "softSelectionEnablePrompt = 0")
cmds.separator(w = 450)


# Buttons
cmds.button(label = "Drop Rocks", w = 100, h = 50, command = "GenerateRocks()")
cmds.setParent( '..' )

cmds.tabLayout( tabs, edit=True, tabLabel=((child1, 'Terrain'), (child2, 'Rocks')) )
cmds.showWindow()


