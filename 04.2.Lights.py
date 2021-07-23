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
# chapter 4, example 2.
#
# Lights example.  
# Read in an object from a file.
# Use the ExaminerViewer to view it with two light coin.Sources.
# The red directional light doesn't move; the green point 
# light is moved back and forth using a shuttle node.
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


def Lights():
    root = coin.SoSeparator()

    # Add a directional light
    myDirLight = coin.SoDirectionalLight()
    myDirLight.direction = (0, -1, -1)
    myDirLight.color = (1, 0, 0)
    root.addChild(myDirLight)

    # Put the shuttle and the light below a transform separator.
    # A transform separator pushes and pops the transformation 
    # just like a separator node, but other aspects of the state 
    # are not pushed and popped. coin.So the shuttle's translation 
    # will affect only the light. But the light will shine on 
    # the rest of the scene.
    myTransformSeparator = coin.SoTransformSeparator()
    root.addChild(myTransformSeparator)

    # A shuttle node translates back and forth between the two
    # fields translation0 and translation1.  
    # This moves the light.
    myShuttle = coin.SoShuttle()
    myTransformSeparator.addChild(myShuttle)
    myShuttle.translation0 = (-2, -1, 3)
    myShuttle.translation1 = ( 1,  2, -3)

    # Add the point light below the transformSeparator
    myPointLight = coin.SoPointLight()
    myTransformSeparator.addChild(myPointLight)
    myPointLight.color = (0, 1, 0)

    root.addChild(coin.SoCone())

    view = Gui.ActiveDocument.ActiveView
    sg = view.getSceneGraph()
    sg.addChild(root)
