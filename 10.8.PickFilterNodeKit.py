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
# This is an example from The Inventor Mentor,
# chapter 10, example 8.
#
# This example demonstrates the use of the pick filter
# callback to always select nodekits. This makes it especially
# easy to edit attributes of objects because the nodekit takes
# care of the part creation details.
#

from __future__ import print_function

####################################################################
#        Modified to be compatible with  FreeCAD                   #
#                                                                  #
# Author : Mariwan Jalal  mariwan.jalal@gmail.com                  #
####################################################################

import os
import sys,math
import FreeCAD as App
import FreeCADGui as Gui
import pivy.coin as coin


#WARNING: THIS WILL NOT WORKS!!! : TODO: FIXME:


class UserData:
    sel = None
    editor = None
    ignore = None

##############################################################
## CODE FOR The Inventor Mentor STARTS HERE  (part 1)

# Truncate the pick path coin.So a nodekit is selected
def pickFilterCB(void, pick):
    # See which child of selection got picked
    p = pick.getPath()

    for i in range(p.getLength() - 1, -1, -1):
        n = p.getNode(i)
        if n.icoin.SofType(coin.SoShapeKit.getClassTypeId()):
            break

    # Copy the path down to the nodekit
    return p.copy(0, i+1)

# CODE FOR The Inventor Mentor ENDS HERE
##############################################################


# Create a sample scene graph
def buildScene():
    g = coin.SoGroup()
    
    # Place a dozen shapes in circular formation
    for i in range(12):
        k = coin.SoShapeKit()
        k.setPart("shape", coin.SoCube())
        xf = k.getPart("transform", True)
        xf.translation = (8*math.sin(i*22/7/6), 8*math.cos(i*22/7/6), 0.0)
        g.addChild(k)

    return g

# Update the material editor to reflect the selected object
def selectCB(userData, path):
    kit = path.getTail()
    kitMtl = kit.getPart("material", True)

    # ud = userData
    userData.ignore = True
    userData.editor.setMaterial(kitMtl)
    userData.ignore = False

# This is called when the user chooses a new material
# in the material editor. This updates the material
# part of each selected node kit.
def mtlChangeCB(userData, mtl):
    # Our material change callback is invoked when the
    # user changes the material, and when we change it
    # through a call to coin.SoGuiMaterialEditor.setMaterial.
    # In this latter case, we ignore the callback invocation
    # ud = userData

    if userData.ignore:
        return

    sel = userData.sel
    
    # Our pick filter guarantees the path tail will
    # be a shape kit.
    for i in range(sel.getNumSelected()):
        p = sel.getPath(i)
        kit = p.getTail()
        kitMtl = kit.getPart("material", True)
        kitMtl.copyFieldValues(mtl)

def PickFilterNodeKitExec():
    
    # Create our scene graph.
    sel = coin.SoSelection()
    sel.addChild(buildScene())

    # Create a material editor
    try:
        ed = coin.SoGuiMaterialEditor()
    except:
        print("The coin.SoGuiMaterialEditor node has not been implemented in the " + \
              "coin.SoGui bindings of Coin!")
        sys.exit(1)
    ed.show()

    # User data for our callbacks
    userData = UserData()
    userData.sel = sel
    userData.editor = ed
    userData.ignore = False
   
    # Selection and material change callbacks
    ed.addMaterialChangedCallback(mtlChangeCB, userData)
    sel.setPickFilterCallback(pickFilterCB)
    sel.addSelectionCallback(selectCB, userData)
    
    view = Gui.ActiveDocument.ActiveView
    sg = view.getSceneGraph()
    sg.addChild(sel)
    