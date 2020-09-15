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
os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.environ["SDL_VIDEODRIVER"] = 'dummy'

from gym.envs.registration import register

from . import envs

_all__ = ('envs', )

register(id='paddles-v0', entry_point='gym_pygame.envs:Paddles')
register(id='paddles-v1', entry_point='gym_pygame.envs:PaddlesNoop')
register(id='paddles-v2', entry_point='gym_pygame.envs:PaddlesShared')

register(id='expander-v0', entry_point='gym_pygame.envs:Expander')
register(id='expander-v1', entry_point='gym_pygame.envs:ExpanderNoop')

register(id='circular-v0', entry_point='gym_pygame.envs:Circular')
register(id='circular-v1', entry_point='gym_pygame.envs:CircularNoop')