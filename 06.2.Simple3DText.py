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
# chapter 6, example 2.
#
# This example renders a globe and uses 3D text to label the
# continents Africa and Asia.
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

def Simple3DText():
    root = coin.SoGroup()

    # Choose a font
    myFont = coin.SoFont()
    myFont.name = "Times-Roman"
    myFont.size = .2
    root.addChild(myFont)

    # We'll color the front of the text white, and the sides 
    # dark grey. coin.So use a materialBinding of PER_PART and
    # two diffuseColor values in the material node.
    myMaterial = coin.SoMaterial()
    myBinding = coin.SoMaterialBinding()
    myMaterial.diffuseColor.set1Value(0, coin.SbColor(1,1,1))
    myMaterial.diffuseColor.set1Value(1, coin.SbColor(.1,.1,.1))
    myBinding.value = coin.SoMaterialBinding.PER_PART
    root.addChild(myMaterial)
    root.addChild(myBinding)

    # Create the globe
    sphereSep = coin.SoSeparator()
    myTexture2 = coin.SoTexture2()
    sphereComplexity = coin.SoComplexity()
    sphereComplexity.value = 0.55
    root.addChild(sphereSep)
    sphereSep.addChild(myTexture2)
    sphereSep.addChild(sphereComplexity)
    sphereSep.addChild(coin.SoSphere())
    myTexture2.filename = "E:\\TEMP\\fix some drawing\\Mentor_Freecad\\globe.rgb"  #TODO: FIXME : CHANGE PATH

    # Add Text3 for AFRICA, transformed to proper location.
    africaSep = coin.SoSeparator()
    africaTransform = coin.SoTransform()
    africaText = coin.SoText3()
    africaTransform.rotation.setValue(coin.SbVec3f(0,1,0), .4)
    africaTransform.translation = (.25, .0, 1.25)
    africaText.parts = coin.SoText3.ALL
    africaText.string = "AFRICA"
    root.addChild(africaSep)
    africaSep.addChild(africaTransform)
    africaSep.addChild(africaText)

    # Add Text3 for ASIA, transformed to proper location.
    asiaSep = coin.SoSeparator()
    asiaTransform = coin.SoTransform()
    asiaText = coin.SoText3()
    asiaTransform.rotation.setValue(coin.SbVec3f(0,1,0), 1.5)
    asiaTransform.translation = (.8, .6, .5)
    asiaText.parts = coin.SoText3.ALL
    asiaText.string = "ASIA"
    root.addChild(asiaSep)
    asiaSep.addChild(asiaTransform)
    asiaSep.addChild(asiaText)
    
    view = Gui.ActiveDocument.ActiveView
    sg = view.getSceneGraph()
    sg.addChild(root)
