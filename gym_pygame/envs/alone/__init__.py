#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Created on 15-07-2021 17:01:28

    [Description]
"""
__author__ = "Benedict Wilkins"
__email__ = "benrjw@gmail.com"
__status__ = "Development"

import copy
import numpy as np
import gym

from .. import PyGameEnvironment 

class Player:

    def __init__(self, position, size, speed):
        self.position = position
        self.size = size
        self.speed = speed
       
    def draw(self, env):
        env.fill_rect(self.position - self.size/2, self.size)

class Alone(PyGameEnvironment):

    def __init__(self, actions, display_size=(32,32), dtype=np.float32):
        super(Alone, self).__init__(display_shape=(1, *display_size), background_colour=(0,0,0), dtype=dtype, format="CHW")

        self.physics = {"up":np.array([0,-1]), "down":np.array([0,1]), "left":np.array([-1,0]), "right":np.array([1,0]), "noop":np.array([0,0])}
        assert all((a in self.physics) for a in actions)
        self.actions = actions
        self.action_space = gym.spaces.Discrete(len(self.actions))

        self.player = Player(np.array(display_size)/2,
                             np.array([6,6]),
                             2)

        self._initial_state = copy.deepcopy(self.player)

    def step(self, action):
        self.player.position += self.player.speed * self.physics[self.actions[action]]
        self.player.position[0] = np.clip(self.player.position[0], 0, self.observation_space.shape[2])
        self.player.position[1] = np.clip(self.player.position[1], 0, self.observation_space.shape[1])

        self.clear()
        self.player.draw(self)
        self.update()
        return self.get_image(), 0., False, None

    def reset(self):
        self.player = copy.deepcopy(self._initial_state)
        self.clear()
        self.player.draw(self)
        self.update()
        return self.get_image()

def make_v0():
    return Alone(["up", "down", "left", "right"], display_size=(32,32), dtype=np.float32)

def make_v1():
    return Alone(["up", "down", "left", "right", "noop"], display_size=(32,32), dtype=np.float32)
