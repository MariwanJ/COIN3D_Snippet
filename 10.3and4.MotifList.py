#!/usr/bin/env python

###
# Copyright (c) 2002-2007 Systems in Motion
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#

###
# This is an example from The Inventor Mentor
# chapter 10, example 3.
#
# The scene graph has 4 objects which may be
# selected by picking with the left mouse button
# (use shift key to extend the selection to more
# than one object).
# 
# Hitting the up arrow key will increase the size of
# each selected object; hitting down arrow will decrease
# the size of each selected object.
#
# This also demonstrates selecting objects from a Motif
# list, and calling select/deselect functions on the
# coin.SoSelection node to change the selection. Use the Shift
# key to extend the selection (i.e. pick more than one
# item in the motif list.)
#

from __future__ import print_function
import os
import sys
import FreeCAD as App
import FreeCADGui as Gui
import pivy.coin as coin


#WARGNING: THIS CODE WILL NOT WORK AS THE CALLBACK IS DISABLED : TODO: FIXME:


# Global data
motifList = None
cubeTransform, sphereTransform, coneTransform, cylTransform = None, None, None, None

###############################################################
# CODE FOR The Inventor Mentor STARTS HERE  

CUBE, SPHERE, CONE, CYL, NUM_OBJECTS = 0, 1, 2, 3, 4

objectNames= (
    "Cube",
    "Sphere",
    "Cone",
    "Cylinder"
    )

# CODE FOR The Inventor Mentor ENDS HERE
###############################################################

#WARNING: This example will not work as it is based on Linux OS. TODO: FIXME: Mariwan


# # Create the object list widget
# def createList(display, selection):
#     global motifList
    
#     args = [None, None, None, None]
    
#     # Create a new shell window for the list
#     n = 0
#     XtSetArg(args[n], XmNtitle, "Selection")
#     n += 1
#     shell = XtAppCreateShell("example", "Inventor",
#                              topLevelShellWidgetClass, display, args, n)
    
# ###############################################################
# # CODE FOR The Inventor Mentor STARTS HERE  (part 3)

#     # Create a table of object names
#     table = XmString[NUM_OBJECTS]
#     for i in range(NUM_OBJECTS):
#         table[i] = XmStringCreate(objectNames[i], 
#                                   XmSTRING_DEFAULT_CHARSET)

#     # Create the list widget
#     n = 0
#     XtSetArg(args[n], XmNitems, table)
#     n += 1
#     XtSetArg(args[n], XmNitemCount, NUM_OBJECTS)
#     n += 1
#     XtSetArg(args[n], XmNselectionPolicy, XmEXTENDED_SELECT)
#     n += 1

#     motifList = XmCreateScrolledList(shell, "funcList", args, n)
#     XtAddCallback(motifList, XmNextendedSelectionCallback,
#                   myListPickCB, selection)
   
# # CODE FOR The Inventor Mentor ENDS HERE
# ###############################################################

#     # Free the name table
#     for i in range(NUM_OBJECTS):
#         XmStringFree(table[i])
#     del table

#     # Manage the list and return the shell
#     XtManageChild(motifList)
    
#     return shell

# This callback is invoked every time the user picks
# an item in the Motif list.
def myListPickCB(Widget, selection, listData):
    mySearchAction = SoSearchAction()
    
    # Remove the selection callbacks so that we don't get
    # called back while we are updating the selection list
    selection.removeSelectionCallback(mySelectionCB, True)
    selection.removeDeselectionCallback(mySelectionCB, False)

###############################################################
# CODE FOR The Inventor Mentor STARTS HERE  (part 4)

    # Clear the selection node, then loop through the list
    # and reselect
    selection.deselectAll()

    # Update the coin.SoSelection based on what is selected in
    # the motif list.  We do this by extracting the string
    # from the selected XmString, and searching for the 
    # object of that name.
    for i in range(listData.selected_item_count):
        mySearchAction.setName(SoGui.decodeString(listData.selected_items[i]))
        mySearchAction.apply(selection)
        selection.select(mySearchAction.getPath())

# CODE FOR The Inventor Mentor ENDS HERE
###############################################################

    # Add the selection callbacks again
    selection.addSelectionCallback(mySelectionCB, True)
    selection.addDeselectionCallback(mySelectionCB, False)


# This is called whenever an object is selected or deselected.
# if userData is True, then it's a selection else deselection.
# (we set this convention up when we registered this callback).
# The function updates the Motif list to reflect the current
# selection.
def mySelectionCB(isSelection, selectionPath):
    global motifList

    args = [None]
    
    # We have to temporarily change the selection policy to
    # MULTIPLE so that we can select and deselect single items.
    XtSetArg(args[0], XmNselectionPolicy, XmMULTIPLE_SELECT)
    XtSetValues(motifList, args, 1)
    
    node = selectionPath.getTail()
    
    for i in range(NUM_OBJECTS):
       if node.getName() == objectNames[i]:
           if isSelection:
               XmListSelectPos(motifList, i+1, False)
           else: XmListDeselectPos(motifList, i+1)
           XmUpdateDisplay(motifList)
           break

    # Restore the selection policy to extended.
    XtSetArg(args[0], XmNselectionPolicy, XmEXTENDED_SELECT)
    XtSetValues(motifList, args, 1)

###############################################################
# CODE FOR The Inventor Mentor STARTS HERE  (Example 10-4)

