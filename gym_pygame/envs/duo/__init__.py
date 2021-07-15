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

    def update(self, env, action):
        self.position += self.speed * env.physics[env.actions[action]]
        self.position[0] = np.clip(self.position[0], 0, env.observation_space.shape[2])
        self.position[1] = np.clip(self.position[1], 0, env.observation_space.shape[1])

    def draw(self, env):
        env.fill_rect(self.position - self.size/2, self.size)

class MultiDiscrete(gym.spaces.Space):

    def __init__(self, *n):
        assert len(n) > 1
        self.action_spaces = [gym.spaces.Discrete(i) for i in n]

    def sample(self):
        return [space.sample() for space in self.action_spaces]
    
    def contains(self, x):
        return all(space.contains(a) for (space, a) in zip(self.action_spaces, x))

class Duo(PyGameEnvironment):

    def __init__(self, actions, display_size=(64,64), dtype=np.float32):
        super(Duo, self).__init__(display_shape=(1, *display_size), background_colour=(0,0,0), dtype=dtype, format="CHW")

        self.physics = {"up":np.array([0,-1]), "down":np.array([0,1]), "left":np.array([-1,0]), "right":np.array([1,0]), "noop":np.array([0,0])}
        assert all((a in self.physics) for a in actions)
        self.actions = actions
        self.action_space = MultiDiscrete(*([len(self.actions)]*2))

        self.players = [Player(np.array(display_size)/3, np.array([6,6]),2),
                        Player(np.array(display_size)*2/3, np.array([6,6]),2)]
        self._initial_state = copy.deepcopy(self.players)

    def step(self, actions):
        assert self.action_space.contains(actions)
        for action, player in zip(actions, self.players):
            player.update(self, action)
        self.clear()
        for player in self.players:
            player.draw(self)
        self.update()
        return self.get_image(), 0., False, None

    def reset(self):
        self.players = copy.deepcopy(self._initial_state)
        self.clear()
        for player in self.players:
            player.draw(self)

        self.update()
        return self.get_image()

def make_v0():
    return Duo(["up", "down", "left", "right"], display_size=(64,64), dtype=np.float32)

def make_v1():
    return Duo(["up", "down", "left", "right", "noop"], display_size=(64,64), dtype=np.float32)