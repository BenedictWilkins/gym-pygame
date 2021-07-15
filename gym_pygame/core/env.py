#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Created on 15-07-2021 16:16:51

    [Description]
"""
__author__ = "Benedict Wilkins"
__email__ = "benrjw@gmail.com"
__status__ = "Development"

import gym 
import numpy as np

from .core import PyGameCore

class PyGameEnvironment(gym.Env, PyGameCore):

    def __init__(self, display_shape=(1, 32, 32), background_colour=(0, 0, 0), format="CHW", dtype=np.float32):
        assert all([(x in format) for x in "CHW"]) # check format is valid 

        _if = np.array([format.index(i) for i in "CHW"])

        c, h, w = np.array(display_shape)[_if]
        if c != 1 and c != 3:
            raise ValueError(f"Invalid channels: {c}, did you forget to set the image format? (current format {format})")

        display_size = (w, h)
        grey_scale = c == 1
 
        super().__init__(display_size=display_size, background_colour=background_colour, format=format, dtype=dtype, grey_scale=grey_scale)

        self.observation_space = gym.spaces.Box(low=self.bounds[0], high=self.bounds[1], shape=self.shape, dtype=self.dtype)
        # NOTE: the action space is not defined yet, it must be defined in the subclass!

    # NOTE: define step and reset in a subclass!