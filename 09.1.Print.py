#!/usr/bin/env python

###
# Copyright (c) 2002-2007 Systems in Motion
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATcoin.SoEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS coin.SOFTWARE.
#coin.

###
# This is an example from the Inventor Mentor,
# chapter 9, example 1.
#
# Printing example.
# Read in an Inventor file and display it in ExaminerViewer.  Press
# the "p" key and the scene renders into a PostScript
# file for printing.
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

class callbackData:
    vwr = None
    filename = None
    scene = None

##############################################################
## CODE FOR The Inventor Mentor STARTS HERE

#Warning: This file might not works as it should. But I put the idea here. Mariwan


def printToPostScript(root, file, viewer, printerDPI):
    # Calculate size of the images in inches which is equal to
    # the size of the viewport in pixels divided by the number
    # of pixels per inch of the screen device.  This size in
    # inches will be the size of the Postscript image that will
    # be generated.
    vp  = viewer.getViewportRegion()
    imagePixSize = vp.getViewportSizePixels()
    imageInches = coin.SbVec2f()

    pixPerInch = coin.SoOffscreenRenderer.getScreenPixelsPerInch()
    imageInches.setValue(imagePixSize[0] / pixPerInch,
                         imagePixSize[1] / pixPerInch)

    # The resolution to render the scene for the printer
    # is equal to the size of the image in inches times
    # the printer DPI
    postScriptRes = coin.SbVec2s()
    postScriptRes.setValue(int(imageInches[0]*printerDPI),
                           int(imageInches[1]*printerDPI))

    # Create a viewport to render the scene into.
    myViewport = coin.SbViewportRegion()
    myViewport.setWindowSize(postScriptRes)
    myViewport.setPixelsPerInch(printerDPI)
    
    # Render the scene
    myRenderer = coin.SoOffscreenRenderer(myViewport)

    if not myRenderer.render(root):
        return False

    # Generate PostScript and write it to the given file
    myRenderer.writeToPostScript(file)

    return True

# CODE FOR The Inventor Mentor ENDS HERE
##############################################################

def processKeyEvents(data, cb):
    if coin.SoKeyboardEvent_isKeyPressEvent(cb.getEvent(), coin.SoKeyboardEvent.P):
        myFile = open(data.filename, "w")

        if myFile == None:
            sys.stderr.write("Cannot open output file\n")
            sys.exit(1)

        sys.stdout.write("Printing scene... ")
        sys.stdout.flush()
        if not printToPostScript(data.scene, myFile, data.vwr, 75):
            sys.stderr.write("Cannot print image\n")
            myFile.close()
            sys.exit(1)

        myFile.close()
        sys.stdout.write("  ...done printing.\n")
        sys.stdout.flush()
        cb.setHandled()

def ExecutePrint():
        
    filename="E:\\TEMP\\fix some drawing\\Mentor_Freecad\\changeme.ps"            #TODO::CHANGE THIS FILE NAME WITH THE PATH

    print("To print the scene: press the 'p' key while in picking mode")

    # Make a scene containing an event callback node
    root = coin.SoSeparator()
    eventCB = coin.SoEventCallback()
    root.addChild(eventCB)

    # Read the geometry from a file and add to the scene
    myInput = coin.SoInput()
    if not myInput.openFile("E:\\TEMP\\fix some drawing\\Mentor_Freecad\\duck.iv"):    #TODO::CHANGE THIS FILE NAME WITH THE PATH
        sys.exit(1)
    geomObject = coin.SoDB.readAll(myInput)
    if geomObject == None:
        sys.exit(1)
    root.addChild(geomObject)

    view = Gui.ActiveDocument.ActiveView    
    # Setup the event callback data and routine for performing the print
    data = callbackData()
    data.vwr = view
    data.filename = ("E:\\TEMP\\fix some drawing\\Mentor_Freecad\\DATA.cvs")          #TODO::CHANGE THIS FILE NAME WITH THE PATH
    data.scene = view.getSceneGraph()
    eventCB.addEventCallback(coin.SoKeyboardEvent.getClassTypeId(), processKeyEvents, data)

    sg = view.getSceneGraph()
    sg.addChild(root)
