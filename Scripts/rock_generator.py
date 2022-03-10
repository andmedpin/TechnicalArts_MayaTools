import maya.cmds as cmds
from random import uniform as rand
import time

current_frame = 1

#TODO: Ask user for soft deformation or not with a checkbox

cmds.promptDialog(
    title = "Rock Generator",
    message = "How Many Rocks?"
)
rock_ammount = int(cmds.promptDialog(q = True, text = True))

cmds.promptDialog(
    title = "Name",
    message = "General Name for the Rocks"
)
rock_name = cmds.promptDialog(q = True, text = True)

for i in range(1, rock_ammount + 1):
    random_radius = rand(1,6)
    random_translateX = rand(-35, 35)
    random_translateZ = rand(-35, 35)
    
    cmds.polySphere(
        radius = random_radius, 
        name = rock_name + "_%s" %i, 
        subdivisionsX = 15, 
        subdivisionsY = 15)
    
    cmds.move(random_translateX, 0, random_translateZ)
    
    cmds.ConvertSelectionToFaces()
    selected_components = cmds.ls(sl = True, flatten = True)
    
    for i in range(len(selected_components)):
        cmds.select(selected_components[i])
        
        random_modX = rand(-0.5, 0.5)
        random_modY = rand(-0.5, 0.5)
        random_modZ = rand(-0.5, 0.5)
        
        cmds.move(random_modX,random_modY, random_modZ, relative = True)
    
    cmds.currentTime(current_frame)
    current_frame += 1
    time.sleep(0.01)

cmds.select(rock_name + "_*")
cmds.group(name = "Rocks")