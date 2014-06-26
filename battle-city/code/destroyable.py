from .sprite import *
from .map import *


class Destroyable(Sprite):
    """Base class for bricks tiles and game base"""
    def __init__(self, position):
        sprite_cache = TileCache("destroyable.png")
        self.frames = sprite_cache["destroyable.png"]
        Sprite.__init__(self, position)


class BricksTile(Destroyable):
    """Bricks tile which can be destroyed"""
    def __init__(self, position):
        Destroyable.__init__(self, position)
        self.image = self.frames[0][0]


class PlayerBase(Destroyable):
    """The base of the player"""
    def __init__(self, position):
        Destroyable.__init__(self, position)
        self.image = self.frames[1][0]
