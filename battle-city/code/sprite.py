import pygame


MAP_TILE_WIDTH = 32
MAP_TILE_HEIGHT = 32

class SortedUpdates(pygame.sprite.RenderUpdates):
    """A sprite group that sorts sprites by depth."""

    def sprites(self):
        """The list of sprites in the group, sorted by depth."""
        return sorted(self.spritedict.keys(), key=lambda sprite: sprite.depth)

class Sprite(pygame.sprite.Sprite):
    """Sprite for animated items and base class for Tank"""
    is_player = False

    def __init__(self, position = (0, 0), frames = None):
        super(Sprite, self).__init__()
        if frames:
            self.frames = frames
        self.image = self.frames[0][0]
        self.rect = self.image.get_rect()
        self.position = position

    def get_position(self):
        """Check the current position of the sprite on the map"""
        return (self.rect.midbottom[0] - MAP_TILE_WIDTH // 2) // MAP_TILE_HEIGHT, (self.rect.midbottom[1] - MAP_TILE_HEIGHT) // MAP_TILE_HEIGHT

    def set_position(self, position):
        """Set the position of the sprite on the map"""
        self.rect.midbottom = position[0] * MAP_TILE_WIDTH + MAP_TILE_WIDTH / 2, position[1] * MAP_TILE_HEIGHT + MAP_TILE_HEIGHT
        self.depth = self.rect.midbottom[1]

    position = property(get_position, set_position)

    def move(self, dx, dy):
        """Change the position of the sprite"""
        self.rect.move_ip(dx, dy)
        self.depth = self.rect.midbottom[1]

    def update(self, *args):
        """Run the current animation"""
        self.animation.next()
