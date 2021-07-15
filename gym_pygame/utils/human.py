#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Created on 15-07-2021 16:38:09

    [Description]
"""
__author__ = "Benedict Wilkins"
__email__ = "benrjw@gmail.com"
__status__ = "Development"

import os
import pygame

class KeyboardPolicy: # TODO check it works...

    def __init__(self, action_space):
        # if this policy is created assume that we want to render the game...
        print(os.environ["SDL_VIDEODRIVER"])
        assert os.environ["SDL_VIDEODRIVER"] != "dummy" 
        self.action_map = [None] * action_space.n

    def wait(self, sleep=0):
        pygame.time.wait(sleep)

    def quit(self):
        pygame.quit()

    def __call__(self):
        while True: 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                    return
                elif event.type == pygame.KEYDOWN and event.key in self.action_map:
                    return self.action_map.index(event.key)