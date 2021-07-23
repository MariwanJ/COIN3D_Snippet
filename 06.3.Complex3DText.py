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

"""
This is an example from the Inventor Mentor,
chapter 6, example 3.

This example renders arguments as text within an
ExaminerViewer.  It is a little fancier than 6.2.
"""
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

def complexText3D():

    root = coin.SoGroup()

    # Let's make the front of the text white,
    # and the sides and back shiny yellow
    myMaterial = coin.SoMaterial()
    # diffuse
    colors = [coin.SbColor()] * 3
    colors[0] = coin.SbColor(1, 1, 1)
    colors[1] = coin.SbColor(1, 1, 0)
    colors[2] = coin.SbColor(1, 1, 0)
    myMaterial.diffuseColor.setValues(0, 3, colors)

    # specular
    colors[0].setValue(1, 1, 1)
    """
    # Note: Inventor 2.1 doesn't support multiple specular colors.
    # colors[1].setValue(1, 1, 0)
    # colors[2].setValue(1, 1, 0)
    # myMaterial.specularColor.setValues(0, 3, colors)
    """
    myMaterial.specularColor.setValue(colors[0])
    myMaterial.shininess.setValue(.1)
    root += myMaterial

    # Choose a font likely to exist.
    myFont = coin.SoFont()
    # times new roman coin.Somehow changes the normals of the text and coin.So the beveling
    # is done in the wrong directions. Commenting out this line coin.Solves this issue here

    # myFont.name = "times" # "Times-Roman"
    root += myFont

    # Specify a beveled cross-section for the text
    myProfileCoords = coin.SoProfileCoordinate2()
    coords = [coin.SbVec2f()] * 4
    coords[0] = coin.SbVec2f(.00, .00)
    coords[1] = coin.SbVec2f(.25, .25)
    coords[2] = coin.SbVec2f(1.25, .25)
    coords[3] = coin.SbVec2f(1.50, .00)
    myProfileCoords.point.setValues(0, 4, coords)
    root += myProfileCoords

    myLinearProfile = coin.SoLinearProfile()
    index = (0, 1, 2, 3)
    myLinearProfile.index.setValues(0, 4, index)
    root += myLinearProfile

    # Set the material binding to PER_PART
    myMaterialBinding = coin.SoMaterialBinding()
    myMaterialBinding.value = coin.SoMaterialBinding.PER_PART
    root += myMaterialBinding

    # Add the text
    myText3 = coin.SoText3()
    #myText3.string = "Beveled Text"
    myText3.string = "Design456 COIN3D"
    myText3.justification = coin.SoText3.CENTER
    myText3.parts = coin.SoText3.ALL

    root += myText3
    view = Gui.ActiveDocument.ActiveView
    sg = view.getSceneGraph()
    sg.addChild(root)
