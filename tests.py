# -*- coding: utf-8 -*-
"""
tkColorPicker - Alternative to colorchooser for Tkinter.
Copyright 2017 Juliette Monsel <j_4321@protonmail.com>

tkColorPicker is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

tkColorPicker is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Tests
"""

import unittest
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk
import tkcolorpicker as tkc
import tempfile


class TestFunctions(unittest.TestCase):
    def test_round2(self):
        self.assertEqual(tkc.round2(1.1), 1)
        self.assertIsInstance(tkc.round2(1.1), int)

    def test_rgb_to_hsv(self):
        self.assertEqual(tkc.rgb_to_hsv(255, 0, 0), (0, 100, 100))

    def test_hsv_to_rgb(self):
        self.assertEqual(tkc.hsv_to_rgb(0, 100, 100), (255, 0, 0))

    def test_rgb_to_hexa(self):
        self.assertEqual(tkc.rgb_to_hexa(255, 255, 255), "#FFFFFF")
        self.assertEqual(tkc.rgb_to_hexa(255, 255, 255, 255), "#FFFFFFFF")

    def test_hexa_to_rgb(self):
        self.assertEqual(tkc.hexa_to_rgb("#FFFFFF"), (255, 255, 255))
        self.assertEqual(tkc.hexa_to_rgb("#FFFFFFFF"), (255, 255, 255, 255))

    def test_hue2col(self):
        self.assertEqual(tkc.hue2col(0), (255, 0, 0))

    def test_col2hue(self):
        self.assertEqual(tkc.col2hue(255, 0, 0), 0)

    def test_create_checkered_image(self):
        tkc.create_checkered_image(100, 100, (155, 120, 10, 255),
                                   (0, 0, 0, 255), s=8)

    def test_overlay(self):
        im = tkc.create_checkered_image(200, 200)
        tkc.overlay(im, (255, 0, 0, 100))


class BaseWidgetTest(unittest.TestCase):
    def setUp(self):
        self.window = tk.Tk()
        self.window.update()

    def tearDown(self):
        self.window.update()
        self.window.destroy()


class TestSpinbox(BaseWidgetTest):
    def test_spinbox_init(self):
        spinbox = tkc.Spinbox(self.window, from_=0, to=10)
        spinbox.pack()
        self.window.update()

    def test_spinbox_bindings(self):
        spinbox = tkc.Spinbox(self.window, from_=0, to=10)
        spinbox.pack()
        self.window.update()
        spinbox.event_generate('<FocusIn>')
        self.window.update()
        spinbox.event_generate('<FocusOut>')
        self.window.update()


class TestColorSquare(BaseWidgetTest):
    def test_colorsquare_init(self):
        cs = tkc.ColorSquare(self.window, hue=60, height=200, width=200)
        cs.pack()
        self.window.update()

    def test_colorsquare_bindings(self):
        cs = tkc.ColorSquare(self.window, hue=60, height=200, width=200)
        cs.pack()
        self.window.update()
        cs.event_generate('<1>', x=10, y=50)
        self.window.update()
        cs.event_generate('<B1-Motion>', x=20, y=50)
        self.window.update()
        cs.event_generate('<Configure>')
        self.window.update()

    def test_colorsquare_functions(self):
        cs = tkc.ColorSquare(self.window, hue=60, height=200, width=200)
        cs.pack()
        self.window.update()
        cs._fill()
        self.window.update()
        cs._draw((60, 100, 100))
        self.window.update()
        self.assertEqual(cs.get_hue(), 60)
        self.window.update()
        cs.set_hue(40)
        self.assertEqual(cs.get_hue(), 40)
        self.window.update()
        cs.set_rgb((255, 0, 0))
        self.assertEqual(cs.get_hue(), 0)
        self.window.update()
        cs.set_hsv((0, 100, 100))
        self.assertEqual(cs.get_hue(), 0)
        self.window.update()
        self.assertEqual(cs.get(), ((255, 0, 0), (0, 100, 100), '#FF0000'))
        self.window.update()


class TestAlphaBar(BaseWidgetTest):
    def test_alphabar_init(self):
        ab = tkc.AlphaBar(self.window, alpha=200, color=(255, 255, 2),
                          height=12, width=200)
        ab.pack()
        self.window.update()

    def test_alphabar_bindings(self):
        ab = tkc.AlphaBar(self.window, alpha=20, height=12, width=200)
        ab.pack()
        self.window.update()
        ab.event_generate('<1>', x=10, y=50)
        self.window.update()
        ab.event_generate('<B1-Motion>', x=20, y=50)
        self.window.update()
        ab.event_generate('<Configure>')
        self.window.update()

    def test_alphabar_functions(self):
        ab = tkc.AlphaBar(self.window, alpha=20, height=12, width=200)
        ab.pack()
        self.window.update()
        ab._draw_gradient(60, (255, 255, 0))
        self.window.update()
        self.assertEqual(ab.get(), 60)
        self.window.update()
        ab.set(40)
        self.window.update()
        self.assertEqual(ab.get(), 40)
        ab.set_color((0, 0, 0))
        self.window.update()
        ab.set_color((0, 0, 0, 100))
        self.window.update()
        ab._update_alpha()
        self.window.update()


