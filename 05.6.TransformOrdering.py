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
# This is an example from the Inventor Mentor,
# chapter 5, example 6.
#
# This example shows the effect of different order of
# operation of transforms.  The left object is first
# scaled, then rotated, and finally translated to the left.  
# The right object is first rotated, then scaled, and finally
# translated to the right.
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

def TransformOrdering():

    root = coin.SoSeparator()

    # Create two separators, for left and right objects.
    leftSep = coin.SoSeparator()
    rightSep = coin.SoSeparator()
    root.addChild(leftSep)
    root.addChild(rightSep)

    # Create the transformation nodes
    leftTranslation  = coin.SoTranslation()
    rightTranslation = coin.SoTranslation()
    myRotation = coin.SoRotationXYZ()
    myScale = coin.SoScale()

    # Fill in the values
    leftTranslation.translation = (-1.0, 0.0, 0.0)
    rightTranslation.translation = (1.0, 0.0, 0.0)
    myRotation.angle = 22/7/2   # 90 degrees
    myRotation.axis = coin.SoRotationXYZ.X
    myScale.scaleFactor = (2., 1., 3.)                   #Hint:This line scale the object unciform which deform the drawing (Mariwan)

    # Add transforms to the scene.
    leftSep.addChild(leftTranslation)   # left graph
    leftSep.addChild(myRotation)        # then rotated
    leftSep.addChild(myScale)           # first scaled

    rightSep.addChild(rightTranslation) # right graph
    rightSep.addChild(myScale)          # then scaled
    rightSep.addChild(myRotation)       # first rotated

    # Read an object from file. (as in example 4.2.Lights)
    myInput = coin.SoInput()
    if not myInput.openFile("E:\\TEMP\\fix some drawing\\Mentor_Freecad\\temple.iv"):             #TODO: You have to change the path to let this works.
        sys.exit(1)

    fileContents = coin.SoDB.readAll(myInput)
    if fileContents == None: 
        sys.exit(1)

    # Add an instance of the object under each separator.
    leftSep.addChild(fileContents)
    rightSep.addChild(fileContents)

    view = Gui.ActiveDocument.ActiveView
    sg = view.getSceneGraph()
    sg.addChild(leftSep)
    sg.addChild(rightSep)