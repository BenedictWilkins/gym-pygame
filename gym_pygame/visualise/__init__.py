#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 Created on 06-05-2021 11:53:30

 [Description]
"""
__author__ ="Benedict Wilkins"
__email__ = "benrjw@gmail.com"
__status__ ="Development"

import logging

try:
    from . import pybullet
except ModuleNotFoundError as e:
    _WARN_MSG = "Optional Module: {0} is not found.".format(e.name)
    logging.getLogger("gym_pygame").info(_WARN_MSG)
