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
# chapter 13, example 6.
#
# Boolean engine.  Derived from example 13.5.
# The smaller duck stays still while the bigger duck moves,
# and starts moving as coin.Soon as the bigger duck stops.
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

# This routine is called for every mouse button event.
def myMousePressCB(gate, eventCB):
    event = eventCB.getEvent()

    # Check for mouse button being pressed
    if coin.SoMouseButtonEvent.isButtonPressEvent(event, coin.SoMouseButtonEvent.ANY):

        # Toggle the gate that controls the duck motion
        if gate.enable.getValue():
            gate.enable = False
        else:
            gate.enable = True

        eventCB.setHandled()


def BooleanExecu():
    # Print out usage message
    print("Only one duck can move at a time.")
    print("Click the left mouse button to toggle between the two ducks.")

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
    pondTranslation = coin.SoTranslation()
    pondTranslation.translation = (0., -6.725, 0.)
    pond.addChild(pondTranslation)
    # water
    waterMaterial = coin.SoMaterial()
    waterMaterial.diffuseColor = (0., 0.3, 0.8)
    pond.addChild(waterMaterial)
    waterCylinder = coin.SoCylinder()
    waterCylinder.radius = 4.0
    waterCylinder.height = 0.5
    pond.addChild(waterCylinder)
    # rock
    rockMaterial = coin.SoMaterial()
    rockMaterial.diffuseColor = (0.8, 0.23, 0.03)
    pond.addChild(rockMaterial)
    rockSphere = coin.SoSphere()
    rockSphere.radius = 0.9
    pond.addChild(rockSphere)

    # Read the duck object from a file and add to the group
    myInput = coin.SoInput()
    if not myInput.openFile("E:\\TEMP\\fix some drawing\\Mentor_Freecad\\duck.iv"):   #TODO: FIXME: Change file path 
        sys.exit(1)
    duckObject = coin.SoDB.readAll(myInput)
    if duckObject == None:
        sys.exit(1)

#############################################################
# CODE FOR The Inventor Mentor STARTS HERE  

    # Bigger duck group
    bigDuck = coin.SoSeparator()
    root.addChild(bigDuck)
    bigDuckRotXYZ = coin.SoRotationXYZ()
    bigDuck.addChild(bigDuckRotXYZ)
    bigInitialTransform = coin.SoTransform()
    bigInitialTransform.translation = (0., 0., 3.5)
    bigInitialTransform.scaleFactor = (6., 6., 6.)
    bigDuck.addChild(bigInitialTransform)
    bigDuck.addChild(duckObject)

    # Smaller duck group
    smallDuck = coin.SoSeparator()
    root.addChild(smallDuck)
    smallDuckRotXYZ = coin.SoRotationXYZ()
    smallDuck.addChild(smallDuckRotXYZ)
    smallInitialTransform = coin.SoTransform()
    smallInitialTransform.translation = (0., -2.24, 1.5)
    smallInitialTransform.scaleFactor = (4., 4., 4.)
    smallDuck.addChild(smallInitialTransform)
    smallDuck.addChild(duckObject)

    # Use a gate engine to start/stop the rotation of 
    # the bigger duck.
    bigDuckGate = coin.SoGate(coin.SoMFFloat.getClassTypeId())
    bigDuckTime = coin.SoElapsedTime()
    bigDuckGate.input.connectFrom(bigDuckTime.timeOut) 
    bigDuckRotXYZ.axis = coin.SoRotationXYZ.Y  # Y axis
    bigDuckRotXYZ.angle.connectFrom(bigDuckGate.output)

    # Each mouse button press will enable/disable the gate 
    # controlling the bigger duck.
    myEventCB = coin.SoEventCallback()
    myEventCB.addEventCallback(coin.SoMouseButtonEvent.getClassTypeId(),
                               myMousePressCB, bigDuckGate)
    root.addChild(myEventCB)

    # Use a Boolean engine to make the rotation of the smaller
    # duck depend on the bigger duck.  The smaller duck moves
    # only when the bigger duck is still.
    myBoolean = coin.SoBoolOperation()
    myBoolean.a.connectFrom(bigDuckGate.enable)
    myBoolean.operation = coin.SoBoolOperation.NOT_A

    smallDuckGate = coin.SoGate(coin.SoMFFloat.getClassTypeId())
    smallDuckTime = coin.SoElapsedTime()
    smallDuckGate.input.connectFrom(smallDuckTime.timeOut) 
    smallDuckGate.enable.connectFrom(myBoolean.output) 
    smallDuckRotXYZ.axis = coin.SoRotationXYZ.Y  # Y axis
    smallDuckRotXYZ.angle.connectFrom(smallDuckGate.output)
    
    view = Gui.ActiveDocument.ActiveView
    sg = view.getSceneGraph()
    sg.addChild(root)
    