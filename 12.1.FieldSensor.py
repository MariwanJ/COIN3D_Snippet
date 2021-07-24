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
# chapter 12, example 1.
#
# Sense changes to a viewer's camera's position.
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


#WARNING:  NOT WORKING WELL DON'T KNOW !! TODO: FIXME: 


# Callback that reports whenever the viewer's position changes.
def cameraChangedCB(viewerCamera, sensor):
    cameraPosition = viewerCamera.position.getValue()
    print("Camera position: (%g,%g,%g)" % (cameraPosition[0], cameraPosition[1],cameraPosition[2]))
    
    
    
def FieldSensorEx():
    inputFile = coin.SoInput()
    inputFile.openFile("E:\\TEMP\\fix some drawing\\Mentor_Freecad\\luxo.vi")          #CHANGE ME  TODO: FIXME:
    
    root = coin.SoDB.readAll(inputFile)
    view = Gui.ActiveDocument.ActiveView
    sg = view.getSceneGraph()
    sg.addChild(root)