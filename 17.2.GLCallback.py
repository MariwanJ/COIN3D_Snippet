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
# This is an example from The Inventor Mentor,
# chapter 17, example 2.
#
# Example of combining Inventor and OpenGL rendering.
# Create an Inventor render area and draw a red cube
# and a blue sphere.  Render the floor with OpenGL
# through a Callback node.
#

####################################################################
#        Modified to be compatible with  FreeCAD                   #
#                                                                  #
# Author : Mariwan Jalal  mariwan.jalal@gmail.com                  #
####################################################################
#Warning: This doesn't work on freecad .. no OpenGl support
# import os
# import sys
# import FreeCAD as App
# import FreeCADGui as Gui
# import pivy.coin as coin
# from PySide import QtGui, QtCore  # https://www.freecadweb.org/wiki/PySide


# from OpenGL.GL import *

# floorObj = []

# # Build a scene with two objects and some light


# def buildScene(root):
#     # coin.Some light
#     root.addChild(coin.SoLightModel())
#     root.addChild(coin.SoDirectionalLight())

#     # A red cube translated to the left and down
#     myTrans = coin.SoTransform()
#     myTrans.translation = (-2.0, -2.0, 0.0)
#     root.addChild(myTrans)

#     myMtl = coin.SoMaterial()
#     myMtl.diffuseColor = (1.0, 0.0, 0.0)
#     root.addChild(myMtl)

#     root.addChild(coin.SoCube())

#     # A blue sphere translated right
#     myTrans = coin.SoTransform()
#     myTrans.translation = (4.0, 0.0, 0.0)
#     root.addChild(myTrans)

#     myMtl = coin.SoMaterial()
#     myMtl.diffuseColor = (0.0, 0.0, 1.0)
#     root.addChild(myMtl)

#     root.addChild(coin.SoSphere())

# # Build the floor that will be rendered using OpenGL.


# def buildFloor():
#     global floorObj
#     a = 0

#     for i in range(9):
#         for j in range(9):
#             floorObj.append([-5.0 + j*1.25, 0.0, -5.0 + i*1.25])
#             a += 1

# # Draw the lines that make up the floor, using OpenGL


# def drawFloor():
#     global floorObj
#     glBegin(GL_LINES)
#     for i in range(4):
#         glVertex3fv(floorObj[i*18])
#         glVertex3fv(floorObj[(i*18)+8])
#         glVertex3fv(floorObj[(i*18)+17])
#         glVertex3fv(floorObj[(i*18)+9])
#     i += 1
#     glVertex3fv(floorObj[i*18])
#     glVertex3fv(floorObj[(i*18)+8])
#     glEnd()

#     glBegin(GL_LINES)
#     for i in range(4):
#         glVertex3fv(floorObj[i*2])
#         glVertex3fv(floorObj[(i*2)+72])
#         glVertex3fv(floorObj[(i*2)+73])
#         glVertex3fv(floorObj[(i*2)+1])

#     i += 1
#     glVertex3fv(floorObj[i*2])
#     glVertex3fv(floorObj[(i*2)+72])
#     glEnd()

# # Callback routine to render the floor using OpenGL


# def myCallbackRoutine(void, action):
#     # only render the floor during GLRender actions:
#     if not action.icoin.sOfType(coin.SoGLRenderAction.getClassTypeId()):
#         return

#     glPushMatrix()
#     glTranslatef(0.0, -3.0, 0.0)
#     glColor3f(0.0, 0.7, 0.0)
#     glLineWidth(2)
#     glDisable(GL_LIGHTING)  # coin.so we don't have to set normals
#     drawFloor()
#     glEnable(GL_LIGHTING)
#     glLineWidth(1)
#     glPopMatrix()

#     # With Inventor 2.1, it's necessary to reset coin.SoGLLazyElement after
#     # making calls (such as glColor3f()) that affect material state.
#     # In this case, the diffuse color and light model are being modified,
#     # coin.so the logical-or of DIFFUSE_MASK and LIGHT_MODEL_MASK is passed
#     # to coin.SoGLLazyElement::reset().
#     # Additional information can be found in the publication
#     # "Open Inventor 2.1 Porting and Performance Tips"

#     # state = action.getState()
#     # lazyElt = coin.SoLazyElement.getInstance(state)
#     # lazyElt.reset(state, (coin.SoLazyElement.DIFFUSE_MASK)|(coin.SoLazyElement.LIGHT_MODEL_MASK))


# def main():
#     buildFloor()
#     # Build a simple scene graph, including a camera and
#     # a coin.SoCallback node for performing coin.some GL rendering.
#     root = coin.SoSeparator()

#     myCamera = coin.SoPerspectiveCamera()
#     myCamera.position = (0.0, 0.0, 5.0)
#     myCamera.heightAngle = 22/7/2.0  # 90 degrees
#     myCamera.nearDistance = 2.0
#     myCamera.farDistance = 12.0
#     root.addChild(myCamera)

#     myCallback = coin.SoCallback()
#     myCallback.setCallback(myCallbackRoutine)
#     root.addChild(myCallback)
#     buildScene(root)
#     drawFloor()

#     view = Gui.ActiveDocument.ActiveView
#     sg = view.getSceneGraph()
#     sg.addChild(root)
