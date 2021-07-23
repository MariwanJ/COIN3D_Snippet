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
# chapter 4, example 1.
#
# Camera example.  
# A blinker node is used to switch between three 
# different views of the same scene. The cameras are 
# switched once per second.
#
####################################################################
#         Modified to be compatible with  FreeCAD                  #
#                                                                  #
# Author : Mariwan Jalal  mariwan.jalal@gmail.com                  #
####################################################################

import os,sys
import FreeCAD as App
import FreeCADGui as Gui
import pivy.coin as coin

def Cameras():
    root = coin.SoSeparator()

    # Create a blinker node and put it in the scene. A blinker
    # switches between its children at timed intervals.
    myBlinker = coin.SoBlinker()
    root.addChild(myBlinker)

    # Create three cameras. Their positions will be set later.
    # This is because the viewAll method depends on the size
    # of the render area, which has not been created yet.
    orthoViewAll = coin.SoOrthographicCamera()
    perspViewAll = coin.SoPerspectiveCamera()
    perspOffCenter = coin.SoPerspectiveCamera()
    myBlinker.addChild(orthoViewAll)
    myBlinker.addChild(perspViewAll)
    myBlinker.addChild(perspOffCenter)

    # Create a light
    root.addChild(coin.SoDirectionalLight())

    # Read the object from a file and add to the scene
    myInput = coin.SoInput()
    # You have to give the file path                                TODO: FIX THE PATH!!!!
    if not myInput.openFile("E:\\TEMP\\fix some drawing\\Mentor_Freecad\\parkbench.iv"):
        sys.exit(1)

    fileContents = coin.SoDB.readAll(myInput)
    if fileContents == None:
        sys.exit(1)

    myMaterial = coin.SoMaterial()
    myMaterial.diffuseColor = (0.8, 0.23, 0.03) 
    root.addChild(myMaterial)
    root.addChild(fileContents)

    view = Gui.ActiveDocument.ActiveView
    sg = view.getSceneGraph()
    sg.addChild(root)
