# -*- coding: utf-8 -*-
"""
tkcolorpicker - Alternative to colorchooser for Tkinter.
Copyright 2017 Juliette Monsel <j_4321@protonmail.com>

tkcolorpicker is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

tkcolorpicker is distributed in the hope that it will be useful,
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
import tkcolorpicker.functions as tkf
from tkcolorpicker.spinbox import Spinbox
from tkcolorpicker.limitvar import LimitVar


class TestFunctions(unittest.TestCase):
    def test_round2(self):
        self.assertEqual(tkf.round2(1.1), 1)
        self.assertIsInstance(tkf.round2(1.1), int)

    def test_rgb_to_hsv(self):
        self.assertEqual(tkf.rgb_to_hsv(255, 0, 0), (0, 100, 100))

    def test_hsv_to_rgb(self):
        self.assertEqual(tkf.hsv_to_rgb(0, 100, 100), (255, 0, 0))

    def test_rgb_to_hexa(self):
        self.assertEqual(tkf.rgb_to_hexa(255, 255, 255), "#FFFFFF")
        self.assertEqual(tkf.rgb_to_hexa(255, 255, 255, 255), "#FFFFFFFF")
        self.assertRaises(ValueError, tkf.rgb_to_hexa, 255, 255)

    def test_hexa_to_rgb(self):
        self.assertEqual(tkf.hexa_to_rgb("#FFFFFF"), (255, 255, 255))
        self.assertEqual(tkf.hexa_to_rgb("#FFFFFFFF"), (255, 255, 255, 255))
        self.assertRaises(ValueError, tkf.hexa_to_rgb, "#FFFFF")

    def test_hue2col(self):
        self.assertEqual(tkf.hue2col(0), (255, 0, 0))
        self.assertRaises(ValueError, tkf.hue2col, 365)
        self.assertRaises(ValueError, tkf.hue2col, -20)

    def test_col2hue(self):
        self.assertEqual(tkf.col2hue(255, 0, 0), 0)

    def test_create_checkered_image(self):
        tkf.create_checkered_image(100, 100, (155, 120, 10, 255),
                                   (0, 0, 0, 255), s=8)

    def test_overlay(self):
        im = tkf.create_checkered_image(200, 200)
        tkf.overlay(im, (255, 0, 0, 100))


class BaseWidgetTest(unittest.TestCase):
    def setUp(self):
        self.window = tk.Tk()
        self.window.update()

    def tearDown(self):
        self.window.update()
        self.window.destroy()


class TestEvent:
    """Fake event for testing."""
    def __init__(self, **kwargs):
        self._prop = kwargs

    def __getattr__(self, attr):
        if attr not in self._prop:
            raise AttributeError("TestEvent has no attribute %s." % attr)
        else:
            return self._prop[attr]


class TestSpinbox(BaseWidgetTest):
    def test_spinbox_init(self):
        spinbox = Spinbox(self.window, from_=0, to=10)
        spinbox.pack()
        self.window.update()

    def test_spinbox_bindings(self):
        spinbox = Spinbox(self.window, from_=0, to=10)
        spinbox.pack()
        self.window.update()
        event = TestEvent(widget=spinbox.frame)
        spinbox.focusin(event)
        spinbox.focusout(event)


class TestLimitVar(BaseWidgetTest):
    def test_limitvar_init(self):
        var = LimitVar(0, 100, self.window, 10)
        self.window.update()
        self.assertEqual(var.get(), 10)
        del var
        var = LimitVar('0', '100', self.window)
        self.window.update()
        self.assertEqual(var.get(), 0)
        del var
        var = LimitVar(0, 100, self.window, 200)
        self.window.update()
        self.assertEqual(var.get(), 100)
        del var
        var = LimitVar(0, 100, self.window, -2)
        self.window.update()
        self.assertEqual(var.get(), 0)
        del var
        self.assertRaises(ValueError, LimitVar, 'a', 0, self.window)
        self.assertRaises(ValueError, LimitVar, 0, 'b', self.window)
        self.assertRaises(ValueError, LimitVar, 100, 0, self.window)

    def test_limitvar_get(self):
        var = LimitVar(0, 100, self.window, 10)
        self.window.update()
        var.set(-2)
        self.window.update()
        self.assertEqual(var.get(), 0)
        var.set(102)
        self.window.update()
        self.assertEqual(var.get(), 100)
        var.set('12')
        self.window.update()
        self.assertEqual(var.get(), 12)
        var.set('a')
        self.window.update()
        self.assertEqual(var.get(), 0)
        self.assertEqual(tk.StringVar.get(var), '0')


class TestColorSquare(BaseWidgetTest):
    def test_colorsquare_init(self):
        cs = tkc.ColorSquare(self.window, hue=60, height=200, width=200)
        cs.pack()
        self.window.update()

    def test_colorsquare_bindings(self):
        cs = tkc.ColorSquare(self.window, hue=0, height=200, width=200)
        cs.pack()
        self.window.update()
        event = TestEvent(x=0, y=0)
        cs._on_click(event)
        self.assertEqual(cs.get(), ((0, 0, 0), (0, 100, 0), '#000000'))
        event.x = cs.winfo_width()
        cs._on_move(event)
        self.assertEqual(cs.get(), ((255, 0, 0), (0, 100, 100), '#FF0000'))

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
        ab.destroy()
        self.window.update()
        ab = tkc.AlphaBar(self.window, alpha=500, color=(255, 255, 2),
                          height=12, width=200)
        ab.pack()
        self.window.update()
        ab.destroy()
        self.window.update()
        ab = tkc.AlphaBar(self.window, alpha=-20, color=(255, 255, 2),
                          height=12, width=200)
        ab.pack()
        self.window.update()
        ab.destroy()
        self.window.update()
        var = tk.IntVar(self.window)
        ab = tkc.AlphaBar(self.window, alpha=200, color=(255, 255, 2),
                          height=12, width=200, variable=var)
        ab.pack()
        self.window.update()
        ab.destroy()
        self.window.update()
        var = tk.StringVar(self.window, 'a')
        ab = tkc.AlphaBar(self.window, alpha=200, color=(255, 255, 2),
                          height=12, width=200, variable=var)
        ab.pack()
        self.window.update()

    def test_alphabar_bindings(self):
        ab = tkc.AlphaBar(self.window, alpha=20, height=12, width=200)
        ab.pack()
        self.window.update()
        event = TestEvent(x=0, y=1)
        ab._on_click(event)
        self.window.update()
        self.assertEqual(ab.get(), 0)
        event.x = ab.winfo_width()
        ab._on_move(event)
        self.window.update()
        self.assertEqual(ab.get(), 255)

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
        ab._variable.set(455)
        self.window.update()
        self.assertEqual(ab.get(), 255)
        ab._variable.set(-55)
        self.window.update()
        self.assertEqual(ab.get(), 0)


class TestGradientBar(BaseWidgetTest):
    def test_gradientbar_init(self):
        gb = tkc.GradientBar(self.window, hue=800, height=12, width=200)
        gb.pack()
        self.window.update()
        gb.destroy()
        self.window.update()
        gb = tkc.GradientBar(self.window, hue=-20, height=12, width=200)
        gb.pack()
        self.window.update()
        gb.destroy()
        self.window.update()
        gb = tkc.GradientBar(self.window, hue=20, height=12, width=200)
        gb.pack()
        self.window.update()
        gb.destroy()
        self.window.update()
        var = tk.IntVar(self.window)
        gb = tkc.GradientBar(self.window, hue=20, height=12, width=200,
                             variable=var)
        gb.pack()
        self.window.update()
        gb.destroy()
        self.window.update()
        var = tk.StringVar(self.window, 'b')
        gb = tkc.GradientBar(self.window, hue=20, height=12, width=200,
                             variable=var)
        gb.pack()
        self.window.update()

    def test_gradientbar_bindings(self):
        gb = tkc.GradientBar(self.window, hue=20, height=12, width=200)
        gb.pack()
        self.window.update()
        event = TestEvent(x=0, y=1)
        gb._on_click(event)
        self.window.update()
        self.assertEqual(gb.get(), 0)
        event.x = gb.winfo_width()
        gb._on_move(event)
        self.window.update()
        self.assertEqual(gb.get(), 360)

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
        gb._variable.set(455)
        self.window.update()
        self.assertEqual(gb.get(), 360)
        gb._variable.set(-55)
        self.window.update()
        self.assertEqual(gb.get(), 0)


class TestColorPicker(BaseWidgetTest):
    def test_colorpicker_init(self):
        c = tkc.ColorPicker(self.window, color="red", title='Test')
        self.window.update()
        c.ok()
        self.assertEqual(c.get_color(),
                         ((255, 0, 0), (0, 100, 100), '#FF0000'))
        c.destroy()
        self.window.update()
        c = tkc.ColorPicker(self.window, color="red", title='Test', alpha=True)
        self.window.update()
        c.ok()
        self.assertEqual(c.get_color(),
                         ((255, 0, 0, 255), (0, 100, 100), '#FF0000FF'))
        c.destroy()
        self.window.update()
        c = tkc.ColorPicker(self.window, color="#ff0000", title='Test')
        self.window.update()
        c.ok()
        self.assertEqual(c.get_color(),
                         ((255, 0, 0), (0, 100, 100), '#FF0000'))
        c.destroy()
        self.window.update()
        c = tkc.ColorPicker(self.window, color="#ff0000", title='Test',
                            alpha=True)
        self.window.update()
        c.ok()
        self.assertEqual(c.get_color(),
                         ((255, 0, 0, 255), (0, 100, 100), '#FF0000FF'))
        c.destroy()
        self.window.update()
        c = tkc.ColorPicker(self.window, color="#ff000000", title='Test',
                            alpha=True)
        self.window.update()
        c.ok()
        self.assertEqual(c.get_color(),
                         ((255, 0, 0, 0), (0, 100, 100), '#FF000000'))
        c.destroy()
        self.window.update()
        c = tkc.ColorPicker(self.window, color="#ff000000", title='Test')
        self.window.update()
        c.ok()
        self.assertEqual(c.get_color(),
                         ((255, 0, 0), (0, 100, 100), '#FF0000'))
        c.destroy()
        self.window.update()
        c = tkc.ColorPicker(self.window, color=(255, 0, 0), title='Test')
        self.window.update()
        c.ok()
        self.assertEqual(c.get_color(),
                         ((255, 0, 0), (0, 100, 100), '#FF0000'))
        c.destroy()
        self.window.update()
        c = tkc.ColorPicker(self.window, color=(255, 0, 0), title='Test',
                            alpha=True)
        self.window.update()
        c.ok()
        self.assertEqual(c.get_color(),
                         ((255, 0, 0, 255), (0, 100, 100), '#FF0000FF'))
        c.destroy()
        self.window.update()
        c = tkc.ColorPicker(self.window, color=(255, 0, 0, 0), title='Test',
                            alpha=True)
        self.window.update()
        c.ok()
        self.assertEqual(c.get_color(),
                         ((255, 0, 0, 0), (0, 100, 100), '#FF000000'))
        c.destroy()
        self.window.update()
        c = tkc.ColorPicker(self.window, color=(255, 0, 0, 0), title='Test')
        self.window.update()
        c.ok()
        self.assertEqual(c.get_color(),
                         ((255, 0, 0), (0, 100, 100), '#FF0000'))
        c.destroy()
        self.window.update()

    def test_colorpicker_bindings(self):
        cp = tkc.ColorPicker(self.window, color=(0, 255, 0), title='Test',
                             alpha=True)
        self.window.update()
        event = TestEvent(x=0, y=1)
        cp.bar._on_click(event)
        self.window.update()
        self.assertEqual(cp.bar.get(), 0)
        cp._change_color(event)
        self.window.update()
        self.assertEqual(cp.hue.get(), 0)

        self.window.update()
        event = TestEvent(x=0, y=1)
        cp.alphabar._on_click(event)
        self.window.update()
        self.assertEqual(cp.alphabar.get(), 0)
        cp._change_alpha(event)
        self.window.update()
        self.assertEqual(cp.alpha.get(), 0)
        event.x = cp.alphabar.winfo_width()
        cp.alphabar._on_click(event)
        cp._change_alpha(event)
        self.window.update()

        cp.color_preview.focus_force()
        cp._unfocus(event)
        self.assertEqual(cp.focus_get(), cp)
        cp.hexa.focus_force()
        cp._unfocus(event)
        self.assertNotEqual(cp.focus_get(), cp)
        self.window.update()

        event = TestEvent(x=cp.square.winfo_width(), y=cp.square.winfo_height())
        cp.square._on_click(event)
        self.window.update()
        cp._change_sel_color(event)
        self.window.update()
        self.assertEqual(cp.square.get(), ((255, 255, 255), (0, 0, 100), '#FFFFFF'))
        self.assertEqual(cp.alpha.get(), 255)
        self.window.update()
        event = TestEvent(widget=tk.Label(self.window, bg='white'))
        cp._palette_cmd(event)
        self.window.update()
        self.assertEqual(cp.square.get(), ((255, 255, 255), (0, 0, 100), '#FFFFFF'))
        cp._reset_preview(event)
        self.window.update()
        self.assertEqual(cp.square.get(), ((0, 255, 0), (120, 100, 100), '#00FF00'))

        cp.hexa.focus_set()
        self.window.update()
        self.assertFalse(cp.hexa.selection_present())
        cp.hexa.event_generate('<Control-a>')
        self.assertEqual(cp.hexa.selection_get(), cp.hexa.get())

        s = tk.Spinbox(self.window, from_=0, to=100)
        s.insert(0, '20')
        s.pack()
        s.focus_set()
        cp._select_all_spinbox(TestEvent(widget=s))
        self.assertEqual(s.selection_get(), s.get())

    def test_colorpicker_functions(self):
        # with alpha
        cp = tkc.ColorPicker(self.window, color=(255, 0, 0, 100), title='Test',
                             alpha=True)
        self.window.update()
        # RGB
        cp.green.set(255)
        self.window.update()
        cp._update_color_rgb()
        self.window.update()
        self.assertEqual(cp.square.get(), ((255, 255, 0), (60, 100, 100), '#FFFF00'))
        self.window.update()
        # HSV
        cp.value.set(0)
        self.window.update()
        cp._update_color_hsv()
        self.window.update()
        self.assertEqual(cp.square.get(), ((0, 0, 0), (60, 100, 0), '#000000'))
        self.window.update()
        # HTML
        cp.hexa.delete(0, 'end')
        cp.hexa.insert(0, '#FF0000')
        self.window.update()
        cp._update_color_hexa()
        self.window.update()
        self.window.update()
        self.assertEqual(cp.square.get(), ((255, 0, 0), (0, 100, 100), '#FF0000'))
        self.assertEqual(cp.alpha.get(), 100)
        cp.hexa.delete(0, 'end')
        cp.hexa.insert(0, '#FFFF00FF')
        self.window.update()
        cp._update_color_hexa()
        self.window.update()
        self.window.update()
        self.assertEqual(cp.square.get(), ((255, 255, 0), (60, 100, 100), '#FFFF00'))
        self.assertEqual(cp.alpha.get(), 255)
        cp.hexa.delete(0, 'end')
        cp.hexa.insert(0, '#AAA')
        self.window.update()
        cp._update_color_hexa()
        self.window.update()
        self.window.update()
        self.assertEqual(cp.square.get(), ((255, 255, 0), (60, 100, 100), '#FFFF00'))
        self.assertEqual(cp.alpha.get(), 255)
        # ALPHA
        cp.alpha.set(0)
        self.window.update()
        cp._update_alpha()
        self.window.update()
        self.assertEqual(cp.get_color(), "")
        self.window.update()
        cp.ok()
        self.assertEqual(cp.get_color(),
                         ((255, 255, 0, 0), (60, 100, 100), "#FFFF0000"))
        self.window.update()

        # without alpha
        cp = tkc.ColorPicker(self.window, color=(255, 0, 0), title='Test')
        self.window.update()
        self.window.update()
        # RGB
        cp.green.set(255)
        self.window.update()
        cp._update_color_rgb()
        self.window.update()
        self.assertEqual(cp.square.get(), ((255, 255, 0), (60, 100, 100), '#FFFF00'))
        self.window.update()
        # HSV
        cp.value.set(0)
        self.window.update()
        cp._update_color_hsv()
        self.window.update()
        self.assertEqual(cp.square.get(), ((0, 0, 0), (60, 100, 0), '#000000'))
        self.window.update()
        # HTML
        cp.hexa.delete(0, 'end')
        cp.hexa.insert(0, '#FF0000')
        self.window.update()
        cp._update_color_hexa()
        self.window.update()
        self.window.update()
        self.assertEqual(cp.square.get(), ((255, 0, 0), (0, 100, 100), '#FF0000'))
        cp.hexa.delete(0, 'end')
        cp.hexa.insert(0, '#AAA')
        self.window.update()
        cp._update_color_hexa()
        self.window.update()
        self.window.update()
        self.assertEqual(cp.square.get(), ((255, 0, 0), (0, 100, 100), '#FF0000'))
        self.assertEqual(cp.get_color(), "")
        self.window.update()
        cp.ok()
        self.assertEqual(cp.get_color(),
                         ((255, 0, 0), (0, 100, 100), "#FF0000"))
        self.window.update()

    def test_askcolor(self):

        def test(event):
            event.widget.ok()
            self.assertEqual(event.widget.color[-1], '#FF0000')

        def events():
            self.window.update()
            c = list(self.window.children.values())[0]
            c.bind('<Visibility>', test)
            self.window.update()
            c.withdraw()
            self.window.update()
            c.deiconify()

        self.window.after(100, events)
        tkc.askcolor(parent=self.window)
