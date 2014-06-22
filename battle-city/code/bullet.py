from .sprite import *


class Bullet(Sprite):
    """Sprite for bullets"""
    def __init__(self, position, direction):
        sprite_cache = TileCache("bullet.png")
        self.frames = sprite_cache["bullet.png"]
        Sprite.__init__(self, position)
        self.direction = direction
        self.position = position
        self.image = self.frames[DIRECTIONS.index(self.direction)][0]
