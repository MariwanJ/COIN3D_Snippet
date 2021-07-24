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
# chapter 13, example 7.
#
# A calculator engine computes a closed, planar curve.
# The output from the engine is connected to the translation
# applied to a flower object, which consequently moves
# along the path of the curve.
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

def CalculatorExe():

    root = coin.SoSeparator()

    # Add a camera and light
    myCamera = coin.SoPerspectiveCamera()
    myCamera.position = (-0.5, -3.0, 19.0)
    myCamera.nearDistance = 10.0
    myCamera.farDistance = 26.0
    root.addChild(myCamera)
    root.addChild(coin.SoDirectionalLight())

    # Rotate scene slightly to get better view
    globalRotXYZ = coin.SoRotationXYZ()
    globalRotXYZ.axis = coin.SoRotationXYZ.X
    globalRotXYZ.angle = 22/7/7
    root.addChild(globalRotXYZ)

    # Read the background path from a file and add to the group
    myInput = coin.SoInput()
    if not myInput.openFile("E:\\TEMP\\fix some drawing\\Mentor_Freecad\\flowerPath.iv"): #TODO: FIXME : Change the path.
        sys.exit(1)
    flowerPath = coin.SoDB.readAll(myInput)
    if flowerPath == None: sys.exit(1)
    root.addChild(flowerPath)

#############################################################
# CODE FOR The Inventor Mentor STARTS HERE  

    # Flower group
    flowerGroup = coin.SoSeparator()
    root.addChild(flowerGroup)

    # Read the flower object from a file and add to the group
    if not myInput.openFile("E:\\TEMP\\fix some drawing\\Mentor_Freecad\\flower.iv"):     #TODO: FIXME : Change the path.
        sys.exit(1)
    flower = coin.SoDB.readAll(myInput)
    if flower == None: sys.exit(1)

    # Set up the flower transformations
    danceTranslation = coin.SoTranslation()
    initialTransform = coin.SoTransform()
    flowerGroup.addChild(danceTranslation)
    initialTransform.scaleFactor = (10., 10., 10.)
    initialTransform.translation = (0., 0., 5.)
    flowerGroup.addChild(initialTransform)
    flowerGroup.addChild(flower)

    # Set up an engine to calculate the motion path:
    # r = 5*cos(5*theta) x = r*cos(theta) z = r*sin(theta)
    # Theta is incremented using a time counter engine,
    # and converted to radians using an expression in
    # the calculator engine.
    calcXZ = coin.SoCalculator()
    thetaCounter = coin.SoTimeCounter()

    thetaCounter.max = 360
    thetaCounter.step = 4
    thetaCounter.frequency = 0.075

    calcXZ.a.connectFrom(thetaCounter.output)    
    calcXZ.expression.set1Value(0, "ta=a*22/7/180") # theta
    calcXZ.expression.set1Value(1, "tb=5*cos(5*ta)") # r
    calcXZ.expression.set1Value(2, "td=tb*cos(ta)") # x 
    calcXZ.expression.set1Value(3, "te=tb*sin(ta)") # z 
    calcXZ.expression.set1Value(4, "oA=vec3f(td,0,te)") 
    danceTranslation.translation.connectFrom(calcXZ.oA)
    
    view = Gui.ActiveDocument.ActiveView
    sg = view.getSceneGraph()
    sg.addChild(root)
    