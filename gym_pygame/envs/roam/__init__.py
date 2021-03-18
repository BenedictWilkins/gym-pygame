#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 Created on 18-03-2021 11:47:46

 [Description]
"""
__author__ ="Benedict Wilkins"
__email__ = "benrjw@gmail.com"
__status__ ="Development"

import copy
import numpy as np
import pygame

from ..pygame import PyGameEnvironment 

physics = [
    {"up":np.array([0,-1]), "down":np.array([0,1]), "left":np.array([-1,0]), "right":np.array([1,0])},                                                   
    {"up":np.array([0,-1]), "down":np.array([0,1]), "left":np.array([-1,0]), "right":np.array([1,0]), "noop":np.array([0,0])},
]

DEFAULT_SIZE = (64, 64)

class Roam(PyGameEnvironment):

    def __init__(self, objects, size=DEFAULT_SIZE, physics=physics[0], dtype=np.float32, seed=None):
        super(Roam, self).__init__(list(physics.keys()), display_size=size, background_colour=(0,0,0), dtype=dtype, format="CHW")
        self.physics = physics
        self.objects = objects  
        self.__initial_state = copy.deepcopy(self.objects)
        self.display_size = np.array(self.display_size)
        
        self.random = np.random.RandomState(seed) # use this for randomness otherwise choose will not work!
        self.__initial_random_state = self.random.get_state()
        
        self.observation_space.low = self.observation_space.low[:1]
        self.observation_space.high = self.observation_space.high[:1]
        self.observation_space.shape = self.observation_space.low.shape

    def step(self, action):
        self.update(action)
        self.draw()
        return self.get_image()[:1], 0., False, None

    def draw(self):
        self.clear(self.background_colour) # clear graphics buffer
        for obj in self.objects:
            obj.draw(self)

    def update(self, action):
        self.objects[0].position += self.objects[0].speed * self.physics[self.actions[action]]
        for obj in self.objects:
            obj.update(self)
            obj.position[0] = np.clip(obj.position[0], 0, self.display_size[0])
            obj.position[1] = np.clip(obj.position[1], 0, self.display_size[1])

    def reset(self):
        self.objects = copy.deepcopy(self.__initial_state)
        self.random.set_state(self.__initial_random_state)
        self.draw()
        return self.get_image()[:1] # its grayscale anyway

class RoamStochatic(Roam):

    def step(self, *args, **kwargs):
        return super().step(*args, **kwargs)
    
    def reset(self, *args, **kwargs):
        return super().reset(*args, **kwargs)

    def update(self, action):
        if np.random.uniform() > 0.8:
            self.objects[0].position += self.objects[0].speed * self.physics[self.actions[action]] # move normally
        else:
            self.objects[0].position -= self.objects[0].speed * self.physics[self.actions[action]] # move backwards very far!

        for obj in self.objects:
            obj.update(self)
            obj.position[0] = np.clip(obj.position[0], 0, self.display_size[0])
            obj.position[1] = np.clip(obj.position[1], 0, self.display_size[1])

class Object:
    """
        Default object with some basic properties.
    """

    def __init__(self, x, y, rotation=0, speed=2):
        self.position = np.array([x,y])
        self.rotation = rotation
        self.speed = speed
    
    @property
    def rotation_matrix(self):
        return np.array([[np.cos(self.rotation), -np.sin(self.rotation)],
                         [np.sin(self.rotation), np.cos(self.rotation)]])

    def update(self, env):
        pass # no updates by default

    def draw(self, env):
        pass # by default is not drawn

class Rect(Object):
    
    def __init__(self, x, y, w, h, **kwargs):
        super(Rect, self).__init__(x, y, **kwargs)
        self.size = np.array([w,h])

    def draw(self, env):
        env.fill_rect(self.position - self.size/2, self.size)

def make_v0():
    kwargs = {}
    kwargs['physics'] = physics[0]
    kwargs['size'] = kwargs.get('size', DEFAULT_SIZE)
    s = kwargs['size'][1]
    r = s / 5
    objs = [Rect(s/2, s/2, r, r)]
    return Roam(objs, **kwargs)

def make_v1():
    kwargs = {}
    kwargs['physics'] = physics[0]
    kwargs['size'] = kwargs.get('size', DEFAULT_SIZE)
    s = kwargs['size'][1]
    r = s / 5
    objs = [Rect(s/2, s/2, r, r)]
    return RoamStochatic(objs, **kwargs)