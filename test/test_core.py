#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Created on 15-07-2021 15:47:57

    [Description]
"""
__author__ = "Benedict Wilkins"
__email__ = "benrjw@gmail.com"
__status__ = "Development"

import unittest


import numpy as np 

from gym_pygame.core import core
from gym_pygame.core import PyGameEnvironment

class TestPyGameEnvironment(unittest.TestCase):

    def test_env(self):
        env = PyGameEnvironment()
        img = env.get_image()


class TestCore(unittest.TestCase):

    def test_pygame_core_float32(self):
        display_size = (32,32)
        background_colour = (0,0,0)
        format = "CHW"
        dtype = np.float32
        grey_scale = False

        pgcore = core.PyGameCore(display_size=display_size, background_colour=background_colour, format=format, dtype=dtype, grey_scale=grey_scale)
        pgcore.draw_circle((0,0), 10)
        pgcore.update()
        img = pgcore.get_image()

        self.assertEqual(img.shape, (3, *display_size))
        self.assertEqual(img.dtype, dtype)
        self.assertEqual(img.max(), 1.)
        self.assertEqual(img.min(), 0.)

    def test_pygame_core_uint8(self):
        display_size = (32,32)
        background_colour = (0,0,0)
        format = "CHW"
        dtype = np.uint8
        grey_scale = False

        pgcore = core.PyGameCore(display_size=display_size, background_colour=background_colour, format=format, dtype=dtype, grey_scale=grey_scale)
        pgcore.draw_circle((0,0), 10)
        pgcore.update()
        img = pgcore.get_image()

        self.assertEqual(img.shape, (3, *display_size))
        self.assertEqual(img.dtype, dtype)
        self.assertEqual(img.max(), 255)
        self.assertEqual(img.min(), 0)


    def test_pygame_core_grey_scale(self):
        display_size = (31,33)
        background_colour = (0,0,0)
        format = "WHC"
        dtype = np.uint8
        grey_scale = True

        pgcore = core.PyGameCore(display_size=display_size, background_colour=background_colour, format=format, dtype=dtype, grey_scale=grey_scale)
        pgcore.draw_circle((0,0), 10)
        pgcore.update()
        img = pgcore.get_image()

        self.assertEqual(img.shape, (*display_size, 1))
        self.assertEqual(img.dtype, dtype)
        self.assertEqual(img.max(), 255)
        self.assertEqual(img.min(), 0)

if __name__ == '__main__':
    unittest.main()
