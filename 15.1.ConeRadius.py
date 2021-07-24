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
# This is an example from the Inventor Mentor.
# chapter 15, example 1.
#
# Uses an coin.SoTranslate1Dragger to control the bottomRadius field 
# of an coin.SoCone.  The 'translation' field of the dragger is the 
# input to an coin.SoDecomposeVec3f engine. The engine extracts the
# x component from the translation. This extracted value is
# connected to the bottomRadius field of the cone.
#
####################################################################
#        Modified to be compatible with  FreeCAD                   #
#                                                                  #
# Author : Mariwan Jalal  mariwan.jalal@gmail.com                  #
####################################################################

import os, sys
import FreeCAD as App
import FreeCADGui as Gui
import pivy.coin as coin
from PySide import QtGui, QtCore  # https://www.freecadweb.org/wiki/PySide

def ConeRadiusExec():
    root = coin.SoSeparator()

    # Create myDragger with an initial translation of (1,0,0)
    myDragger = coin.SoTranslate1Dragger()
    root.addChild(myDragger)
    myDragger.translation = (1,0,0)

    # Place an coin.SoCone above myDragger
    myTransform = coin.SoTransform()
    myCone = coin.SoCone()
    root.addChild(myTransform)
    root.addChild(myCone)
    myTransform.translation = (0,3,0)

    # coin.SoDecomposeVec3f engine extracts myDragger's x-component
    # The result is connected to myCone's bottomRadius.
    myEngine = coin.SoDecomposeVec3f()
    myEngine.vector.connectFrom(myDragger.translation)
    myCone.bottomRadius.connectFrom(myEngine.x)
    
    view = Gui.ActiveDocument.ActiveView
    sg = view.getSceneGraph()
    sg.addChild(root)
