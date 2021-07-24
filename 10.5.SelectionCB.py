#!/usr/bin/env python

###
# Copyright (c) 2002-2007 Systems in Motion
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#

###
# This is an example from The Inventor Mentor,
# chapter 10, example 5.
#
# The scene graph has a sphere and a text 3D object. 
# A selection node is placed at the top of the scene graph. 
# When an object is selected, a selection callback is called
# to change the material color of that object.
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

#Warning: Didn't work for me .: TODO: FIXME:


# global data
textMaterial, sphereMaterial = [None]*2
reddish = (1.0, 0.2, 0.2)  # Color when selected
white   = (0.8, 0.8, 0.8)  # Color when not selected

# This routine is called when an object gets selected. 
# We determine which object was selected, and change 
# that objects material color.
def mySelectionCB(void, selectionPath):
    if selectionPath.getTail().isOfType(coin.SoText3.getClassTypeId()):
        textMaterial.diffuseColor.setValue(reddish)
    elif selectionPath.getTail().isOfType(coin.SoSphere.getClassTypeId()):
        sphereMaterial.diffuseColor.setValue(reddish)

# This routine is called whenever an object gets deselected. 
# We determine which object was deselected, and reset 
# that objects material color.
def myDeselectionCB(void, deselectionPath):
    if deselectionPath.getTail().isOfType(coin.SoText3.getClassTypeId()):
        textMaterial.diffuseColor = white
    elif deselectionPath.getTail().isOfType(coin.SoSphere.getClassTypeId()):
        sphereMaterial.diffuseColor = white

def SelectionCBExec():
    global textMaterial, sphereMaterial

    # Create and set up the selection node
    selectionRoot = coin.SoSelection()
    selectionRoot.policy = coin.SoSelection.SINGLE
    selectionRoot.addSelectionCallback(mySelectionCB)
    selectionRoot.addDeselectionCallback(myDeselectionCB)

    # Create the scene graph
    root = coin.SoSeparator()
    selectionRoot.addChild(root)

    myCamera = coin.SoPerspectiveCamera()
    root.addChild(myCamera)
    root.addChild(coin.SoDirectionalLight())

    # Add a sphere node
    sphereRoot = coin.SoSeparator()
    sphereTransform = coin.SoTransform()
    sphereTransform.translation = (17., 17., 0.)
    sphereTransform.scaleFactor = (8., 8., 8.)
    sphereRoot.addChild(sphereTransform)

    sphereMaterial = coin.SoMaterial()
    sphereMaterial.diffuseColor = (.8, .8, .8)
    sphereRoot.addChild(sphereMaterial)
    sphereRoot.addChild(coin.SoSphere())
    root.addChild(sphereRoot)

    # Add a text node
    textRoot = coin.SoSeparator()
    textTransform = coin.SoTransform()
    textTransform.translation = (0., -1., 0.)
    textRoot.addChild(textTransform)

    textMaterial = coin.SoMaterial()
    textMaterial.diffuseColor = (.8, .8, .8)
    textRoot.addChild(textMaterial)
    textPickStyle = coin.SoPickStyle()
    textPickStyle.style = coin.SoPickStyle.BOUNDING_BOX
    textRoot.addChild(textPickStyle)
    myText = coin.SoText3()
    myText.string = "rhubarb"
    textRoot.addChild(myText)
    root.addChild(textRoot)

    view = Gui.ActiveDocument.ActiveView
    sg = view.getSceneGraph()
    sg.addChild(root)

