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
# chapter 14, example 2.
#
# Use nodekits to create a scene with a desk into an 
# coin.SoWrapperKit.  Then, add a material editor for the desk and 
# a light editor on the light.
# 
# The scene is organized using an coin.SoSceneKit, which contains
# lists for grouping lights (lightList), cameras (cameraList), 
# and objects (childList) in a scene.
# 
# Once the scene is created, a material editor is attached to 
# the wrapperKit's 'material' part, and a directional light editor
# is attached to the light's 'directionalLight' part.
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


#WARNING: NOT WORKING : TODO: FIXME:

def EditorsExec():

    # SCENE!
    myScene = coin.SoSceneKit()

    # LIGHTS! Add an coin.SoLightKit to the "lightList." The 
    # coin.SoLightKit creates an coin.SoDirectionalLight by default.
    myScene.setPart("lightList[0]", coin.SoLightKit())

    # CAMERA!! Add an coin.SoCameraKit to the "cameraList." The 
    # coin.SoCameraKit creates an coin.SoPerspectiveCamera by default.
    myScene.setPart("cameraList[0]", coin.SoCameraKit())
    myScene.setCameraNumber(0)

    # Read an object from file. 
    myInput = coin.SoInput()
    if not myInput.openFile("E:\\TEMP\\fix some drawing\\Mentor_Freecad\\desk.iv"):   #TODO: FIXME: CHANGE PATH
        sys.exit(1)
    fileContents = coin.SoDB.readAll(myInput)
    if fileContents == None: 
        sys.exit(1)

    # OBJECT!! Create an coin.SoWrapperKit and set its contents to
    # be what you read from file.
    myDesk =coin.SoWrapperKit()
    myDesk.setPart("contents", fileContents)
    myScene.setPart("childList[0]", myDesk)

    # Give the desk a good starting color
    myDesk.set("material { diffuseColor .8 .3 .1 }")

    # MATERIAL EDITOR!!  Attach it to myDesk's material node.
    # Use the coin.So_GET_PART macro to get this part from myDesk.
    try:
        mtlEditor = coin.SoGuiMaterialEditor()
    except:
        print("The coin.SoGuiMaterialEditor node has not been implemented in the " + \
              "coin.SoGui bindings of Coin!")
        sys.exit(1)
    mtl = coin.So_GET_PART(myDesk,"material",coin.SoMaterial())
    mtlEditor.attach(mtl)
    mtlEditor.setTitle("Material of Desk")
    mtlEditor.show()

    # DIRECTIONAL LIGHT EDITOR!! Attach it to the 
    # coin.SoDirectionalLight node within the coin.SoLightKit we made.
    try:
        ltEditor = coin.SoGuiDirectionalLightEditor()
    except:
        print("The coin.SoGuiDirectionalLightEditor node has not been implemented in the " + \
              "coin.SoGui bindings of Coin!")
        sys.exit(1)        
    ltPath = myScene.createPathToPart("lightList[0].light", True)
    ltEditor.attach(ltPath)
    ltEditor.setTitle("Lighting of Desk")
    ltEditor.show()
   
    view = Gui.ActiveDocument.ActiveView
    sg = view.getSceneGraph()
    sg.addChild(myScene)
    