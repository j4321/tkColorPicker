tkColorPicker
=============

Color picker dialog for Tkinter.

This module contains a `ColorPicker` class which implements the color picker
and an `askcolor` function that displays the color picker and
returns the chosen color in rgb and html formats.

Requirements
------------

- Linux, Windows, Mac
- Python 3 with tkinter + ttk (default for Windows but not for Linux)


Installation
------------

With pip:

::

    $ pip install tkColorPicker



Example
=======

.. code:: python

    import tkinter as tk
    import tkinter.ttk as ttk
    from tkColorPicker import askcolor

    root = tk.Tk()
    style = ttk.Style(root)
    style.theme_use('clam')

    print(askcolor(root, (255, 255, 0)))
    root.mainloop()




