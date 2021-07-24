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
# chapter 12, example 4.
#
# Timer sensors.  An object is rotated by a timer sensor.
# (called "rotatingSensor").  The interval between calls 
# controls how often it rotates.
# A second timer (called "schedulingSensor") goes off
# every 5 seconds and changes the interval of 
# "rotatingSensor".  The interval alternates between
# once per second and 10 times per second.
# This example could also be done using engines.
#

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


###########################################################
# CODE FOR The Inventor Mentor STARTS HERE

# This function is called either 10 times/second or once every
# second the scheduling changes every 5 seconds (see below):
def rotatingSensorCallback(myRotation, sensor):
    # Rotate an object...
    currentRotation = myRotation.rotation.getValue()
    currentRotation *= coin.SbRotation(coin.SbVec3f(0,0,1), 22/7/90.0)
    myRotation.rotation.setValue(currentRotation)

# This function is called once every 5 seconds, and
# reschedules the other sensor.
def schedulingSensorCallback(rotatingSensor, sensor):
    rotatingSensor.unschedule()
    if rotatingSensor.getInterval() == 1.0:
        rotatingSensor.setInterval(1.0/10.0)
    else: rotatingSensor.setInterval(1.0)
    rotatingSensor.schedule()

# CODE FOR The Inventor Mentor ENDS HERE
###########################################################

def TimerSensorExcu():
    root = coin.SoSeparator()

###########################################################   
# CODE FOR The Inventor Mentor STARTS HERE

    myRotation = coin.SoRotation()
    root.addChild(myRotation)

    rotatingSensor = coin.SoTimerSensor(rotatingSensorCallback, myRotation)
    rotatingSensor.setInterval(1.0) # scheduled once per second
    rotatingSensor.schedule()

    schedulingSensor = coin.SoTimerSensor(schedulingSensorCallback, rotatingSensor)
    schedulingSensor.setInterval(5.0) # once per 5 seconds
    schedulingSensor.schedule()

# CODE FOR The Inventor Mentor ENDS HERE
###########################################################

    inputFile = coin.SoInput()
    inputFile.openFile("E:\\TEMP\\fix some drawing\\Mentor_Freecad\\windmillTower.iv")
    root.addChild(coin.SoDB.readAll(inputFile))
    
    view = Gui.ActiveDocument.ActiveView
    sg = view.getSceneGraph()
    sg.addChild(root)