#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Created on 15-07-2021 16:48:44

    [Description]
"""
__author__ = "Benedict Wilkins"
__email__ = "benrjw@gmail.com"
__status__ = "Development"

import numpy as np

class Entity:
    """
        Default entity with some basic properties.
    """
    def __init__(self, position, rotation=0, speed=1):
        self.position = np.array(position)
        self.rotation = rotation
        self.speed = speed
        
    @property
    def rotation_matrix(self):
        return np.array([[np.cos(self.rotation), -np.sin(self.rotation)],
                         [np.sin(self.rotation), np.cos(self.rotation)]])

    def update(self, env):
        pass # fill in subclass

    def draw(self, env):
        pass # by default is not drawn

class Ball(Entity):

    def __init__(self, position, radius, rotation=0, speed=1):
        super(Ball, self).__init__(position, rotation=rotation, speed=speed)
        self.radius = radius

    def draw(self, env):
        env.fill_circle(self.position, self.radius)

class Poly(Entity):

    def __init__(self, x, y, poly, rotation=0, speed=2):
        assert len(poly.shape) == 2 and poly.shape[1] == 2
        super(Poly, self).__init__(x, y, rotation=rotation, speed=speed)
        self.poly = poly
    
    def draw(self, env):
        poly = self.position + np.dot(self.poly, self.rotation_matrix)
        env.fill_poly(poly)

class Triangle(Poly): # triangular polygon that follows the player

    def __init__(self, x, y, r, **kwargs):
        poly = np.array([[r * np.cos(2*np.pi/3), r * np.sin(2*np.pi/3)],
                         [r * np.cos(4*np.pi/3), r * np.sin(4*np.pi/3)],
                         [r * np.cos(0),         r * np.sin(0)]])

            
        super(Triangle, self).__init__(x, y, poly, **kwargs)
        self.radius = r

        # rotate triangle so 0 rad is on x axis
        #self.rotation = np.pi / 2 
        #self.poly = np.dot(self.poly, self.rotation_matrix)
        #self.rotation = 0 # reset rotation
    

class Rect(Object):
    
    def __init__(self, x, y, w, h, **kwargs):
        super(Rect, self).__init__(x, y, **kwargs)
        self.size = np.array([w,h])

    def draw(self, env):
        env.fill_rect(self.position - self.size/2, self.size)

