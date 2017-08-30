tkcolorpicker
=============

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

With pip:

::

    $ pip install tkcolorpicker


Documentation
-------------

Syntax:

::

    askcolor(color="red", parent=None, title=_("Color Chooser"), alpha=False):

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
