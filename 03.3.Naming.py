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
# chapter 3.
#
# Create a little scene graph and then name coin.Some nodes and
# get back nodes by name.
#
####################################################################
#         Modified to be compatible with  FreeCAD                  #
#                                                                  #
# Author : Mariwan Jalal  mariwan.jalal@gmail.com                  #
####################################################################

import os,sys
import FreeCAD as App
import FreeCADGui as Gui
import pivy.coin as coin


def RemoveCube():
   # Remove the cube named 'MyCube' from the separator named
   # 'Root'.  In a real application, icoin.SofType() would probably
   # be used to make sure the nodes are of the correct type
   # before doing the cast.
   # In Pivy no cast is necessary as it gets autocasted for you.

   myRoot = coin.SoNode.getByName("Root")

   myCube = coin.SoNode.getByName("MyCube")
   
   myRoot.removeChild(myCube)

def ExecuteRemoveCube():
   # coin.SoDB.init() invoked automatically upon coin module import
    
   # Create coin.Some objects and give them names:
   root = coin.SoSeparator()
   root.setName("Root")
    
   myCube = coin.SoCube()
   root.addChild(myCube)
   myCube.setName("MyCube")
    
   mySphere = coin.SoSphere()
   root.addChild(mySphere)
   mySphere.setName("MySphere")

