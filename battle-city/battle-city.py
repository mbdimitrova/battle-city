#!/usr/bin/env python3.3
import pygame

"""
This is an attempt to recreate
Battle City for NES
"""

from code.game import *

if __name__=='__main__':
    pygame.init()
    Game("level01").main()
