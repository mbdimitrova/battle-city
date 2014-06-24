import pygame


TILE_WIDTH = 32
TILE_HEIGHT = 32

DIRECTIONS = ["up", "right", "down", "left"]

# Motion offsets
DX = [ 0,  1,  0, -1]
DY = [-1,  0,  1,  0]


class SortedUpdates(pygame.sprite.RenderUpdates):
    """A sprite group that sorts sprites by depth."""

    def sprites(self):
        """The list of sprites in the group, sorted by depth."""
        return sorted(self.spritedict.keys(), key=lambda sprite: sprite.depth)


class Sprite(pygame.sprite.Sprite):
    """Base class for tanks and bullets"""

    def __init__(self, position=(0, 0), frames=None):
        super(Sprite, self).__init__()
        if frames:
            self.frames = frames
        self.image = self.frames[0][0]
        self.rect = self.image.get_rect()
        self.position = position
        self.direction = None

    def get_position(self):
        """Check the current position of the sprite on the map"""
        x = (self.rect.midbottom[0] - TILE_WIDTH // 2) // TILE_HEIGHT
        y = (self.rect.midbottom[1] - TILE_HEIGHT) // TILE_HEIGHT
        return x, y

    def set_position(self, position):
        """Set the position of the sprite on the map"""
        x = position[0] * TILE_WIDTH + TILE_WIDTH // 2
        y = position[1] * TILE_HEIGHT + TILE_HEIGHT
        self.rect.midbottom = x, y
        self.depth = self.rect.midbottom[1]

    position = property(get_position, set_position)

    def next_position(self):
        x, y = self.position
        direction = DIRECTIONS.index(self.direction)
        next_x = x + DX[direction]
        next_y = y + DY[direction]
        return (next_x, next_y)

    def move(self):
        """Change the position of the sprite"""

        direction = DIRECTIONS.index(self.direction)
        self.image = self.frames[direction][0]
        dx = 4 * DX[direction]
        dy = 4 * DY[direction]
        for tick in range(8):
            self.rect.move_ip(dx, dy)
            self.depth = self.rect.midbottom[1]
            #yield None
