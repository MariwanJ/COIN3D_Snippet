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
# chapter 9, example 2.
#
# Using the offscreen renderer to generate a texture map.
# Generate simple scene and grab the image to use as
# a texture map.
#

from __future__ import print_function
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


def generateTextureMap(root, texture, textureWidth, textureHeight):
    myViewport = coin.SbViewportRegion(textureWidth, textureHeight)

    # Render the scene
    myRenderer = coin.SoOffscreenRenderer(myViewport)
    myRenderer.setBackgroundColor(coin.SbColor(0.3, 0.3, 0.3))
    if not myRenderer.render(root):
        del myRenderer
        return False

    # Generate the texture
    texture.image.setValue(coin.SbVec2s(textureWidth, textureHeight),
                           coin.SoOffscreenRenderer.RGB, myRenderer.getBuffer())

    del myRenderer
    return True

def TextureExecute():
    # Make a scene from reading in a file
    texRoot = coin.SoSeparator()
    input = coin.SoInput()

    input.openFile("E:\\TEMP\\fix some drawing\\Mentor_Freecad\\jumpyMan.iv")           #TODO : Change the path and file name if you want
    result = coin.SoDB.readAll(input)

    myCamera = coin.SoPerspectiveCamera()
    rot = coin.SoRotationXYZ()
    rot.axis = coin.SoRotationXYZ.X
    rot.angle = 22/7/2
    myCamera.position = (-0.2, -0.2, 2.0)
    myCamera.scaleHeight(0.4)
    texRoot.addChild(myCamera)
    texRoot.addChild(coin.SoDirectionalLight())
    texRoot.addChild(rot)
    texRoot.addChild(result)

    # Generate the texture map
    texture = coin.SoTexture2()
    if generateTextureMap(texRoot, texture, 64, 64):
        print("Successfully generated texture map")
    else:
        print("Could not generate texture map")

    # Make a scene with a cube and apply the texture to it
    root = coin.SoSeparator()
    root.addChild(texture)
    root.addChild(coin.SoCube())
    
    view = Gui.ActiveDocument.ActiveView
    sg = view.getSceneGraph()
    sg.addChild(root)