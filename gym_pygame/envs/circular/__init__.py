#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Created on 15-09-2020 18:44:26

    [Description]
"""
__author__ = "Benedict Wilkins"
__email__ = "benrjw@gmail.com"
__status__ = "Development"

import copy
import numpy as np
import gym

from .. import PyGameEnvironment 

DEG2RAD = np.pi/180

class Player:

    def __init__(self, center, radius, angle, size, speed):
        super().__init__()
        self.center = center
        self.radius = radius
        self.angle  = angle
        self.size = size
        self.speed = speed

    @property
    def position(self):
        cx, cy = self.center
        r, a = self.radius, self.angle
        return np.array([cx + r * np.cos(a), cy + r * np.sin(a)])
        
class Circular(PyGameEnvironment):

    def __init__(self, actions, display_shape=(1, 64, 64), dtype=np.float32):
        super(Circular, self).__init__(display_shape = display_shape, background_colour=(0,0,0), format="CHW", dtype=dtype)
          
        self.physics = {"left":1, "right":-1, "noop":0}
        assert all((a in self.physics) for a in actions)
        self.actions = actions
        self.action_space = gym.spaces.Discrete(len(self.actions))
    
        radius = min(display_shape[1:]) / 3
        display_size = np.array(display_shape[1:])
        self.player = Player(display_size/2, radius, 0, np.array([6,6]), 2)

        self._initial_state = copy.deepcopy(self.player)

    def step(self, action):
        self.player.angle += DEG2RAD * self.player.speed * self.physics[self.actions[action]]
        self.clear()
        self.fill_rect(self.player.position - self.player.size/2, self.player.size)
        self.update()

        return self.get_image(), 0., False, None

    def reset(self):
        self.player = copy.deepcopy(self._initial_state)

        self.clear()
        self.fill_rect(self.player.position - self.player.size/2, self.player.size)
        self.update()

        return self.get_image()

class CircularRandom(Circular):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def reset(self):
        # random reset angle!
        self.player.angle = np.random.uniform() * 2 * np.pi
        self.draw()
        return self.get_image()

class CircularExpander(Circular):

    def __init__(self, *args, display_shape=(3,64,64), **kwargs):
        super().__init__(*args, display_shape=display_shape, **kwargs)

        self.expander = Player(np.array(display_shape[1:]) / 2, 0, 0, size=np.zeros(2), speed=0.5)
        self._initial_state = copy.deepcopy([self.player, self.expander])



    def step(self, action):
        self.player.angle += DEG2RAD * self.player.speed * self.physics[self.actions[action]]
        self.expander.angle += self.expander.speed

        # when expander fills the screen we are donse
        if self.expander.angle * 2 >= np.linalg.norm(np.array(self.observation_space.shape[1:])):
            self.expander.speed *= -1
        elif self.expander.angle <= 0:
            self.expander.speed *= -1

        self.clear()
        self.fill_circle(self.expander.position, self.expander.angle, colour=(0,255,0))
        self.fill_rect(self.player.position - self.player.size/2, self.player.size, colour=(255,0,0))
        self.update()

        return self.get_image(), 0., False, None

    def reset(self):
        self.player, self.expander = copy.deepcopy(self._initial_state)

        self.clear()
        self.fill_circle(self.expander.position, self.expander.angle, colour=(0,255,0))
        self.fill_rect(self.player.position - self.player.size/2, self.player.size, colour=(255,0,0))
        self.update()

        return self.get_image()


def make_v0():
    return Circular(["left", "right"])

def make_v1():
    return Circular(["left", "right", "noop"])

def make_v2():
    return CircularRandom(["left", "right"])

def make_v3():
    return CircularRandom(["left", "right", "noop"])

def make_v4():
    return CircularExpander(["left", "right"])

def make_v5():
    return CircularExpander(["left", "right", "noop"])