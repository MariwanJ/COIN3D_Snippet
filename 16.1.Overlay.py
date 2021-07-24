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
# This is an example from the Inventor Mentor,
# chapter 16, example 1.
#
# This example shows how to use the overlay planes with the
# viewer components. By default color 0 is used for the
# overlay planes background color (clear color), coin.so we use
# color 1 for the object. This example alcoin.so shows how to
# load the overlay color map with the wanted color.
#

from __future__ import print_function
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

overlayScene = """
#Inventor V2.0 ascii

Separator {
   OrthographicCamera {
      position 0 0 5
      nearDistance 1.0
      farDistance 10.0
      height 1
   }
   LightModel { model BASE_COLOR }
   ColorIndex { index 1 }
   Coordinate3 { point [ -1 -1 0, -1 1 0, 1 1 0, 1 -1 0] }
   FaceSet {}
}"""

def OverlayExe():

    # read the scene graph in
    input = coin.SoInput()
    input.setBuffer(overlayScene)
    scene = coin.SoDB.readAll(input)
    if scene == None:
        print("Couldn't read scene")
        sys.exit(1)

    # Allocate the viewer, set the overlay scene and
    # load the overlay color map with the wanted color.
    color = coin.SbColor(.5, 1, .5)
    myViewer = Gui.createViewer(2)
    for i,v in enumerate(myViewer):
        v.setSceneGraph(coin.SoCone())
   # myViewer.setOverlaySceneGraph(scene)     #TODO FIXME : DOESN'T WORK !! 
   # myViewer.setOverlayColorMap(1, 1, color)
   # myViewer.setTitle("Overlay Plane")
