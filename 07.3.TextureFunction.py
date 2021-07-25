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
# chapter 7, example 3.
#
# This example illustrates using texture functions to
# generate texture coordinates on a sphere.
# It draws three texture mapped spheres, each with a 
# different repeat frequency as defined by the fields of the 
# coin.SoTextureCoordinatePlane node.
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

def TextureFunc():

    root = coin.SoSeparator()

    # Choose a texture.
    faceTexture = coin.SoTexture2()
    root.addChild(faceTexture)
    faceTexture.filename = "E:\\TEMP\\fix some drawing\\Mentor_Freecad\\sillyFace.rgb"           #TODO: FIXME: Change path

    # Make the diffuse color pure white
    myMaterial = coin.SoMaterial()
    myMaterial.diffuseColor = (1,1,1)
    root.addChild(myMaterial)

    # This texture2Transform centers the texture about (0,0,0) 
    myTexXf = coin.SoTexture2Transform()
    myTexXf.translation = (.5,.5)
    root.addChild(myTexXf)

    # Define a texture coordinate plane node.  This one will 
    # repeat with a frequency of two times per unit length.
    # Add a sphere for it to affect.
    texPlane1 = coin.SoTextureCoordinatePlane()
    texPlane1.directionS = (2,0,0)
    texPlane1.directionT = (0,2,0)
    root.addChild(texPlane1)
    root.addChild(coin.SoSphere())

    # A translation node for spacing the three spheres.
    myTranslation = coin.SoTranslation()
    myTranslation.translation = (2.5,0,0)

    # Create a second sphere with a repeat frequency of 1.
    texPlane2 = coin.SoTextureCoordinatePlane()
    texPlane2.directionS = (1,0,0)
    texPlane2.directionT = (0,1,0)
    root.addChild(myTranslation)
    root.addChild(texPlane2)
    root.addChild(coin.SoSphere())

    # The third sphere has a repeat frequency of .5
    texPlane3 = coin.SoTextureCoordinatePlane()
    texPlane3.directionS = (.5,0,0)
    texPlane3.directionT = (0,.5,0)
    root.addChild(myTranslation)
    root.addChild(texPlane3)
    root.addChild(coin.SoSphere())
    view = Gui.ActiveDocument.ActiveView
    sg = view.getSceneGraph()
    sg.addChild(root)
