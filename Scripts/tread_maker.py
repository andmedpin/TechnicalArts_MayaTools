import maya.cmds as cmds

first_run = True


# =====     Function Definitions    =====

def window_maker():
    window_name = "TreadBuildWindow"

    if cmds.window(window_name, query=True, exists=True):
        cmds.deleteUI(window_name)

    cmds.window(window_name)
    cmds.columnLayout()

    # Title
    cmds.text("Tread Maker")
    cmds.separator(w=500, h=10)
    window_maker.init_button = cmds.button(label="Initialize", command="make_locator()")
    window_maker.reset_button = cmds.button(label="Reset", command="reset_locator()", enable=False)

    cmds.separator(w=500)
    window_maker.curve_button = cmds.button(label="Make Tread Curve", command="make_curve()", visible=False,
                                            enable=False)

    cmds.separator(w=500)
    window_maker.text_button = cmds.textFieldButtonGrp(buttonLabel="Pick Tread OBJ", buttonCommand="pick_object()",
                                                       editable=False, visible=False)
    window_maker.picker_button = cmds.button(label="Pick Tread Object", command="make_curve()", visible=False,
                                             enable=False)

    cmds.separator(w=500)
    # window_maker.tread_text = cmds.text(label="Yo",visible = True)
    window_maker.text_tread = cmds.text("No. Treads", visible=False)
    window_maker.copies_slider = cmds.intSliderGrp(min=10, max=200, width=500, field=True, changeCommand="numchange()",
                                                   visible=False)
    cmds.separator(w=500)
    # window_maker.tread_button = cmds.button(label = "Make Treads", command = "make_treads()", visible = True, enable = True)

    cmds.showWindow()


def make_locator():
    global first_run
    make_locator.front_locator = cmds.spaceLocator(n="CircleLocator_Front")
    cmds.scale(3, 3, 3)
    cmds.move(0, 0, 10, r=True)
    make_locator.back_locator = cmds.spaceLocator(n="CircleLocator_Back")
    cmds.scale(3, 3, 3)

    # Only prompt for locator placement the first time the user runs the program
    if first_run == True:
        cmds.confirmDialog(title="Locator Placement", message="Place the Locators where you need.")
        first_run = False
    cmds.button(window_maker.init_button, edit=True, enable=False)
    cmds.button(window_maker.reset_button, edit=True, enable=True)
    cmds.button(window_maker.curve_button, edit=True, visible=True, enable=True)


def reset_locator():
    # Delete Locators
    cmds.delete(make_locator.front_locator)
    cmds.delete(make_locator.back_locator)

    # Hide Buttons
    cmds.button(window_maker.init_button, edit=True, enable=True)
    cmds.button(window_maker.curve_button, edit=True, enable=False, visible=False)
    cmds.button(window_maker.reset_button, edit=True, enable=False)
    cmds.textFieldButtonGrp(window_maker.text_button, edit=True, enable=False, visible=False, text="")
    cmds.intSliderGrp(window_maker.copies_slider, edit=True, visible=False, value=0)
    cmds.text(window_maker.text_tread, edit=True, visible=False)

    # If the user resets before the Curve gets created, just try to get it and ignore the Error
    try:
        cmds.delete(make_curve.tread_curve)
        cmds.delete(make_curve.locator_group)
        cmds.delete(numchange.new_polyobject)
    except AttributeError:
        pass
    except ValueError:
        pass


def make_curve():
    cmds.select(make_locator.front_locator)
    front_locator_position = cmds.getAttr(".translateZ")
    cmds.select(make_locator.back_locator)
    back_locator_position = cmds.getAttr(".translateZ")
    print(front_locator_position)
    print(back_locator_position)
    locator_distance = abs(front_locator_position - back_locator_position)
    print("Total Distance is %i" % locator_distance)
    curve_radius = locator_distance / 2
    make_curve.tread_curve = cmds.circle(n="TreadCurve", r=curve_radius, nr=(1, 0, 0))
    make_curve.locator_group = cmds.group(make_locator.front_locator, make_locator.back_locator, n="Loc_Group")
    cmds.select(make_curve.tread_curve, r=True)
    cmds.select("Loc_Group", add=True)
    cmds.align(z="mid", atl=True)
    cmds.select(make_curve.tread_curve)
    cmds.FreezeTransformations()
    cmds.textFieldButtonGrp(window_maker.text_button, edit=True, enable=True, visible=True)
    cmds.button(window_maker.curve_button, edit=True, enable=False, visible=False)
    cmds.select(clear=True)
    cmds.confirmDialog(title="Tread", message="Select an object to be the tread")
    # delete the values of selected_object


