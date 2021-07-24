#!/usr/bin/env python

###
# Copyright (c) 2002-2007 Systems in Motion
#
# Permission to use, copy, modify, and distribute this coin.Software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE coin.SoFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS coin.SoFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATcoin.SoEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS coin.SoFTWARE.
#

###
# This is an example from The Inventor Mentor,
# chapter 9, example 4.
#
# Example of setting up pick actions and using the pick path.
# A couple of objects are displayed.  The program catches 
# mouse button events and determines the mouse position. 
# A pick action is applied and if an object is picked the
# pick path is printed to stdout.
#


####################################################################
#        Modified to be compatible with  FreeCAD                   #
#                                                                  #
# Author : Mariwan Jalal  mariwan.jalal@gmail.com                  #
####################################################################

import os
import sys
import FreeCAD as App
import FreeCADGui as Gui
import pivy.coin as coin

###############################################################
# CODE FOR The Inventor Mentor STARTS HERE


#Warning: Might not works as it should  : TODO: FIXME: Mariwan



def writePickedPath(root, viewport, curSorPosition):
    myPickAction = coin.SoRayPickAction(viewport)

    # Set an 8-pixel wide region around the pixel
    myPickAction.setPoint(curSorPosition)
    myPickAction.setRadius(8.0)

    # Start a pick traversal
    myPickAction.apply(root)
    myPickedPoint = myPickAction.getPickedPoint()
    if myPickedPoint == None: return False

    # Write out the path to the picked object
    myWriteAction = coin.SoWriteAction()
    myWriteAction.apply(myPickedPoint.getPath())

    return True

# CODE FOR The Inventor Mentor ENDS HERE
###############################################################

# This routine is called for every mouse button event.
def myMousePressCB(userData, eventCB):
    root = userData
    event = eventCB.getEvent()

    # Check for mouse button being pressed  
    if coin.SoMouseButtonEvent.isButtonPressEvent(event, coin.SoMouseButtonEvent.ANY):
        myRegion = eventCB.getAction().getViewportRegion()
        writePickedPath(root, myRegion, event.getPosition(myRegion))
        eventCB.setHandled()

def PickActionExec():
    myMouseEvent = coin.SoMouseButtonEvent()
    root = coin.SoSeparator()

    # Add an event callback to catch mouse button presses.
    # The callback is set up later on.
    myEventCB = coin.SoEventCallback()
    root.addChild(myEventCB)

    # Read object data from a file
    mySceneInput = coin.SoInput()
    if not mySceneInput.openFile("E:\\TEMP\\fix some drawing\\Mentor_Freecad\\star.iv"):   #TODO Change path and file name  
        sys.exit(1)
    starObject = coin.SoDB.readAll(mySceneInput)
    if starObject == None: sys.exit(1)
    mySceneInput.closeFile()

    # Add two copies of the star object, one white and one red
    myRotation = coin.SoRotationXYZ()
    myRotation.axis = coin.SoRotationXYZ.X
    myRotation.angle = 22/7/2.2  # almost 90 degrees
    root.addChild(myRotation)

    root.addChild(starObject)  # first star object

    myMaterial = coin.SoMaterial()
    myMaterial.diffuseColor = (1.0, 0.0, 0.0)   # red
    root.addChild(myMaterial)
    myTranslation = coin.SoTranslation()
    myTranslation.translation = (1.0, 0.0, 1.0)
    root.addChild(myTranslation)
    root.addChild(starObject)  # second star object

    # Set up the event callback. We want to pass the root of the
    # entire scene graph (including the camera) as the userData,
    # coin.So we get the scene manager's version of the scene graph
    # root.
    view = Gui.ActiveDocument.ActiveView
    sg = view.getSceneGraph()
    sg.addChild(root)
    
    myEventCB.addEventCallback(coin.SoMouseButtonEvent.getClassTypeId(),
                               myMousePressCB,
                               sg)

