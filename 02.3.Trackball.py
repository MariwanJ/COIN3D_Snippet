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
# chapter 2, example 3.
#
# Use the trackball manipulator to edit/rotate a red cone
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

#Great Example how you can use this to rotate objects :)
def Trackball():

    root = coin.SoSeparator()

    root.addChild(coin.SoDirectionalLight()) # child 1
    root.addChild(coin.SoTrackballManip())   # child 2

    myMaterial = coin.SoMaterial()
    myMaterial.diffuseColor = (1.0, 0.0, 0.0)
    root.addChild(myMaterial)
    root.addChild(coin.SoCone())


    view = Gui.ActiveDocument.ActiveView
    sg = view.getSceneGraph()
    sg.addChild(root)
