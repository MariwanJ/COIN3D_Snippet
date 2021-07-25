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
# chapter 7, example 2.
#
# This example illustrates using texture coordinates on
# a Face Set.
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

# set this variable to 0 if you want to use the other method
IV_STRICT = 1

def TextureCoord():

    root = coin.SoSeparator()
    
    # Choose a texture
    brick = coin.SoTexture2()
    root.addChild(brick)
    brick.filename = "E:\\TEMP\\fix some drawing\\Mentor\\brick.1.rgb"     #TODO : FIXME : CHANGE PATH

    if IV_STRICT:
        # This is the preferred code for Inventor 2.1 

        # Using the new coin.SoVertexProperty node is more efficient
        myVertexProperty = coin.SoVertexProperty()

        # Define the square's spatial coordinates
        myVertexProperty.vertex.set1Value(0, coin.SbVec3f(-3, -3, 0))
        myVertexProperty.vertex.set1Value(1, coin.SbVec3f( 3, -3, 0))
        myVertexProperty.vertex.set1Value(2, coin.SbVec3f( 3,  3, 0))
        myVertexProperty.vertex.set1Value(3, coin.SbVec3f(-3,  3, 0))

        # Define the square's normal
        myVertexProperty.normal.set1Value(0, coin.SbVec3f(0, 0, 1))

        # Define the square's texture coordinates
        myVertexProperty.texCoord.set1Value(0, coin.SbVec2f(0, 0))
        myVertexProperty.texCoord.set1Value(1, coin.SbVec2f(1, 0))
        myVertexProperty.texCoord.set1Value(2, coin.SbVec2f(1, 1))
        myVertexProperty.texCoord.set1Value(3, coin.SbVec2f(0, 1))

        # coin.SoTextureCoordinateBinding node is now obSolete--in Inventor 2.1,
        # texture coordinates will always be generated if none are 
        # provided.
        #
        # tBind = coin.SoTextureCoordinateBinding()
        # root.addChild(tBind)
        # tBind.value(coin.SoTextureCoordinateBinding.PER_VERTEX)
        #
        # Define normal binding
        myVertexProperty.normalBinding = coin.SoNormalBinding.OVERALL

        # Define a FaceSet
        myFaceSet = coin.SoFaceSet()
        root.addChild(myFaceSet)
        myFaceSet.numVertices.set1Value(0, 4)

        myFaceSet.vertexProperty.setValue(myVertexProperty)

    else:
        # Define the square's spatial coordinates
        coord = coin.SoCoordinate3()
        root.addChild(coord)
        coord.point.set1Value(0, coin.SbVec3f(-3, -3, 0))
        coord.point.set1Value(1, coin.SbVec3f( 3, -3, 0))
        coord.point.set1Value(2, coin.SbVec3f( 3,  3, 0))
        coord.point.set1Value(3, coin.SbVec3f(-3,  3, 0))

        # Define the square's normal
        normal = coin.SoNormal()
        root.addChild(normal)
        normal.vector.set1Value(0, coin.SbVec3f(0, 0, 1))

        # Define the square's texture coordinates
        texCoord = coin.SoTextureCoordinate2()
        root.addChild(texCoord)
        texCoord.point.set1Value(0, coin.SbVec2f(0, 0))
        texCoord.point.set1Value(1, coin.SbVec2f(1, 0))
        texCoord.point.set1Value(2, coin.SbVec2f(1, 1))
        texCoord.point.set1Value(3, coin.SbVec2f(0, 1))

        # Define normal binding
        nBind = coin.SoNormalBinding()
        root.addChild(nBind)
        nBind.value = coin.SoNormalBinding.OVERALL

        # coin.SoTextureCoordinateBinding node is now obSolete--in Inventor 2.1,
        # texture coordinates will always be generated if none are 
        # provided.
        #
        # tBind = coin.SoTextureCoordinateBinding()
        # root.addChild(tBind)
        # tBind.value.setValue(coin.SoTextureCoordinateBinding.PER_VERTEX)
        #

        # Define a FaceSet
        myFaceSet = coin.SoFaceSet()
        root.addChild(myFaceSet)
        myFaceSet.numVertices.set1Value(0, 4)
    view = Gui.ActiveDocument.ActiveView
    sg = view.getSceneGraph()
    sg.addChild(root)
