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
# chapter 16, example 3.
#
# This example builds a render area in a window supplied by
# the application and a Material Editor in its own window.
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


def AttachEditorExe():
    # Build the material editor in its own window
    try:
        myEditor = coin.SoGuiMaterialEditor()
    except:
        print("The coin.SoGuiMaterialEditor node has not been implemented in the " + \
              "coin.SoGui bindings of Coin!")
        sys.exit(1)
   
    # Create a scene graph
    root =coin.SoSeparator()
    myCamera = coin.SoPerspectiveCamera()
    myMaterial = coin.SoMaterial()
   
    myCamera.position = (0.212482, -0.881014, 2.5)
    myCamera.heightAngle = 22/7/4
    root.addChild(myCamera)
    root.addChild(coin.SoDirectionalLight())
    root.addChild(myMaterial)

    # Read the geometry from a file and add to the scene
    myInput = coin.SoInput()
    if not myInput.openFile("E:\\TEMP\\fix some drawing\\Mentor_Freecad\\dogDish.iv"):   #todo: FIXME: change path
        sys.exit(1)
    geomObject = coin.SoDB.readAll(myInput)
    if geomObject == None:
        sys.exit(1)
    root.addChild(geomObject)
    view = Gui.ActiveDocument.ActiveView
    sg = view.getSceneGraph()
    sg.addChild(root)
