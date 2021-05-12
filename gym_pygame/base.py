#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 Created on 06-05-2021 12:17:49

 [Description]
"""
__author__ ="Benedict Wilkins"
__email__ = "benrjw@gmail.com"
__status__ ="Development"

import numbers

import pygame
import pygame.gfxdraw

import gym
import numpy as np

from functools import wraps

def format_image(image, fold, fnew):
    old = np.array([fold.index(i) for i in "CHW"])
    new = np.array([fnew.index(i) for i in "CHW"])
    swap = new[old]
    return image.transpose(*swap)

class PyGameBase:

    def __init__(self, display_size=(32,32), background_colour=(0,0,0), format="WHC", dtype=np.uint8):
        super().__init__()

        pygame.init()

        self.background_colour = background_colour
        self.display = pygame.display.set_mode(display_size) 

        # state format (default WHC uint8)
        if np.issubdtype(dtype, np.floating):
            format_dtype = lambda x: x.astype(dtype) / 255. #creates a copy?
            high = 1.
        elif np.issubdtype(dtype, np.integer):
            format_dtype = lambda x: x
            high = 255
        else:
            raise TypeError("Invalid dtype: {0}".format(dtype))
        format_shape = lambda x: format_image(x, "WHC", format)

        self.__format_image = lambda x: format_dtype(format_shape(x))
        self.display_size = display_size # W, H

    def get_image_raw(self):
        '''
            Get the current state as an image in WHC 0-255 format (default 3 channels). Creates a 
            direct copy of the pygame display pixel buffer.
        '''
        pygame.display.update()
        return pygame.surfarray.array3d(self.display)

    def get_image(self):
        '''
            Get the current state as an image in the format specified on creation of the environment. 
            Creates a copy of the pygame display pixel buffer.
        '''
        pygame.display.update()
        buffer = pygame.surfarray.pixels3d(self.display)
        return self.__format_image(buffer)

    def clear(self, colour=(0,0,0)):
        self.display.fill(colour)

    def fill_circle(self, position, radius, colour=(255,255,255)):
        pygame.gfxdraw.filled_circle(self.display, int(position[0]), int(position[1]), int(radius), colour)
        pygame.gfxdraw.aacircle(self.display, int(position[0]), int(position[1]), int(radius), colour)
      
    def draw_circle(self, position, radius, colour=(255,255,255)):
         pygame.gfxdraw.aacircle(self.display, int(position[0]), int(position[1]), int(radius), colour)
   
    def draw_rect(self, position, size, colour=(255,255,255)):
        pygame.gfxdraw.rectangle(self.display, (*position, *size), colour)

    def fill_rect(self, position, size, colour=(255,255,255)):
        pygame.gfxdraw.box(self.display, (*position, *size), colour)

    def draw_poly(self, poly, colour=(255,255,255)):
        pygame.gfxdraw.aapolygon(self.display, poly, colour)

    def fill_poly(self, poly, colour=(255,255,255)):
        pygame.gfxdraw.filled_polygon(self.display, poly, colour)
        pygame.gfxdraw.aapolygon(self.display, poly, colour)

    def quit(self):
        pygame.quit()