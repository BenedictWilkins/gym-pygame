#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 Created on 06-05-2021 12:17:49

 [Description]
"""
__author__ ="Benedict Wilkins"
__email__ = "benrjw@gmail.com"
__status__ ="Development"

import pygame
import pygame.gfxdraw

import numpy as np

from functools import wraps

class ImageFormat:
    
    def __init__(self, shape, format, dtype):
        # image format (pygame default is WHC uint8 3 channels)

        # format dtype
        if np.issubdtype(dtype, np.floating):
            self.format_dtype = self.format_dtype_float
            high = 1
        elif np.issubdtype(dtype, np.integer):
            self.format_dtype = self.format_dtype_int
            high = 255
        else:
            raise TypeError("Invalid dtype: {0}".format(dtype))

        self._pygame_format = np.array(["WHC".index(i) for i in "CHW"])
        self._format = np.array([format.index(i) for i in "CHW"])
        self._swap = self._format[self._pygame_format] # transpose image to correct format
        self._bounds = (0, high)
        self._shape = np.array(shape) # WHC
        self._dtype = dtype
        self.is_grey = self._shape[-1] == 1
        
    def __call__(self, x):
        return self.format_dtype(self.format_shape(x))

    def format_dtype(self, x):
        # this function is set in __init__ to either format_dtype_int or format_dtype_float
        raise NotImplementedError()
    
    def format_dtype_int(self, x):
        return x.astype(self.dtype)

    def format_dtype_float(self, x):
        x = x.astype(self.dtype)
        x /= 255.
        return x

    def format_shape(self, x):
        return x[:,:,:self._shape[-1]].transpose(*self._swap)

    @property
    def shape(self):
        return tuple(self._shape[self._swap])

    @property
    def dtype(self):
        return self._dtype

    @property
    def bounds(self):
        return self._bounds
    
    @property
    def width(self):
        return self._shape[0]

    @property
    def height(self):
        return self._shape[1]

    @property
    def channels(self):
        return self._shape[2]


class PyGameCore:
    """
        Wrapper for pygame.s
    """

    def __init__(self, display_size=(32, 32), background_colour=(0,0,0), format="WHC", dtype=np.uint8, grey_scale=False):
        super().__init__()

        pygame.init()

        self.background_colour = background_colour
        self.display = pygame.display.set_mode(display_size) 

        shape = (*display_size, 3**int(not grey_scale)) #(W,H,C) pygame default (will be modified in ImageFormat)
        self._imageformat = ImageFormat(shape, format, dtype)

    def get_image_raw(self):
        '''
            Get the current state as an image in WHC 0-255 format (default 3 channels). Creates a 
            copy of the pygame display pixel buffer.
        '''
        return pygame.surfarray.array3d(self.display)

    def get_image(self):
        '''
            Get the current state as an image in the format specified on creation of the environment. 
            Creates a copy of the pygame display pixel buffer.
        '''
        buffer = self.get_image_raw()
        return self._imageformat(buffer)

    def update(self):
        '''
            Update the pygame internal graphics buffer. This should be called before reading any graphics data.
        '''
        pygame.display.update()

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

    @property
    def dtype(self):
        return self._imageformat.dtype

    @property
    def shape(self):
        return self._imageformat.shape

    @property
    def bounds(self):
        return self._imageformat.bounds

    @property
    def width(self):
        return self._imageformat.width

    @property
    def height(self):
        return self._imageformat.height

    @property
    def channels(self):
        return self._imageformat.channels
