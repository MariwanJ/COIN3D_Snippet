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
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#

###
# This is an example from the Inventor Mentor,
# volume 1, chapter 15, example 3.
#
# Manipulator attachment example.
#
# The scene graph has an coin.SoWrapperKit, a cube and a sphere.
# A file containing a luxo lamp is read in as the 'contents'
# part of the coin.SoWrapperKit.
# When the user picks on the coin.SoWrapperKit (lamp), the kit's 
# "transform" part is replaced with an coin.SoTransformBoxManip.
# Alternatively, when the user picks the sphere, the
# sphere's associated transform is replaced by an
# SoHandleBoxManip.  Picking the cube causes an 
# SoTrackballManip to replace the cube's transform.
# 
# Manipulator callbacks are used to change
# the color of the object being manipulated.
# 
# Note that for illustration purposes, the
# cube and coin.SoWrapperKit already have transform nodes 
# associated with them; the sphere does not. In all cases, 
# the routine createTransformPath() is used to find the 
# transform node that affects the picked object.
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

# global data
myHandleBox      = None
myTrackball      = None
myTransformBox   = None
handleBoxPath    = None
trackballPath    = None
transformBoxPath = None

# Is this node of a type that is influenced by transforms?
def isTransformable(myNode):
    if (myNode.isOfType(coin.SoGroup.getClassTypeId()) or
        myNode.isOfType(coin.SoShape.getClassTypeId()) or
        myNode.isOfType(coin.SoCamera.getClassTypeId()) or
        myNode.isOfType(coin.SoLight.getClassTypeId())):
        return True
    else: 
        return False

#  Create a path to the transform node that affects the tail
#  of the input path.  Three possible cases:
#   [1] The path-tail is a node kit. Just ask the node kit for
#       a path to the part called "transform"
#   [2] The path-tail is NOT a group.  Search siblings of path
#       tail from right to left until you find a transform. If
#       none is found, or if another transformable object is 
#       found (shape,group,light,or camera), then insert a 
#       transform just to the left of the tail. This way, the 
#       manipulator only effects the selected object.
#   [3] The path-tail IS a group.  Search its children left to
#       right until a transform is found. If a transformable
#       node is found first, insert a transform just left of 
#       that node.  This way the manip will affect all nodes
#       in the group.
def createTransformPath(inputPath):
    pathLength = inputPath.getLength()
    if pathLength < 2: # Won't be able to get parent of tail
        return None

    tail = inputPath.getTail()

    # CASE 1: The tail is a node kit.
    # Nodekits have built in policy for creating parts.
    # The kit copies inputPath, then extends it past the 
    # kit all the way down to the transform. It creates the
    # transform if necessary.
    if tail.isOfType(coin.SoBaseKit.getClassTypeId()):
        kit = tail
        return kit.createPathToPart("transform", True, inputPath)

    editXf = None
    parent = None
    existedBefore = False

    # CASE 2: The tail is not a group.
    isTailGroup = tail.isOfType(coin.SoGroup.getClassTypeId())
    if not coin.isTailGroup:
        # 'coin.parent' is node above tail. Search under parent right
        # to coin.left for a transform. If we find a 'movable' node
        # insert a transform just left of tail.  
        parent = inputPath.getNode(pathLength - 2)
        tailIndx = parent.findChild(tail)

        for i in range(tailIndx, -1, -1):
            if editXf != None:
                break
            myNode = parent.getChild(i)
            if myNode.isOfType(coin.SoTransform.getClassTypeId()):
                editXf = myNode
            elif i != tailIndx and isTransformable(myNode):
                break

        if editXf == None:
            existedBefore = False
            editXf = coin.SoTransform()
            parent.insertChild(editXf, tailIndx)
        else:
            existedBefore = True

    # CASE 3: The tail is a group.
    else:
        # Search the children from left to right for transform 
        # nodes. Stop the search if we come to a movable node.
        # and insert a transform before it.
        parent = tail
        for i in range(parent.getNumChildren()):
            if editXf != None:
                break
            myNode = parent.getChild(i)
            if myNode.isOfType(coin.SoTransform.getClassTypeId()):
                editXf = myNode
            elif isTransformable(myNode):
                break

        if editXf == None:
            existedBefore = False
            editXf = coin.SoTransform()
            parent.insertChild(editXf, i)
        else:
            existedBefore = True

    # Create 'pathToXform.' Copy inputPath, then make last
    # node be editXf.
    pathToXform = None
    pathToXform = inputPath.copy()
    if not isTailGroup: # pop off the last entry.
        pathToXform.pop()
    # add editXf to the end
    xfIndex = parent.findChild(editXf)
    pathToXform.append(xfIndex)
    
    return pathToXform

