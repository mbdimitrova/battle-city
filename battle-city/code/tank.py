from .sprite import *
from .map import *
from .bullet import *


class Tank(Sprite):
    """Sprite for enemy tanks and base class for Player"""

    def __init__(self, position, direction, lives):
        sprite_cache = TileCache("tanks.png")
        self.frames = sprite_cache["tanks.png"]
        Sprite.__init__(self, position)
        self.direction = direction
        self.lives = lives
        self.position = position
        self.image = self.frames[DIRECTIONS.index(self.direction)][0]
        self.is_enemy = True

    def update(self, *args):
        self.image = self.frames[DIRECTIONS.index(self.direction)][0]

    def shoot(self):
        (next_x, next_y) = self.next_position()
        bullet = Bullet((next_x, next_y), self.direction)
        return bullet

    def move_to(self, direction):
        """Changes the direction and moves in the new direction"""
        self.direction = direction
        self.move()

    def is_killed(self):
        self.lives -= 1
        return self.lives == 0


class Player(Tank):
    """Display the player"""

    def __init__(self, position, direction, lives):
        Tank.__init__(self, position, direction, lives)
        self.is_enemy = False
        sprite_cache = TileCache("player.png")
        self.frames = sprite_cache["player.png"]
