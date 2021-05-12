#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Created on 06-05-2021 11:50:14
"""
__author__ ="Benedict Wilkins"
__email__ = "benrjw@gmail.com"
__status__ ="Development"

import pybullet_envs
import numpy as np

from ...base import PyGameBase

class LocomotionVisualiser(PyGameBase):

    def __init__(self, env, display_size=(32,32), background_colour=(0,0,0), format="HWC", dtype=np.uint8):
        super().__init__(display_size=display_size, background_colour=background_colour, format=format, dtype=dtype)
        joints = env.robot.ordered_joints 

        self.num_joints = len(joints)


    def render(self, state):
        # structure of the state 
        # z - self.initial_z,       # position z
        # np.sin(angle_to_target),  # target ? 
        # np.cos(angle_to_target),  # target ?
        # 0.3 * vx,                 # body velocity y 
        # 0.3 * vy,                 # body velocity y 
        # 0.3 * vz,                 # body velocity z 
        # r                         # roll
        # p                         # pitch

        # (x, vx)                   # joint position/velocity x num_joints
        # ... 

        # feet contact              # contact of the robots feet with the floor
        # ...
        print(state)
        print(self.num_joints)
        print(state[8:8+2*self.num_joints])








