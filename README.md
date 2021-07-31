## Coin3D/Pivy Examples/Macros for FreeCAD

A Collection of 3D drawing examples using Pivy/Coin3D within FreeCAD.

### Description

**[FreeCAD](https://freecadweb.org)** is a free libre open source Parametric CAD/CAM<br>
**[Coin3D](https://github.com/coin3d/coin/)** (AKA 'Coin') is an OpenGL-based, 3D graphics library that has its roots in the Open Inventor 2.1 API, which Coin still is compatible with.<br>
**[Pivy](https://github.com/coin3d/pivy)** is a Python library for python bindings of Coin3D.<br>
**[Wiki](https://wiki.freecadweb.org/Coin3d_snippets)** List of the examples with some descriptions<br>
### Purpose

This repository's purpose is to show practical examples of how to use the Coin3D API in macros or within the FreeCAD console. The code has been modified to be suitable to run within FreeCAD (see [Limitations](#Limitations)).

### Background

I've always wanted to see some examples of the Coin3d API. But documentation is so sparse until now... a repository of practical examples that will help decrease a dev's learning curve regarding this library. I searched a lot to find these kind of examples.. without much assistance.. Google in the end came through!! But not initially (only after many months of searching). The original examples can be found at:

https://github.com/coin3d/pivy/tree/master/examples/Mentor


### Limitations

- There are files that **cannot** be modified to a suitable python file for FreeCAD due to having 3rd party dependencies or incorrect context. For example, you may see references to specific Linux commands or a dependency on an OpenGL library that doesn't exist in FreeCAD.
- Be aware that there are some files loaded from your hard disk (`*.iv`) extensions because their paths are hardcoded. You'll need to modify them. There is always a TODO: FIXME: text near to that line

### Examples

This section will contain screenshots of different Coin3d snippets. TBD

### License

**Note:** There is no LICENSE file or license mentioned, I'm assuming the original license applies.

I hope you enjoy learning Coin3D in FreeCAD.

-*Mariwan Jalal*