class TestGradientBar(BaseWidgetTest):
    def test_gradientbar_init(self):
        gb = tkc.GradientBar(self.window, hue=20, height=12, width=200)
        gb.pack()
        self.window.update()

    def test_gradientbar_bindings(self):
        gb = tkc.GradientBar(self.window, hue=20, height=12, width=200)
        gb.pack()
        self.window.update()
        gb.event_generate('<1>', x=10, y=50)
        self.window.update()
        gb.event_generate('<B1-Motion>', x=20, y=50)
        self.window.update()
        gb.event_generate('<Configure>')
        self.window.update()

    def test_gradientbar_functions(self):
        gb = tkc.GradientBar(self.window, hue=20, height=12, width=200)
        gb.pack()
        self.window.update()
        gb._draw_gradient(60)
        self.window.update()
        self.assertEqual(gb.get(), 60)
        self.window.update()
        gb.set(40)
        self.window.update()
        self.assertEqual(gb.get(), 40)
        gb._update_hue()
        self.window.update()


class TestColorPicker(BaseWidgetTest):
    def test_colorpicker_init(self):
        c = tkc.ColorPicker(self.window, color="sky blue", title='Test')
        c.destroy()
        self.window.update()
        c = tkc.ColorPicker(self.window, color="pink", title='Test', alpha=True)
        c.destroy()
        self.window.update()
        c = tkc.ColorPicker(self.window, color="#ff0000", title='Test')
        c.destroy()
        self.window.update()
        c = tkc.ColorPicker(self.window, color="#00ff00", title='Test', alpha=True)
        c.destroy()
        self.window.update()
        c = tkc.ColorPicker(self.window, color="#00ff00cc", title='Test', alpha=True)
        c.destroy()
        self.window.update()
        c = tkc.ColorPicker(self.window, color="#00ff00cc", title='Test')
        c.destroy()
        self.window.update()
        c = tkc.ColorPicker(self.window, color=(255, 0, 0), title='Test')
        c.destroy()
        self.window.update()
        c = tkc.ColorPicker(self.window, color=(255, 0, 0), title='Test',
                            alpha=True)
        c.destroy()
        self.window.update()
        c = tkc.ColorPicker(self.window, color=(255, 0, 0, 100), title='Test',
                            alpha=True)
        c = tkc.ColorPicker(self.window, color=(255, 0, 0, 100), title='Test')
        c.destroy()
        self.window.update()

    def test_colorpicker_bindings(self):
        cp = tkc.ColorPicker(self.window, color="sky blue", title='Test',
                             alpha=True)
        self.window.update()
        cp.bar.event_generate("<ButtonRelease-1>", x=10, y=1)
        self.window.update()
        cp.bar.event_generate("<Button-1>", x=10, y=1)
        self.window.update()
        cp.alphabar.event_generate("<ButtonRelease-1>", x=10, y=1)
        self.window.update()
        cp.alphabar.event_generate("<Button-1>", x=10, y=1)
        self.window.update()
        cp.square.event_generate("<ButtonRelease-1>", x=10, y=1)
        self.window.update()
        cp.square.event_generate("<Button-1>", x=10, y=1)
        self.window.update()
        cp.hexa.event_generate("<FocusOut>")
        self.window.update()
        cp.hexa.event_generate("<Return>")
        self.window.update()

    def test_colorpicker_functions(self):
        cp = tkc.ColorPicker(self.window, color=(255, 0, 0, 255), title='Test',
                             alpha=True)
        self.window.update()
        cp._update_color_rgb()
        self.window.update()
        cp._update_color_hsv()
        self.window.update()
        cp._update_alpha()
        self.window.update()
        self.assertEqual(cp.get_color(), "")
        self.window.update()
        cp.ok()
        self.assertEqual(cp.get_color(),
                         ((255, 0, 0, 255), (0, 100, 100), "#FF0000FF"))
        self.window.update()
        cp.destroy()
        self.window.update()
        cp = tkc.ColorPicker(self.window, color=(255, 0, 0), title='Test')
        self.window.update()
        cp._update_color_rgb()
        self.window.update()
        cp._update_color_hsv()
        self.window.update()
        self.assertEqual(cp.get_color(), "")
        self.window.update()
        cp.ok()
        self.assertEqual(cp.get_color(),
                         ((255, 0, 0), (0, 100, 100), "#FF0000"))
        self.window.update()

    def test_colorpicker_staticmethods(self):
        cp = tkc.ColorPicker(self.window, color="sky blue", title='Test')
        strvar = tkc.tk.StringVar(cp, -2)
        self.window.update()
        self.assertEqual(cp.get_hue_value(strvar), 0)
        self.assertEqual(cp.get_sv_value(strvar), 0)
        self.assertEqual(cp.get_color_value(strvar), 0)
        self.window.update()
        strvar.set(50)
        self.assertEqual(cp.get_hue_value(strvar), 50)
        self.assertEqual(cp.get_sv_value(strvar), 50)
        self.assertEqual(cp.get_color_value(strvar), 50)
        self.window.update()
        strvar.set(390)
        self.assertEqual(cp.get_hue_value(strvar), 360)
        self.assertEqual(strvar.get(), '360')
        self.assertEqual(cp.get_color_value(strvar), 255)
        self.assertEqual(strvar.get(), '255')
        self.assertEqual(cp.get_sv_value(strvar), 100)
        self.assertEqual(strvar.get(), '100')
        self.window.update()
