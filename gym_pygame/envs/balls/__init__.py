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

class Ball:

    def __init__(self, x, y, r, speed=2):
        self.position = np.array([x,y])
        self.radius = r
        self.speed = speed

    def center(self):
        return self.position + self.size/2

    def update(self, env):
        pass

    def draw(self, env):
        env.fill_circle(self.position, self.radius)

class Player(Ball):

    def draw(self, env):
        env.fill_rect(self.position - self.radius, (self.radius*2, self.radius*2))
 
physics = [
    {"up":np.array([0,-1]), "down":np.array([0,1]), "noop":np.array([0,0])},  # simple + no-op
    {"up":np.array([0,-1]), "down":np.array([0,1]), "left":np.array([-1,0]), "right":np.array([1,0]), "noop":np.array([0,0])},  # simple + no-op
]

class Balls(PyGameEnvironment):

    def __init__(self, balls, size=DEFAULT_SIZE, physics=physics[0], dtype=np.float32, format="CHW"):
        super(Balls, self).__init__(list(physics.keys()), display_size=size, background_colour=(0,0,0), dtype=dtype, format=format)
        self.physics = physics
        self.balls = balls  
        self.__initial_state = copy.deepcopy(self.balls)
        self.display_size = np.array(self.display_size)
    
    def step(self, action):
        #update state
        self.update(action)
        self.draw()

        return self.get_image(), 0., False, None

    def draw(self):
        self.clear(self.background_colour) # clear graphics buffer
        for ball in self.balls:
            ball.draw(self)

    def update(self, action):
        self.balls[0].position += self.balls[0].speed * self.physics[self.actions[action]]
        for ball in self.balls:
            ball.update(self)
            ball.position[0] = np.clip(ball.position[0], 0, self.display_size[0])
            ball.position[1] = np.clip(ball.position[1], 0, self.display_size[1])

    def reset(self):
        self.balls = copy.deepcopy(self.__initial_state)
        self.draw()
        return self.get_image()

def BallsI(**kwargs):
    """ Two balls, each is independant of the other. One is control via action, the other moves up/down 
    until it hits the side then reverses direction.

    Returns:
        Balls: new Balls environment
    """
    class BallVertical(Ball):

        def __init__(self, *args, **kwargs):
            super(BallVertical, self).__init__(*args, **kwargs)
            self.trigger = False

        def update(self, env):
            if self.position[1] <= 0:
                self.trigger = True
            elif self.position[1] >= env.display_size[1]:
                self.trigger = False
            action = int(self.trigger)
            self.position += self.speed * env.physics[env.actions[action]]

    kwargs['physics'] = physics[1]
    kwargs['size'] = kwargs.get('size', DEFAULT_SIZE)
    s = kwargs['size'][1]
    r = s / 10
    balls = [Player(s/6,s/2 - r/2, r),
             BallVertical(s*5/6,s/2 - r/2, r)]

    return Balls(balls, **kwargs)  

def BallsC(**kwargs):

    class BallFollow(Ball):
        
        def update(self, env):
            # move towards the player ball
            target = env.balls[0].position
            v = target - self.position
            d = np.linalg.norm(v)
            if d > self.radius * 2:
                self.position += self.speed * (v / d)
            #else: ??
            #    self.position -= self.speed * (v / d)


    kwargs['physics'] = physics[1]
    kwargs['size'] = kwargs.get('size', DEFAULT_SIZE)
    s = kwargs['size'][1]
    r = s / 10
    balls = [Player(s/6,s/2 - r/2, r),
             BallFollow(s*5/6,s/2 - r/2, r)]

    return Balls(balls, **kwargs)

def BallsW(**kwargs):

    class BallWind(Player):
        
        def update(self, env):
            self.position += np.array([-self.speed/2, 0])

    kwargs['physics'] = physics[1]
    kwargs['size'] = kwargs.get('size', DEFAULT_SIZE)
    s = kwargs['size'][1]
    r = s / 10
    balls = [BallWind(s/2, s/2, r)]

    return Balls(balls, **kwargs)

def BallsO(**kwargs):

    class BlizzardBalls(Balls):

        def __init__(self, *args, **kwargs):
            super(BlizzardBalls, self).__init__(*args, **kwargs)
            self.blizzard_p = 0
            self.blizzard_n = 6
            self.blizzard_w = self.display_size[0] / self.blizzard_n
        
        def step(self, action):
            return super(BlizzardBalls, self).step(action)

        def update(self, action):
            super(BlizzardBalls, self).update(action)
            self.blizzard_p += 1
            self.blizzard_p = self.blizzard_p % self.blizzard_w
            #print(self.blizzard_p)

        def draw(self):
            super(BlizzardBalls, self).draw()
            for i in range(self.blizzard_n + 1):
                x = i * self.blizzard_w
                self.fill_rect(np.array([self.blizzard_p + x - self.blizzard_w, 0]), np.array([self.blizzard_w/2,self.display_size[1]]))

        def reset(self):
            self.blizzard_p = 0
            return super(BlizzardBalls, self).reset()

    kwargs['physics'] = physics[1]
    kwargs['size'] = kwargs.get('size', DEFAULT_SIZE)
    s = kwargs['size'][1]
    r = s / 10
    balls = [Player(s/2, s/2, r)]

    return BlizzardBalls(balls, **kwargs)

def BallsS(**kwargs):

    kwargs['physics'] = physics[1]
    kwargs['size'] = kwargs.get('size', DEFAULT_SIZE)
    s = kwargs['size'][1]
    r = s / 10
    balls = [Player(s/2, s/2, r)]

    return Balls(balls, **kwargs)





