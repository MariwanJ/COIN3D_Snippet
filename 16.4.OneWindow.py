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
# chapter 16, example 4.
#
# This example builds a render area and Material Editor within 
# a window supplied by the application. It uses a Motif form 
# widget to lay both components inside the same window.  
# It attaches the editor to the material of an object.
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

#Warning:  Some of the code cannot be fixed here. 
 
def main():
    # Initialize Inventor and Qt
    #myWindow = coin.SoGui.init(sys.argv[0])
   
    # Build the form to hold both components
    #myForm = QtCreateWidget("Form", xmFormWidgetClass, myWindow, None, 0)
   
    ## Build the render area and Material Editor
    #myRenderArea = coin.SoGuiRenderArea(myForm)
    #myRenderArea.setSize(coin.SbVec2s(200, 200))
    #myEditor = coin.SoGuiMaterialEditor(myForm)
   
    # Layout the components within the form
    #args = []
    #QtGui.QtSetArg(args[0], XmNtopAttachment,    XmATTACH_FORM)
    #QtGui.QtSetArg(args[1], XmNbottomAttachment, XmATTACH_FORM)
    #QtGui.QtSetArg(args[2], XmNleftAttachment,   XmATTACH_FORM) 
    #QtGui.QtSetArg(args[3], XmNrightAttachment,  XmATTACH_POSITION)
    #QtGui.QtSetArg(args[4], XmNrightPosition,    40)
    #QtGui.QtSetValues(myRenderArea.getWidget(), args, 5)
    #QtGui.QtSetArg(args[2], XmNrightAttachment,  XmATTACH_FORM) 
    #QtGui.QtSetArg(args[3], XmNleftAttachment,   XmATTACH_POSITION)
    #QtGui.QtSetArg(args[4], XmNleftPosition,     41) 
    #QtGui.QtSetValues(myEditor.getWidget(), args, 5)
    
    # Create a scene graph
    root = coin.SoSeparator()
    myCamera = coin.SoPerspectiveCamera()
    myMaterial = coin.SoMaterial()
   
    myCamera.position = (0.212482, -0.881014, 2.5)
    myCamera.heightAngle = 22/7/4
    root.addChild(myCamera)
    root.addChild(coin.SoDirectionalLight())
    root.addChild(myMaterial)

    # Read the geometry from a file and add to the scene
    myInput = coin.SoInput()
    if not myInput.openFile("E:\\TEMP\\fix some drawing\\Mentor_Freecad\\dogDish.iv"):  #TODO : FIXME: Change path.
        sys.exit(1)
    geomObject = coin.SoDB.readAll(myInput)
    if geomObject == None:
        sys.exit(1)
    root.addChild(geomObject)

    view = Gui.ActiveDocument.ActiveView
    sg = view.getSceneGraph()
    sg.addChild(root)
