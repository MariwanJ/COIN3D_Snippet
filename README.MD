## Coin3D/Pivy Examples/Macros for FreeCAD

A Collection of 3D drawing examples using Pivy/Coin3D within [FreeCAD](https://www.freecadweb.org).

### Description

**[FreeCAD](https://freecadweb.org)** is a free libre open source Parametric CAD/CAM   
**[Coin3D](https://github.com/coin3d/coin/)** (AKA 'Coin') is an OpenGL-based, 3D graphics library that has its roots in the Open Inventor 2.1 API, which Coin still is compatible with.  
**[Pivy](https://github.com/coin3d/pivy)** is a Python library for python bindings of Coin3D. 

### AIM

I've always wanted to see some examples for of the Coin3d API. But documentation on this is so sparse until now... a repository of practical examples that will help decrease a dev's learning curve regarding this library. I search a lot to find these kind of examples.. without much assistance.. Google in the end came through!! but not initially (only after many monthes of searching). The original examples can be found at:

https://github.com/coin3d/pivy/tree/master/examples/Mentor

But this repository's aim is to modify them so one can run them as a macro or within the FreeCAD console.

**Note:** There is no LICENSE file or license mentioned, I'm assuming the original license applies.

I hope you enjoy learning Coin3D in FreeCAD.

-*Mariwan Jalal*

### Limitations

- There are files that **cannot** be modified to a suitable python file for FreeCAD due to the nature of the commands inside said files. For example, it may reference a specific Linux command or it uses an OpenGL library that does note exist in FreeCAD.
- Be aware that there are some files loaded from your hard disk (`*.iv`) extensions because their paths are hardcoded. You'll need to modify them. 
- There is always a TODO: FIXME: text near to that line

### Examples

This section will contain screenshots of different Coin3d snippets. TBD

