from .sprite import *
from .map import *

DIRECTIONS = ["up", "right", "down", "left"]
# Motion offsets
DX = [ 0,  1,  0, -1]
DY = [-1,  0,  1,  0]

class Player(Sprite):
    """Display and animate the player"""
    is_player = True

    def __init__(self, position, direction, lives):
        sprite_cache = TileCache("player.png")
        self.frames = sprite_cache["player.png"]
        Sprite.__init__(self, position)
        self.direction = direction
        self.lives = lives
        self.position = position
        self.image = self.frames[DIRECTIONS.index(self.direction)][0]

    def move_tank(self):
        direction = DIRECTIONS.index(self.direction)
        self.image = self.frames[direction][0]
        self.move(DX[direction], DY[direction])

    def update(self, *args):
        self.image = self.frames[DIRECTIONS.index(self.direction)][0]
