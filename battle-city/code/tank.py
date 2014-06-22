from .sprite import *
from .map import *


class Tank(Sprite):
    """Sprite for enemy tanks and base class for Player"""
    is_enemy = True

    def __init__(self, position, direction, lives):
        sprite_cache = TileCache("tanks.png")
        self.frames = sprite_cache["tanks.png"]
        Sprite.__init__(self, position)
        self.direction = direction
        self.lives = lives
        self.position = position
        self.image = self.frames[DIRECTIONS.index(self.direction)][0]

    def update(self, *args):
        self.image = self.frames[DIRECTIONS.index(self.direction)][0]


class Player(Tank):
    """Display and animate the player"""
    is_player = True

    def __init__(self, position, direction, lives):
        Tank.__init__(self, position, direction, lives)
        sprite_cache = TileCache("player.png")
        self.frames = sprite_cache["player.png"]

