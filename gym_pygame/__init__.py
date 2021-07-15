#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Created on 15-09-2020 18:44:00

    [Description]
"""
__author__ = "Benedict Wilkins"
__email__ = "benrjw@gmail.com"
__status__ = "Development"

import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
#OLD_VDRIVER = os.environ['SDL_VIDEODRIVER']
os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.environ["SDL_VIDEODRIVER"] = 'dummy'

def render(*args, **kwargs):
    """ Render an environment using a pygame window, must be called before any environment is created. """
    os.environ['SDL_VIDEODRIVER'] = ""

from gym.envs.registration import register

from .core import PyGameEnvironment

register(id="Alone-v0", entry_point="gym_pygame.envs.alone:make_v0")
register(id="Alone-v1", entry_point="gym_pygame.envs.alone:make_v1")

register(id="Circular-v0", entry_point="gym_pygame.envs.circular:make_v0")
register(id="Circular-v1", entry_point="gym_pygame.envs.circular:make_v1")
register(id="Circular-v2", entry_point="gym_pygame.envs.circular:make_v2")
register(id="Circular-v3", entry_point="gym_pygame.envs.circular:make_v3")

# expander versions
register(id="Circular-v4", entry_point="gym_pygame.envs.circular:make_v4")
register(id="Circular-v5", entry_point="gym_pygame.envs.circular:make_v5")

register(id="Duo-v0", entry_point="gym_pygame.envs.duo:make_v0")
register(id="Duo-v1", entry_point="gym_pygame.envs.duo:make_v1")

register(id="Windy-v0", entry_point="gym_pygame.envs.windy:make_v0")
register(id="Windy-v1", entry_point="gym_pygame.envs.windy:make_v1")

"""
_all__ = ('envs', 'visualise')

register(id="Roam-v0", entry_point='gym_pygame.envs.roam:make_v0')
register(id="Roam-noop-v0", entry_point='gym_pygame.envs.roam:make_noop_v0')
register(id="Roam-v1", entry_point='gym_pygame.envs.roam:make_v1')

#register(id='Paddles-v0', entry_point='gym_pygame.envs:Paddles')
#register(id='Paddles-v1', entry_point='gym_pygame.envs:PaddlesNoop')
#register(id='Paddles-v2', entry_point='gym_pygame.envs:PaddlesShared')

#register(id='Expander-v0', entry_point='gym_pygame.envs:Expander')
#register(id='Expander-v1', entry_point='gym_pygame.envs:ExpanderNoop')

#register(id='Circular-v0', entry_point='gym_pygame.envs:Circular')
#register(id='Circular-v1', entry_point='gym_pygame.envs:CircularNoop')

#register(id='Motorway-v0', entry_point='gym_pygame.envs:Motorway')
#register(id='Motorway-v1', entry_point='gym_pygame.envs:MotorwayNoop')

#register(id='Windy-v0', entry_point='gym_pygame.envs:Windy')
#register(id='windy-v1', entry_point='gym_pygame.envs:WindyNoop')
"""