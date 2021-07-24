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
# chapter 9, example 3.
#
# Search Action example.
# Read in a scene from a file.
# Search through the scene looking for a light.
# If none exists, add a directional light to the scene
# and print out the modified scene.
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

def Search():
    # Initialize Inventor
    # coin.SoDB.init() invoked automatically upon coin module import
    
    # Open and read input scene graph
    sceneInput = coin.SoInput()
    if not sceneInput.openFile("E:\\TEMP\\fix some drawing\\Mentor_Freecad\\bird.iv"):   #TODO Change path and file name      
        return 1

    root = coin.SoDB.readAll(sceneInput)
    if root == None:
        return 1

##############################################################
# CODE FOR The Inventor Mentor STARTS HERE

    mySearchAction = coin.SoSearchAction()

    # Look for first existing light derived from class coin.SoLight
    mySearchAction.setType(coin.SoLight.getClassTypeId())
    mySearchAction.setInterest(coin.SoSearchAction.FIRST)
    
    mySearchAction.apply(root)
    if mySearchAction.getPath() == None: # No lights found
        # Add a default directional light to the scene
        myLight = coin.SoDirectionalLight()
        root.insertChild(myLight, 0)

# CODE FOR The Inventor Mentor ENDS HERE
##############################################################

    myWriteAction = coin.SoWriteAction()
    myWriteAction.apply(root)

    view = Gui.ActiveDocument.ActiveView
    sg = view.getSceneGraph()
    sg.addChild(root)