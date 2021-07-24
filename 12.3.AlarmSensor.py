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

def raiseFlagCallback(flagAngleXform, senSor):
    # We know that flagAngleXform is an autocasted coin.SoTransform node
    # Rotate flag by 90 degrees about the Z axis:
    flagAngleXform.rotation.setValue(coin.SbVec3f(0,0,1), 22/7/2)

# CODE FOR The Inventor Mentor ENDS HERE
###########################################################


def AlarmSensorEx():

###########################################################
# CODE FOR The Inventor Mentor STARTS HERE

    flagXform = coin.SoTransform()

    # Create an alarm that will call the flag-raising callback:
    myAlarm = coin.SoAlarmSensor(raiseFlagCallback, flagXform)
    myAlarm.setTimeFromNow(12.0)  # 12 seconds
    myAlarm.schedule()

# CODE FOR The Inventor Mentor ENDS HERE
###########################################################

    root = coin.SoSeparator()
    root.addChild(flagXform)
    myCone = coin.SoCone()
    myCone.bottomRadius = 0.1
    root.addChild(myCone)
    
    view = Gui.ActiveDocument.ActiveView
    sg = view.getSceneGraph()
    sg.addChild(root)
