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
# chapter 12, example 2.
#
# Using getTriggerNode/getTriggerField methods of the data
# sencoin.Sor.
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


# Sencoin.Sor callback function:
def rootChangedCB(void, mySenSor):
    # SenSors get autocasted; there is no need to cast them manually
    # through the cast() function, such as:
    #   mySencoin.Sor = cast(s, "coin.SoDataSencoin.Sor")
    # mySencoin.Sor is therefore a coin.SoNodeSencoin.Sor.

    changedNode = mySenSor.getTriggerNode()
    changedField = mySenSor.getTriggerField()
    
    print("The node named '%s' changed" % (changedNode.getName().getString()))

    if changedField:
        # the pythonic getFieldName() method returns a string or None in Pivy.
        fieldName = changedNode.getFieldName(changedField)
        print(" (field %s)" % (fieldName))
    else:
        print(" (no fields changed)")

def NodeSensorEx():
    # coin.SoDB.init() invoked automatically upon coin module import

    root = coin.SoSeparator()
    root.setName("Root")

    myCube = coin.SoCube()
    root.addChild(myCube)
    myCube.setName("MyCube")

    mySphere = coin.SoSphere()
    root.addChild(mySphere)
    mySphere.setName("MySphere")

    mySenSor = coin.SoNodeSensor(rootChangedCB, None)
    mySenSor.setPriority(0)
    # mySencoin.Sor.setFunction(rootChangedCB)
    mySenSor.attach(root)

    # Now, make a few changes to the scene graph the senSor's
    # callback function will be called immediately after each
    # change.
    myCube.width = 1.0
    myCube.height = 2.0
    mySphere.radius = 3.0
    root.removeChild(mySphere)
    
    view = Gui.ActiveDocument.ActiveView
    sg = view.getSceneGraph()
    sg.addChild(root)