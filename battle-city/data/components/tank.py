from .. import constants as c


class Tank:
    def __init__(self, x, y, direction, lives, die_after):
        """Sets up a tank"""
        self.x = x
        self.y = y
        self.direction = direction
        self.lives = lives
        self.die_after = die_after

    def move(self, direction):
        """Moves the tank in the given direction"""
        self.direction = direction
        if direction == c.DOWN:
            self.y -= 1
        elif direction == c.UP:
            self.y += 1
        elif direction == c.LEFT:
            self.x -= 1
        elif direction == c.RIGHT:
            self.x += 1
        
