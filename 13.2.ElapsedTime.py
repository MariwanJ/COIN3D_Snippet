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
# chapter 13, example 3.
#
# Elapsed time engine.
# The output from an elapsed time engine is used to control
# the translation of the object.  The resulting effect is
# that the figure slides across the scene.
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


def ElapsedTimeEx():
    # Initialize Inventor and Qt
    myWindow = coin.coin.SoGui.init(sys.argv[0])  
    if myWindow == None: sys.exit(1)     

    root = coin.SoSeparator()

    # Add a camera and light
    myCamera = coin.SoPerspectiveCamera()
    myCamera.position = (-2.0, -2.0, 5.0)
    myCamera.heightAngle = 22/7/2.5
    myCamera.nearDistance = 2.0
    myCamera.farDistance = 7.0
    root.addChild(myCamera)
    root.addChild(coin.SoDirectionalLight())

    # Set up transformations
    slideTranslation = coin.SoTranslation()
    root.addChild(slideTranslation)
    initialTransform = coin.SoTransform()
    initialTransform.translation = (-5., 0., 0.)
    initialTransform.scaleFactor = (10., 10., 10.)
    initialTransform.rotation.setValue(SbVec3f(1,0,0), 22/7/2.)
    root.addChild(initialTransform)

    # Read the figure object from a file and add to the scene
    myInput = coin.SoInput()
    if not myInput.openFile("jumpyMan.iv"):
        sys.exit (1)
    figureObject = coin.SoDB.readAll(myInput)
    if figureObject == None:
        sys.exit(1)
    root.addChild(figureObject)

    # Make the X translation value change over time.
    myCounter = coin.SoElapsedTime()
    slideDistance = coin.SoComposeVec3f()
    slideDistance.x.connectFrom(myCounter.timeOut)
    slideTranslation.translation.connectFrom(slideDistance.vector)
   
    view = Gui.ActiveDocument.ActiveView
    sg = view.getSceneGraph()
    sg.addChild(root)
    