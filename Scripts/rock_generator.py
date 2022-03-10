import maya.cmds as cmds
from random import uniform as rand
import time

currentFrame = 1

#TODO: Ask user for soft deformation or not with a checkbox

cmds.promptDialog(
    title = "Rock Generator",
    message = "How Many Rocks?"
)
rockAmmount = int(cmds.promptDialog(q = True, text = True))

cmds.promptDialog(
    title = "Name",
    message = "General Name for the Rocks"
)
rockName = cmds.promptDialog(q = True, text = True)

for i in range(1, rockAmmount + 1):
    randomRadius = rand(1,6)
    randomTranslateX = rand(-35, 35)
    randomTranslateZ = rand(-35, 35)
    
    cmds.polySphere(
        radius = randomRadius, 
        name = rockName + "_%s" %i, 
        subdivisionsX = 15, 
        subdivisionsY = 15)
    
    cmds.move(randomTranslateX, 0, randomTranslateZ)
    
    cmds.ConvertSelectionToFaces()
    selectedComponents = cmds.ls(sl = True, flatten = True)
    
    for i in range(len(selectedComponents)):
        cmds.select(selectedComponents[i])
        
        randomModX = rand(-0.5, 0.5)
        randomModY = rand(-0.5, 0.5)
        randomModZ = rand(-0.5, 0.5)
        
        cmds.move(randomModX,randomModY, randomModZ, relative = True)
    
    cmds.currentTime(currentFrame)
    currentFrame += 1
    time.sleep(0.01)

cmds.select(rockName + "_*")
cmds.group(name = "Rocks")