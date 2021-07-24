#!/usr/bin/env python

###
# Copyright (c) 2002-2007 Systems in Motion
#
# Permission to use, copy, modify, and distribute this coin.software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE coin.SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS coin.SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATcoin.SOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS coin.SOFTWARE.
#

###
# This is an example from the Inventor Mentor,
# chapter 14, example 3.
#
# This example illustrates the creation of motion hierarchies
# using nodekits by creating a model of a balance-style scale.
#
# It adds an coin.SoEventCallback to the "callback" list in the 
#     nodekit called 'support.'
# The callback will have the following response to events:
# Pressing right arrow key == lower the right pan
# Pressing left arrow key  == lower the left pan
# The pans are lowered by animating three rotations in the 
#     motion hierarchy.
# Use an coin.SoText2Kit to print instructions to the user as part
#     of the scene.
#
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

# Callback Function for Animating the Balance Scale.
# -- used to make the balance tip back and forth
# -- Note: this routine is only called in response to KeyPress
#    events since the call 'setEventInterest(KeyPressMask)' is
#    made on the coin.SoEventCallback node that uses it.
# -- The routine checks if the key pressed was left arrow (which
#    is XK_Left in X-windows talk), or right arrow (which is
#    XK_Right)
# -- The balance is made to tip by rotating the beam part of the
#    scale (to tip it) and then compensating (making the strings
#    vertical again) by rotating the string parts in the opposite
#    direction.
def tipTheBalance(support, # The nodekit representing 'support', the
                  # fulcrum of the balance. Passed in during
                  # main routine, below. 
                  eventCB):

    ev = eventCB.getEvent()

    # Which Key was pressed?
    # If Right or Left Arrow key, then continue...
    if coin.SoKeyboardEvent.isKeyPressEvent(ev, coin.SoKeyboardEvent.RIGHT_ARROW) or \
       coin.SoKeyboardEvent.isKeyPressEvent(ev, coin.SoKeyboardEvent.LEFT_ARROW):
        startRot, beamIncrement, stringIncrement = SbRotation(), SbRotation(), SbRotation()
        
        # These three parts are extracted based on knowledge of the
        # motion hierarchy (see the diagram in the main routine.
        beam1   = support.getPart("childList[0]",True)
        string1 = beam1.getPart("childList[0]",True)
        string2 = beam1.getPart("childList[1]",True)

        # Set angular increments to be .1 Radians about the Z-Axis
        # The strings rotate opposite the beam, and the two types
        # of key press produce opposite effects.
        if coin.SoKeyboardEvent.isKeyPressEvent(ev, coin.SoKeyboardEvent.RIGHT_ARROW):
            beamIncrement.setValue(coin.SbVec3f(0, 0, 1), -.1)
            stringIncrement.setValue(coin.SbVec3f(0, 0, 1), .1)
        else:
            beamIncrement.setValue(coin.SbVec3f(0, 0, 1), .1)
            stringIncrement.setValue(coin.SbVec3f(0, 0, 1), -.1)

        # Use coin.SO_GET_PART to find the transform for each of the 
        # rotating parts and modify their rotations.

        xf = beam1.getPart("transform", True)
        startRot = xf.rotation.getValue()
        startRot *= beamIncrement
        xf.rotation = startRot

        xf = string1.getPart("transform", True)
        startRot = xf.rotation.getValue()
        startRot *= stringIncrement
        xf.rotation = startRot

        xf = string2.getPart("transform", True)
        startRot = xf.rotation.getValue()
        startRot *= stringIncrement     
        xf.rotation = startRot

        eventCB.setHandled()

def BalanceExe():
    myScene = coin.SoSceneKit()

    myScene.setPart("lightList[0]", coin.SoLightKit())
    myScene.setPart("cameraList[0]", coin.SoCameraKit())
    myScene.setCameraNumber(1)                             #Change this to 0,1. ..etc     #todo:

    # Create the Balance Scale -- put each part in the 
    # childList of its parent, to build up this hierarchy:
    #
    #                    myScene
    #                       |
    #                     support
    #                       |
    #                     beam
    #                       |
    #                   --------
    #                   |       |
    #                string1  string2
    #                   |       |
    #                tray1     tray2

    support = coin.SoShapeKit()
    support.setPart("shape", coin.SoCone())
    support.set("shape { height 3 bottomRadius .3 }")
    myScene.setPart("childList[0]", support)

    beam = coin.SoShapeKit()
    beam.setPart("shape", coin.SoCube())
    beam.set("shape { width 3 height .2 depth .2 }")
    beam.set("transform { translation 0 1.5 0 } ")
    support.setPart("childList[0]", beam)

    string1 = coin.SoShapeKit()
    string1.setPart("shape", coin.SoCylinder())
    string1.set("shape { radius .05 height 2}")
    string1.set("transform { translation -1.5 -1 0 }")
    string1.set("transform { center 0 1 0 }")
    beam.setPart("childList[0]", string1)

    string2 = coin.SoShapeKit()
    string2.setPart("shape", coin.SoCylinder())
    string2.set("shape { radius .05 height 2}")
    string2.set("transform { translation 1.5 -1 0 } ")
    string2.set("transform { center 0 1 0 } ")
    beam.setPart("childList[1]", string2)

    tray1 = coin.SoShapeKit()
    tray1.setPart("shape", coin.SoCylinder())
    tray1.set("shape { radius .75 height .1 }")
    tray1.set("transform { translation 0 -1 0 } ")
    string1.setPart("childList[0]", tray1)

    tray2 = coin.SoShapeKit()
    tray2.setPart("shape", coin.SoCylinder())
    tray2.set("shape { radius .75 height .1 }")
    tray2.set("transform { translation 0 -1 0 } ")
    string2.setPart("childList[0]", tray2)

    # Add EventCallback coin.so Balance Responds to Events
    myCallbackNode = coin.SoEventCallback()
    myCallbackNode.addEventCallback(coin.SoKeyboardEvent.getClassTypeId(),
                                    tipTheBalance, support)
    support.setPart("callbackList[0]", myCallbackNode)

    # Add Instructions as Text in the Scene...
    myText = coin.SoShapeKit()
    myText.setPart("shape", coin.SoText2())
    myText.set("shape { string \"Press Left or Right Arrow Key\" }")
    myText.set("shape { justification CENTER }")
    myText.set("font { name \"Helvetica-Bold\" }")
    myText.set("font { size 16.0 }")
    myText.set("transform { translation 0 -2 0 }")
    myScene.setPart("childList[1]", myText)

    view = Gui.ActiveDocument.ActiveView
    sg = view.getSceneGraph()
    sg.addChild(myScene)