def pick_object():
    global selected_object
    selected_object = cmds.ls(sl=True)

    if len(selected_object) == 1:
        shapes = cmds.listRelatives(selected_object[0], shapes=True)
        if shapes:
            print(cmds.objectType(shapes[0]))
            if cmds.objectType(shapes[0], isType='mesh'):
                cmds.textFieldButtonGrp(window_maker.text_button, edit=True, text=selected_object[0])
                cmds.intSliderGrp(window_maker.copies_slider, edit=True, visible=True)
                cmds.text(window_maker.text_tread, edit=True, visible=True)
                return selected_object
            else:
                cmds.warning("Please Select an Object that has a mesh.")
    else:
        cmds.warning("Select 1 object")
        cmds.textFieldButtonGrp(window_maker.text_button, e=True, tx="")


def numchange():
    if cmds.objExists("TreadFull"):
        cmds.delete("TreadFull")
    if cmds.objExists("_wire"):
        cmds.delete("_wire")

    global updateCopynum
    updateCopynum = cmds.intSliderGrp(window_maker.copies_slider, v=True, q=True)

    cmds.select(selected_object, r=True)
    cmds.select(make_curve.tread_curve, add=True)
    cmds.pathAnimation(
        f=True,
        fa="z",
        ua="y",
        wut="vector",
        wu=(0, 1, 0),
        inverseFront=False,
        iu=False,
        b=False,
        stu=1,
        etu=updateCopynum
    )
    cmds.select(selected_object, r=True)
    cmds.selectKey("motionPath1_uValue", time=(1, updateCopynum))
    cmds.keyTangent(itt="linear", ott="linear")
    cmds.snapshot(n="TreadSS", i=1, ch=False, st=1, et=updateCopynum, u="Animation Curve")
    cmds.DeleteMotionPaths()
    cmds.select("TreadSSGroup", r=True)
    numchange.new_polyobject = cmds.polyUnite(n="TreadFull", ch=False)
    cmds.CenterPivot(numchange.new_polyobject)
    cmds.select("TreadSSGroup", r=True)
    cmds.delete()

    def create_wireDeformer(geo, wireCurve, dropoff_distance=40):
        wire = cmds.wire(geo, w=wireCurve, n="_wire")
        wire_node = wire[0]
        cmds.setAttr(wire_node + ".dropoffDistance[0]", dropoff_distance)

    cmds.select("TreadFull")
    wireObj = cmds.ls(sl=True, o=True)[0]

    cmds.select(make_curve.tread_curve)
    wireCurve = cmds.ls(sl=True, o=True)[0]

    create_wireDeformer(wireObj, wireCurve, 40)
    return updateCopynum


def make_treads():
    cmds.select(selected_object, r=True)
    cmds.select(make_curve.tread_curve, add=True)
    cmds.pathAnimation(
        f=True,
        fa="z",
        ua="y",
        wut="vector",
        wu=(0, 1, 0),
        inverseFront=False,
        iu=False,
        b=False,
        stu=1,
        etu=updateCopynum
    )
    cmds.select(selected_object, r=True)
    cmds.selectKey("motionPath1_uValue", time=(1, updateCopynum))
    cmds.keyTangent(itt="linear", ott="linear")
    cmds.snapshot(n="TreadSS", i=1, ch=False, st=1, et=updateCopynum, u="Animation Curve")
    cmds.DeleteMotionPaths()
    cmds.select("TreadSSGroup", r=True)
    cmds.polyUnite(n="TreadFull", ch=False)
    cmds.select("TreadSSGroup", r=True)
    cmds.delete()

    def create_wireDeformer(geo, wireCurve, dropoff_distance=40):
        wire = cmds.wire(geo, w=wireCurve, n="_wire")
        wire_node = wire[0]
        cmds.setAttr(wire_node + ".dropoffDistance[0]", dropoff_distance)

    cmds.select("TreadFull")
    wireObj = cmds.ls(sl=True, o=True)[0]

    cmds.select(make_curve.tread_curve)
    wireCurve = cmds.ls(sl=True, o=True)[0]

    create_wireDeformer(wireObj, wireCurve, 40)


# =====     Make sure the user knows the direction or not    =====
confirm_prompt = cmds.confirmDialog(
    title="Start",
    m="Is your model is placed along the Z Axis",
    b=["Yes", "No"],
    defaultButton="Yes",
    cancelButton="No"
)

print(confirm_prompt)

if confirm_prompt == "No" or confirm_prompt == "dismiss":
    cmds.warning("Please, place your model along the Z Axis")
    # cmds.confirmDialog(m = "Please do it")


else:
    window_maker()