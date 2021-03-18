#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Created on 15-09-2020 18:44:37

    [Description]
"""
__author__ = "Benedict Wilkins"
__email__ = "benrjw@gmail.com"
__status__ = "Development"

import copy
import numpy as np
from ..pygame import PyGameEnvironment 

DEFAULT_SIZE = (64,64)

class Player:

    def __init__(self, x, y, w, h, speed=1):
        self.position = np.array([x,y])
        self.size = np.array([w,h])
        self.speed = 1

    def center(self):
        return self.position + self.size/2


physics = [
    {"up":np.array([0,-1]), "down":np.array([0,1])},                                         # simple
    {"up":np.array([0,-1]), "down":np.array([0,1]), "noop":np.array([0,0])},                 # simple + no-op
]

class Windy(PyGameEnvironment):

    def __init__(self, size=DEFAULT_SIZE, physics=physics[0], dtype=np.float32, format="CHW"):
        super(Windy, self).__init__(list(physics.keys()), display_size=size, background_colour=(0,0,0), dtype=dtype, format=format)
        self.physics = physics
        self.player = Player(size[0]- size[0]/8, size[1]*7/8, size[0]/8, size[1]/8)
        self.display_size = np.array(self.display_size)
        self.__initial_state = copy.deepcopy(self.player)

    def step(self, action):
        #update state
        self.player.position[0] -= 1 #wind
        self.player.position += self.player.speed * self.physics[self.actions[action]]
        self.player.position = np.clip(self.player.position, 0, self.display_size - self.player.size)

        # update graphics
        self.clear(self.background_colour) 
        self.fill_rect(self.player.position, self.player.size)

        done = self.player.position[0] == 0

        return self.get_image(), 0., done, None

    def reset(self):
        self.player = copy.deepcopy(self.__initial_state)
        self.clear(self.background_colour) # clear graphics buffer
        self.fill_rect(self.player.position, self.player.size)
        return self.get_image()

def WindyNoop(**kwargs):
    kwargs['physics'] = physics[1]
    return Windy(**kwargs)