# Scale each object in the selection list
def myScaleSelection(selection, sf):
    global cubeTransform, sphereTransform, coneTransform, cylTransform

    # Scale each object in the selection list
    for i in range(selection.getNumSelected()):
        selectedPath = selection.getPath(i)
        xform = None

        # Look for the shape node, starting from the tail of the
        # path.  Once we know the type of shape, we know which
        # transform to modify
        for j in range(selectedPath.getLength()):
            if xform != None: break
            n = selectedPath.getNodeFromTail(j)

            if n.isOfType(coin.SoCube.getClassTypeId()):
                xform = cubeTransform
            elif n.isOfType(coin.SoCone.getClassTypeId()):
                xform = coneTransform
            elif n.isOfType(coin.SoSphere.getClassTypeId()):
                xform = sphereTransform
            elif n.isOfType(coin.SoCylinder.getClassTypeId()):
                xform = cylTransform

        # Apply the scale
        scaleFactor = xform.scaleFactor.getValue()
        scaleFactor *= sf
        xform.scaleFactor = scaleFactor

# If the event is down arrow, then scale down every object 
# in the selection list if the event is up arrow, scale up.
# The userData is the selectionRoot from main().
def myKeyPressCB(selection, eventCB):
    event = eventCB.getEvent()

    # check for the Up and Down arrow keys being pressed
    if coin.SoKeyboardEvent.isKeyPressEvent(event, coin.SoKeyboardEvent.UP_ARROW):
        myScaleSelection(selection, 1.1)
        eventCB.setHandled()
    elif coin.SoKeyboardEvent.isKeyPressEvent(event, coin.SoKeyboardEvent.DOWN_ARROW):
        myScaleSelection(selection, 1.0/1.1)
        eventCB.setHandled()

# CODE FOR The Inventor Mentor ENDS HERE
###############################################################

def MotifListExec():
    global cubeTransform, sphereTransform, coneTransform, cylTransform

    # Print out usage message
    print("Left mouse button        - selects object")
    print("<shift>Left mouse button - selects multiple objects")
    print("Up and Down arrows       - scale selected objects")
    
    # Create and set up the selection node
    selectionRoot = coin.SoSelection()
    selectionRoot.policy = coin.SoSelection.SHIFT
    selectionRoot.addSelectionCallback(mySelectionCB, True)
    selectionRoot.addDeselectionCallback(mySelectionCB, False)

    # Add a camera and some light
    myCamera = coin.SoPerspectiveCamera()
    selectionRoot.addChild(myCamera)
    selectionRoot.addChild(coin.SoDirectionalLight())

    # Add an event callback so we can receive key press events
    myEventCB = coin.SoEventCallback()
    myEventCB.addEventCallback(coin.SoKeyboardEvent.getClassTypeId(), 
                               myKeyPressCB, selectionRoot)
    selectionRoot.addChild(myEventCB)

    # Add some geometry to the scene
    # a red cube
    cubeRoot = coin.SoSeparator()
    cubeMaterial = coin.SoMaterial()
    cubeTransform = coin.SoTransform()
    cube = coin.SoCube()
    cubeRoot.addChild(cubeTransform)
    cubeRoot.addChild(cubeMaterial)
    cubeRoot.addChild(cube)
    cubeTransform.translation = (-2, 2, 0)
    cubeMaterial.diffuseColor = (.8, 0, 0)
    selectionRoot.addChild(cubeRoot)

    # a blue sphere
    sphereRoot = coin.SoSeparator()
    sphereMaterial = coin.SoMaterial()
    sphereTransform = coin.SoTransform()
    sphere = coin.SoSphere()
    sphereRoot.addChild(sphereTransform)
    sphereRoot.addChild(sphereMaterial)
    sphereRoot.addChild(sphere)
    sphereTransform.translation = (2, 2, 0)
    sphereMaterial.diffuseColor = (0, 0, .8)
    selectionRoot.addChild(sphereRoot)

    # a green cone
    coneRoot = coin.SoSeparator()
    coneMaterial = coin.SoMaterial()
    coneTransform = coin.SoTransform()
    cone = coin.SoCone()
    coneRoot.addChild(coneTransform)
    coneRoot.addChild(coneMaterial)
    coneRoot.addChild(cone)
    coneTransform.translation = (2, -2, 0)
    coneMaterial.diffuseColor = (0, .8, 0)
    selectionRoot.addChild(coneRoot)

    # a magenta cylinder
    cylRoot = coin.SoSeparator()
    cylMaterial = coin.SoMaterial()
    cylTransform = coin.SoTransform()
    cyl = coin.SoCylinder()
    cylRoot.addChild(cylTransform)
    cylRoot.addChild(cylMaterial)
    cylRoot.addChild(cyl)
    cylTransform.translation = (-2, -2, 0)
    cylMaterial.diffuseColor = (.8, 0, .8)
    selectionRoot.addChild(cylRoot)

###############################################################
# CODE FOR The Inventor Mentor STARTS HERE  (part 2)

    cube.setName(objectNames[CUBE])
    sphere.setName(objectNames[SPHERE])
    cone.setName(objectNames[CONE])
    cyl.setName(objectNames[CYL])

# CODE FOR The Inventor Mentor ENDS HERE
###############################################################

    # Create a render area for viewing the scene
    view = Gui.ActiveDocument.ActiveView
    sg = view.getSceneGraph()
    sg.addChild(cylRoot)
    sg.addChild(coneRoot)
    sg.addChild(cubeRoot)
    sg.addChild(sphereRoot)
    
    sg.addChild(selectionRoot)

