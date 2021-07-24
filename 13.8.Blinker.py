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
# chapter 13, example 9.
#
# Blinker node.
# Use a blinker node to flash a neon ad sign on and off
#

from __future__ import print_function

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

def BlinkerExe():

    # Set up camera and light
    root = coin.SoSeparator()
    myCamera = coin.SoPerspectiveCamera()
    root.addChild(myCamera)
    root.addChild(coin.SoDirectionalLight())

    # Read in the parts of the sign from a file
    myInput = coin.SoInput()
    if not myInput.openFile("E:\\TEMP\\fix some drawing\\Mentor_Freecad\\eatAtJosies.iv"):   #TODO: FIXME : CHANGE PATH
        sys.exit(1)
    fileContents = coin.SoDB.readAll(myInput)
    if fileContents == None:
        sys.exit(1)

    eatAt = coin.SoNode.getByName("EatAt")
    josie = coin.SoNode.getByName("Josies")
    frame = coin.SoNode.getByName("Frame")

#############################################################
# CODE FOR The Inventor Mentor STARTS HERE

    # Add the non-blinking part of the sign to the root
    root.addChild(eatAt)
   
    # Add the fast-blinking part to a blinker node
    fastBlinker = coin.SoBlinker()
    root.addChild(fastBlinker)
    fastBlinker.speed = 2  # blinks 2 times a second
    fastBlinker.addChild(josie)

    # Add the slow-blinking part to another blinker node
    slowBlinker = coin.SoBlinker()
    root.addChild(slowBlinker)
    slowBlinker.speed = 0.5  # 2 secs per cycle 1 on, 1 off
    slowBlinker.addChild(frame)
    
    view = Gui.ActiveDocument.ActiveView
    sg = view.getSceneGraph()
    sg.addChild(root)
    