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
# chapter 13, example 4.
#
# Time counter engine.
# The output from an time counter engine is used to control
# horizontal and vertical motion of a figure object.
# The resulting effect is that the figure jumps across
# the screen.
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
from PySide import QtGui, QtCore  # https://www.freecadweb.org/wiki/PySide

def TimeCounterEx():

    root = coin.SoSeparator()
    
    # Add a camera and light
    myCamera = coin.SoPerspectiveCamera()
    myCamera.position = (-8.0, -7.0, 20.0)
    myCamera.heightAngle = 22/7/2.5
    myCamera.nearDistance = 15.0
    myCamera.farDistance = 25.0
    root.addChild(myCamera)
    root.addChild(coin.SoDirectionalLight())

##############################################################
# CODE FOR The Inventor Mentor STARTS HERE

    # Set up transformations
    jumpTranslation = coin.SoTranslation()
    root.addChild(jumpTranslation)
    initialTransform = coin.SoTransform()
    initialTransform.translation = (-20., 0., 0.)
    initialTransform.scaleFactor = (40., 40., 40.)
    initialTransform.rotation.setValue(coin.SbVec3f(1,0,0), 22/7/2.)
    root.addChild(initialTransform)

    # Read the man object from a file and add to the scene
    myInput = coin.SoInput()
    myInput.openFile("E:\\TEMP\\fix some drawing\\Mentor_Freecad\\jumpyMan.iv")       #TODO: FIXME: CHANGE ME 
    manObject = coin.SoDB.readAll(myInput)
    if manObject == None:
        sys.exit(1)
    root.addChild(manObject)

    # Create two counters, and connect to X and Y translations.
    # The Y counter is small and high frequency.
    # The X counter is large and low frequency.
    # This results in small jumps across the screen, 
    # left to right, again and again and again and ....
    jumpHeightCounter = coin.SoTimeCounter()
    jumpWidthCounter = coin.SoTimeCounter()
    jump = coin.SoComposeVec3f()

    jumpHeightCounter.max = 4
    jumpHeightCounter.frequency = 1.5
    jumpWidthCounter.max = 40
    jumpWidthCounter.frequency = 0.15

    jump.x.connectFrom(jumpWidthCounter.output)
    jump.y.connectFrom(jumpHeightCounter.output)
    jumpTranslation.translation.connectFrom(jump.vector)

    view = Gui.ActiveDocument.ActiveView
    sg = view.getSceneGraph()
    sg.addChild(root)
    