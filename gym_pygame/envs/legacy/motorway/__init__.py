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
from ..pygame import PyGameEnvironment 

DEFAULT_SIZE = (64,64)

class Car:

    def __init__(self, x, y, w, h, speed=2):
        self.position = np.array([x,y])
        self.size = np.array([w,h])
        self.speed = speed

    @property
    def center(self):
        return self.p + self.size/2

    def __str__(self):
        return "{0:.4f}".format(self.speed)
    
    def __repr__(self):
        return str(self)

physics = [
    {"up":np.array([0,-1]), "down":np.array([0,1])},                                         # simple
    {"up":np.array([0,-1]), "down":np.array([0,1]), "noop":np.array([0,0])},                 # simple + no-op
]

car_speed = [-1.6953, 0.5608, 1.0111, 0.3795, -0.3054, 0.8836, -0.6497, 1.5671]

class Motorway(PyGameEnvironment):

    def __init__(self, size=DEFAULT_SIZE, physics=physics[0], dtype=np.float32, format="CHW"):
        super(Motorway, self).__init__(list(physics.keys()), display_size=size, background_colour=(0,0,0), format=format, dtype=dtype)
        self.physics = physics
        self.player = Car(size[0]/2-size[0]/32, size[1]-size[1]/16, size[0]/16, size[1]/16)

        cspeed = 2
        ncars = 10 # (-2)
        inc = size[1]/(ncars-1)
        self.cars = [Car(0, i*inc, int(inc*2.5/3), int(inc*2/3), speed = car_speed[i]) for i in range(ncars-2)]

        self.__initial_state = copy.deepcopy((self.player, *self.cars))
        #print(self.__initial_state)

    def collision(self, player, car):
        return (player.position[0] < car.position[0] + car.size[0] and 
               player.position[0] + player.size[0] > car.position[0] and 
               player.position[1] < car.position[1] + car.size[1] and
               player.position[1] + player.size[1] > car.position[1])
            
    def step(self, action):
        #update player state
        self.player.position = self.player.position + self.player.speed * self.physics[self.actions[action]]
        
        self.player.position[1] = min(self.player.position[1], self.display_size[1]-self.player.size[1])
        done = self.player.position[1] <= 0
        reward = int(done)

        #update car state
        for car in self.cars:
            car.position[0] = (car.position[0] + car.speed + car.size[0]) % (self.display_size[0] + car.size[0])
            car.position[0] -= car.size[0]

            done = done or self.collision(self.player, car)
            reward = -int(done)

        # update graphics
        self.clear(self.background_colour) 
        self.fill_rect(self.player.position, self.player.size)

        for car in self.cars:
            self.fill_rect(car.position, car.size)
            #print(car.position, car.size)

        return self.get_image(), 0., done, None

    def reset(self):
        self.player, *self.cars = copy.deepcopy(self.__initial_state)

        self.clear(self.background_colour)
        self.fill_rect(self.player.position, self.player.size)
        for car in self.cars:
            self.fill_rect(car.position, car.size)

        return self.get_image()

def MotorwayNoop(**kwargs):
    return Motorway(physics=physics[1], **kwargs)