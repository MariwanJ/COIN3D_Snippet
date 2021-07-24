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
# This is an example from the Inventor Mentor.
# chapter 14, example 1.
#
# Use coin.SoShapeKits to create two 3-D words, "NICE" and "HAPPY"
# Use nodekit methods to access the fields of the "material"
# and "transform" parts.
# Use a calculator engine and an elapsed time engine to make
# the words change color and fly about the screen.
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

def FrolickingWordsExe():
    # Initialize Inventor and Qt

    root = coin.SoSeparator()

    # Create shape kits with the words "HAPPY" and "NICE"
    happyKit = coin.SoShapeKit()
    root.addChild(happyKit)
    happyKit.setPart("shape", coin.SoText3())
    happyKit.set("shape { parts ALL string \"HAPPY\"}")
    happyKit.set("font { size 2}")

    niceKit = coin.SoShapeKit()
    root.addChild(niceKit)
    niceKit.setPart("shape", coin.SoText3())
    niceKit.set("shape { parts ALL string \"NICE\"}")
    niceKit.set("font { size 2}")

    # Create the Elapsed Time engine
    myTimer = coin.SoElapsedTime()

    # Create two calculator - one for HAPPY, one for NICE.
    happyCalc = coin.SoCalculator()
    happyCalc.a.connectFrom(myTimer.timeOut)
    happyCalc.expression = """ta=cos(2*a); tb=sin(2*a);
                              oA = vec3f(3*pow(ta,3),3*pow(tb,3),1);
                              oB = vec3f(fabs(ta)+.1,fabs(.5*fabs(tb))+.1,1);
                              oC = vec3f(fabs(ta),fabs(tb),.5)"""

    # The second calculator uses different arguments to
    # sin() and cos(), coin.So it moves out of phase.
    niceCalc = coin.SoCalculator()
    niceCalc.a.connectFrom(myTimer.timeOut)
    niceCalc.expression = """ta=cos(2*a+2); tb=sin(2*a+2);
                             oA = vec3f(3*pow(ta,3),3*pow(tb,3),1);
                             oB = vec3f(fabs(ta)+.1,fabs(.5*fabs(tb))+.1,1);
                             oC = vec3f(fabs(ta),fabs(tb),.5)"""

    # Connect the transforms from the calculators...
    happyXf = happyKit.getPart("transform",True)
    happyXf.translation.connectFrom(happyCalc.oA)
    happyXf.scaleFactor.connectFrom(happyCalc.oB)
    niceXf = niceKit.getPart("transform",True)
    niceXf.translation.connectFrom(niceCalc.oA)
    niceXf.scaleFactor.connectFrom(niceCalc.oB)

    # Connect the materials from the calculators...
    happyMtl = happyKit.getPart("material",True)
    happyMtl.diffuseColor.connectFrom(happyCalc.oC)
    niceMtl = niceKit.getPart("material",True)
    niceMtl.diffuseColor.connectFrom(niceCalc.oC)

    view = Gui.ActiveDocument.ActiveView
    sg = view.getSceneGraph()
    sg.addChild(root)
