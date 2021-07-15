#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Created on 09-12-2020 17:25:23

    [Description]
"""
__author__ = "Benedict Wilkins"
__email__ = "benrjw@gmail.com"
__status__ = "Development"

DEFAULT_SIZE = (64,64)

import copy
import numpy as np
import pygame
from gym_pygame import PyGameEnvironment 

physics = [
    {"up":np.array([0,-1]), "down":np.array([0,1]), "noop":np.array([0,0])},                                                   
    {"up":np.array([0,-1]), "down":np.array([0,1]), "left":np.array([-1,0]), "right":np.array([1,0]), "noop":np.array([0,0])},
]

class Objects(PyGameEnvironment):

    def __init__(self, objects, size=DEFAULT_SIZE, physics=physics[0], dtype=np.float32, format="CHW", seed=None):
        super(Objects, self).__init__(list(physics.keys()), display_size=size, background_colour=(0,0,0), dtype=dtype, format=format)
        self.physics = physics
        self.objects = objects  
        self.__initial_state = copy.deepcopy(self.objects)
        self.display_size = np.array(self.display_size)
        
        self.random = np.random.RandomState(seed) # use this for randomness otherwise choose will not work!
        self.__initial_random_state = self.random.get_state()

        self.docs = "Objects environment base class."

    def step(self, action):
        self.update(action)
        self.draw()
        return self.get_image(), 0., False, None

    def choose(self, action):
        """
            Like step but it does not advance the environment to the next state.
        """
        old_display, old_objects, random_state = self.display, self.objects, self.random.get_state()

        self.display = pygame.Surface(self.display_size)
        self.objects = copy.deepcopy(self.objects)

        self.update(action) 
        self.draw()

        buffer = pygame.surfarray.pixels3d(self.display)
        img = self._PyGameEnvironment__format_image(buffer)
        result = (img, 0. , False, None)

        self.display, self.objects = old_display, old_objects
        self.random.set_state(random_state)

        return result


    def draw(self):
        self.clear(self.background_colour) # clear graphics buffer
        for obj in self.objects:
            obj.draw(self)

    def update(self, action):
        #print("UPDATE", action)
        self.objects[0].position += self.objects[0].speed * self.physics[self.actions[action]]
        for obj in self.objects:
            obj.update(self)
            obj.position[0] = np.clip(obj.position[0], 0, self.display_size[0])
            obj.position[1] = np.clip(obj.position[1], 0, self.display_size[1])

    def reset(self):
        self.objects = copy.deepcopy(self.__initial_state)
        self.random.set_state(self.__initial_random_state)
        self.draw()
        return self.get_image()


class RMPolicy:
    """ Policy that chooses a random location and moves to it (more interesting than a uniform random policy) """ 

    def __init__(self, env, noop_prob=0.1):
        self.env = env # hacks to get internal state while deciding
        self.target = np.array([np.random.randint(env.display_size[0]), np.random.randint(env.display_size[1])])
        self.noop_prob = noop_prob

    def __call__(self, *args, **kwargs):
        env = self.env
        actor_pos = env.objects[0].position
        d = self.target - actor_pos

        if np.linalg.norm(d) < np.linalg.norm([env.objects[0].speed]*2): 
            self.target = np.array([np.random.randint(env.display_size[0]), np.random.randint(env.display_size[1])])
            return self() # target was reached, set a new target and move to it
        
        # compute action to get to target
        xs, ys = np.sign(d[0]), np.sign(d[1])
        possible_actions = [] # noop is always possible (with small prob)
        if np.abs(d[0]) >= env.objects[0].speed:
            xs = int(((xs + 1) // 2) + 2)
            possible_actions.append(xs)
        if np.abs(d[1]) >= env.objects[0].speed:
            ys = int((ys + 1) // 2)
            possible_actions.append(ys)
        
        assert len(possible_actions) > 0
        a = np.random.choice(possible_actions)
        a = np.random.choice([4, a], p=[self.noop_prob, 1-self.noop_prob])
        return a
        
        