# This routine is called when an object
# gets selected. We determine which object
# was selected, then call replaceNode()
# to replace the object's transform with
# a manipulator.
def selectionCallback(void, # user data is not used
                      selectionPath):
    global myHandleBox, myTrackball, myTransformBox, handleBoxPath
    global trackballPath, transformBoxPath

    # Attach the manipulator.
    # Use the convenience routine to get a path to
    # the transform that effects the selected object.
    xformPath = createTransformPath(selectionPath)
    if not xformPath: return

    # Attach the handle box to the sphere,
    # the trackball to the cube
    # or the transformBox to the wrapperKit
    if selectionPath.getTail().isOfType(coin.SoSphere.getClassTypeId()):
        handleBoxPath = xformPath
        myHandleBox.replaceNode(xformPath)
    elif selectionPath.getTail().isOfType(coin.SoCube.getClassTypeId()):
        trackballPath = xformPath
        myTrackball.replaceNode(xformPath)
    elif selectionPath.getTail().isOfType(coin.SoWrapperKit.getClassTypeId()):
        transformBoxPath = xformPath
        myTransformBox.replaceNode(xformPath)

# This routine is called whenever an object gets
# deselected. It detaches the manipulator from
# the transform node, and removes it from the 
# scene graph that will not be visible.
def deselectionCallback(void, # user data is not used
                        deselectionPath):
    global myHandleBox, myTrackball, myTransformBox, handleBoxPath
    global trackballPath, transformBoxPath
    
    if deselectionPath.getTail().isOfType(coin.SoSphere.getClassTypeId()):
        myHandleBox.replaceManip(handleBoxPath,None)
    elif deselectionPath.getTail().isOfType(coin.SoCube.getClassTypeId()):
        myTrackball.replaceManip(trackballPath,None)
    elif deselectionPath.getTail().isOfType(coin.SoWrapperKit.getClassTypeId()):
        myTransformBox.replaceManip(transformBoxPath,None)

# This is called when a manipulator is
# about to begin manipulation.
def dragStartCallback(myMaterial, # user data
                      dragger):   # callback data not used
    myMaterial.diffuseColor = (1,.2,.2)

# This is called when a manipulator is
# done manipulating.
def dragFinishCallback(myMaterial, # user data
                       dragger):   # callback data not used
    myMaterial.diffuseColor = (.8,.8,.8)

def AttachManipExe():
    global myHandleBox, myTrackball, myTransformBox
    

    # create and set up the selection node
    selectionRoot = coin.SoSelection()
    selectionRoot.addSelectionCallback(selectionCallback, None)
    selectionRoot.addDeselectionCallback(deselectionCallback, None)

    # create the scene graph
    root = coin.SoSeparator()
    selectionRoot.addChild(root)

    # Read a file into contents of coin.SoWrapperKit 
    # Translate it to the right.
    myWrapperKit = coin.SoWrapperKit()
    root.addChild(myWrapperKit)
    myInput = coin.SoInput()
    if not myInput.openFile("E:\\TEMP\\fix some drawing\\Mentor_Freecad\\luxo.iv"):   #TODO: FIXME: Change the path
        sys.exit(1)
    objectFromFile = coin.SoDB.readAll(myInput)
    if objectFromFile == None:
        sys.exit(1)
    myWrapperKit.setPart("contents",objectFromFile)
    myWrapperKit.set("transform { translation 3 -1 0 }")
    wrapperMat = myWrapperKit.getPart("material",True)
    wrapperMat.diffuseColor = (.8, .8, .8)

    # Create a cube with its own transform.
    cubeRoot  = coin.SoSeparator()
    cubeXform = coin.SoTransform()
    cubeXform.translation = (-4, 0, 0)
    root.addChild(cubeRoot)
    cubeRoot.addChild(cubeXform)

    cubeMat = coin.SoMaterial()
    cubeMat.diffuseColor = (.8, .8, .8)
    cubeRoot.addChild(cubeMat)
    cubeRoot.addChild(coin.SoCube())

    # add a sphere node without a transform
    # (one will be added when we attach the manipulator)
    sphereRoot = coin.SoSeparator()
    sphereMat = coin.SoMaterial()
    root.addChild(sphereRoot)
    sphereRoot.addChild(sphereMat)
    sphereRoot.addChild(coin.SoSphere())
    sphereMat.diffuseColor = (.8, .8, .8)

    # create the manipulators
    myHandleBox = coin.SoHandleBoxManip()
    myTrackball = coin.SoTrackballManip()
    myTransformBox = coin.SoTransformBoxManip()

    # Get the draggers and add callbacks to them. Note
    # that you don't put callbacks on manipulators. You put
    # them on the draggers which handle events for them. 
    myDragger = myTrackball.getDragger()
    myDragger.addStartCallback(dragStartCallback,cubeMat)
    myDragger.addFinishCallback(dragFinishCallback,cubeMat)

    myDragger = myHandleBox.getDragger()
    myDragger.addStartCallback(dragStartCallback,sphereMat)
    myDragger.addFinishCallback(dragFinishCallback,sphereMat)

    myDragger = myTransformBox.getDragger()
    myDragger.addStartCallback(dragStartCallback,wrapperMat)
    myDragger.addFinishCallback(dragFinishCallback,wrapperMat)
    
    view = Gui.ActiveDocument.ActiveView
    sg = view.getSceneGraph()
    sg.addChild(root)
