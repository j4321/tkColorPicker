tkcolorpicker
=============

|Release| |Travis| |Appveyor| |Codecov| |Windows| |Linux| |Mac| |License|

Color picker dialog for Tkinter.

This module contains a `ColorPicker` class which implements the color picker
and an `askcolor` function that displays the color picker and
returns the chosen color in RGB and HTML formats.


Requirements
------------

- Linux, Windows, Mac
- Python 2.7 or 3.x with tkinter + ttk (default for Windows but not for Linux)


Installation
------------

- Ubuntu: use the PPA `ppa:j-4321-i/ppa`

    ::

        $ sudo add-apt-repository ppa:j-4321-i/ppa
        $ sudo apt-get update
        $ sudo apt-get install python(3)-tkcolorpicker


- Archlinux: 
    
    the package is available on `AUR <https://aur.archlinux.org/packages/python-tkcolorpicker>`__


- With pip:

    ::

        $ pip install tkcolorpicker


Documentation
-------------

Syntax:

::

    askcolor(color="red", parent=None, title=_("Color Chooser"), alpha=False)

Open a ColorPicker dialog and return the chosen color.

The selected color is returned as a tuple (RGB(A), #RRGGBB(AA))
(None, None) is returned if the color selection is cancelled.

Arguments:

    + color: initially selected color, supported formats:
    
        - RGB(A)
        - #RRGGBB(AA) 
        - tkinter color name (see http://wiki.tcl.tk/37701 for a list)
        
    + parent: parent window
    + title: dialog title
    + alpha: alpha channel suppport


Example
-------

.. code:: python

    import tkinter as tk
    import tkinter.ttk as ttk
    from tkcolorpicker import askcolor

    root = tk.Tk()
    style = ttk.Style(root)
    style.theme_use('clam')

    print(askcolor((255, 255, 0), root))
    root.mainloop()


.. |Release| image:: https://badge.fury.io/py/tkcolorpicker.svg
    :alt: Latest Release
.. _Release:  https://pypi.org/project/tkcolorpicker/
.. |Linux| image:: https://img.shields.io/badge/platform-Linux-blue.svg
    :alt: Platform
.. |Windows| image:: https://img.shields.io/badge/platform-Windows-blue.svg
    :alt: Platform
.. |Mac| image:: https://img.shields.io/badge/platform-Mac-blue.svg
    :alt: Platform
.. |Travis| image:: https://travis-ci.org/j4321/tkColorPicker.svg?branch=master
    :target: https://travis-ci.org/j4321/tkColorPicker
    :alt: Travis CI Build Status
.. |Appveyor| image:: https://ci.appveyor.com/api/projects/status/7ow8wfw5by7uiise/branch/master?svg=true
    :target: https://ci.appveyor.com/project/j4321/tkcolorpicker/branch/master
    :alt: Appveyor Build Status
.. |Codecov| image:: https://codecov.io/gh/j4321/tkColorPicker/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/j4321/tkColorPicker
    :alt: Code coverage
.. |License| image:: https://img.shields.io/github/license/j4321/tkColorPicker.svg
    :target: https://www.gnu.org/licenses/gpl-3.0.en.html
    :alt: License
