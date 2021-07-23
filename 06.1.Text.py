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
# chapter 6, example 1.
#
# This example renders a globe and uses 2D text to label the
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

def Text():

    root = coin.SoGroup()

    # Choose a font
    myFont = coin.SoFont()
    myFont.name = "Times-Roman"
    myFont.size = 24.0
    root.addChild(myFont)

    # Add the globe, a sphere with a texture map.
    # Put it within a separator.
    sphereSep = coin.SoSeparator()
    myTexture2 = coin.SoTexture2()
    sphereComplexity = coin.SoComplexity()
    sphereComplexity.value = 0.55
    root.addChild(sphereSep)
    sphereSep.addChild(myTexture2)
    sphereSep.addChild(sphereComplexity)
    sphereSep.addChild(coin.SoSphere())
    myTexture2.filename = "globe.rgb"

    # Add Text2 for AFRICA, translated to proper location.
    africaSep = coin.SoSeparator()
    africaTranslate = coin.SoTranslation()
    africaText = coin.SoText2()
    africaTranslate.translation = (.25,.0,1.25)
    africaText.string = "AFRICA"
    root.addChild(africaSep)
    africaSep.addChild(africaTranslate)
    africaSep.addChild(africaText)

    # Add Text2 for ASIA, translated to proper location.
    asiaSep = coin.SoSeparator()
    asiaTranslate = coin.SoTranslation()
    asiaText = coin.SoText2()
    asiaTranslate.translation = (.8,.8,0)
    asiaText.string = "ASIA"
    root.addChild(asiaSep)
    asiaSep.addChild(asiaTranslate)
    asiaSep.addChild(asiaText)
    view = Gui.ActiveDocument.ActiveView
    sg = view.getSceneGraph()
    sg.addChild(root)
