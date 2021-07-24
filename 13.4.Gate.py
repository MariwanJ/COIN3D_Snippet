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
# This is an example from the Inventor Mentor
# chapter 13, example 5.
#
# Gate engine.
# Mouse button presses enable and disable a gate engine.
# The gate engine controls an elapsed time engine that
# controls the motion of the duck.
#

from __future__ import print_function

####################################################################
#        Modified to be compatible with  FreeCAD                   #
#                                                                  #
# Author : Mariwan Jalal  mariwan.jalal@gmail.com                  #
####################################################################

import os, sys
import FreeCAD as App
import FreeCADGui as Gui
import pivy.coin as coin
from PySide import QtGui, QtCore  # https://www.freecadweb.org/wiki/PySide

#############################################################
# CODE FOR The Inventor Mentor STARTS HERE  (part 2)

# This routine is called for every mouse button event.
def myMousePressCB(userData, eventCB):
    # In Pivy no cast is necessary as it gets autocasted for you.
    gate = userData
    event = eventCB.getEvent()

    # Check for mouse button being pressed
    if coin.SoMouseButtonEvent.isButtonPressEvent(event, coin.SoMouseButtonEvent.ANY):

        # Toggle the gate that controls the duck motion
        if gate.enable.getValue():
            gate.enable = False
        else:
            gate.enable = True

        eventCB.setHandled()

# CODE FOR The Inventor Mentor ENDS HERE
#############################################################


def GagteExecute():
    # Print out usage message
    print("Click the left mouse button to enable/disable the duck motion")

    root = coin.SoSeparator()

    # Add a camera and light
    myCamera = coin.SoPerspectiveCamera()
    myCamera.position = (0., -4., 8.0)
    myCamera.heightAngle = 22/7/2.5
    myCamera.nearDistance = 1.0
    myCamera.farDistance = 15.0
    root.addChild(myCamera)
    root.addChild(coin.SoDirectionalLight())

    # Rotate scene slightly to get better view
    globalRotXYZ = coin.SoRotationXYZ()
    globalRotXYZ.axis = coin.SoRotationXYZ.X
    globalRotXYZ.angle = 22/7/9
    root.addChild(globalRotXYZ)

    # Pond group
    pond = coin.SoSeparator()
    root.addChild(pond)
    cylMaterial = coin.SoMaterial()
    cylMaterial.diffuseColor = (0., 0.3, 0.8)
    pond.addChild(cylMaterial)
    cylTranslation = coin.SoTranslation()
    cylTranslation.translation = (0., -6.725, 0.)
    pond.addChild(cylTranslation)
    myCylinder = coin.SoCylinder()
    myCylinder.radius = 4.0
    myCylinder.height = 0.5
    pond.addChild(myCylinder)

#############################################################
# CODE FOR The Inventor Mentor STARTS HERE  (part 1)

    # Duck group
    duck = coin.SoSeparator()
    root.addChild(duck)

    # Read the duck object from a file and add to the group
    myInput = coin.SoInput()
    if not myInput.openFile("E:\\TEMP\\fix some drawing\\Mentor_Freecad\\duck.iv"):     #TODO: FIXME: Chnage the path/file if you want
        sys.exit(1)
    duckObject = coin.SoDB.readAll(myInput)
    if duckObject == None:
        sys.exit(1)

    # Set up the duck transformations
    duckRotXYZ = coin.SoRotationXYZ()
    duck.addChild(duckRotXYZ)
    initialTransform = coin.SoTransform()
    initialTransform.translation = (0., 0., 3.)
    initialTransform.scaleFactor = (6., 6., 6.)
    duck.addChild(initialTransform)

    duck.addChild(duckObject)

    # Update the rotation value if the gate is enabled.
    myGate = coin.SoGate(coin.SoMFFloat.getClassTypeId())
    myCounter = coin.SoElapsedTime()
    myGate.input.connectFrom(myCounter.timeOut) 
    duckRotXYZ.axis = coin.SoRotationXYZ.Y  # rotate about Y axis
    duckRotXYZ.angle.connectFrom(myGate.output)

    # Add an event callback to catch mouse button presses.
    # Each button press will enable or disable the duck motion.
    myEventCB = coin.SoEventCallback()
    myEventCB.addEventCallback(coin.SoMouseButtonEvent.getClassTypeId(),
                               myMousePressCB, myGate)
    root.addChild(myEventCB)

    view = Gui.ActiveDocument.ActiveView
    sg = view.getSceneGraph()
    sg.addChild(root)
    