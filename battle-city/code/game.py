import pygame as pg
import pygame.locals as pgl
from .level import *
from .sprite import *
from .tank import *


TILE_WIDTH = 32
TILE_HEIGHT = 32

class Game(object):
    """The main game object"""
    def __init__(self, current_level):
        self.pressed_key = None
        self.game_over = False
        self.create_level(Level(current_level, TILE_WIDTH, TILE_HEIGHT))
        self.screen = pg.display.get_surface()

    def create_level(self, level):
        """Creates a level and sets it as the current one"""
        self.sprites = SortedUpdates()
        self.overlays = pygame.sprite.RenderUpdates()
        self.level = level
        
        self.background, overlays = self.level.render(self.level.name)
            
        for position, tile in level.items.items():
            if tile.get("player") == "true":
                sprite = Player(position, "up", 3)
                self.player = sprite
            self.sprites.add(sprite)

        for (x, y), image in overlays.items():
            overlay = pygame.sprite.Sprite(self.overlays)
            overlay.image = image
            overlay.rect = image.get_rect().move(x * TILE_WIDTH, (y - 1) * TILE_HEIGHT)

    def control(self):
        """Handle the game controls"""
        keys = pg.key.get_pressed()

        def is_pressed(key):
            """Check is the specified key is pressed"""
            return self.pressed_key == key or keys[key]

        def move(direction):
            """Move the player in the specified direction"""
            x, y = self.player.position
            self.player.direction = direction
            direction = DIRECTIONS.index(direction)
            next_x = x + DX[direction]
            next_y = y + DY[direction]
            if not self.level.is_blocking(next_x, next_y ):
                self.player.move_tank()

        if is_pressed(pgl.K_UP):
            move("up")
        elif is_pressed(pgl.K_DOWN):
            move("down")
        elif is_pressed(pgl.K_LEFT):
            move("left")
        elif is_pressed(pgl.K_RIGHT):
            move("right")
        
    
    def main(self):
        """The main game loop"""
        clock = pg.time.Clock()
        
        # Draw the screen
        self.screen.blit(self.background, (0, 0))
        self.overlays.draw(self.screen)
        pg.display.flip()

        while not self.game_over:
            # Update sprites
            self.sprites.clear(self.screen, self.background)
            self.sprites.update()

            self.control()
            self.player.update()
            dirty = self.sprites.draw(self.screen)
            self.overlays.draw(self.screen)
            pg.display.update(dirty)
            clock.tick(15)

            for event in pg.event.get():
                if event.type == pgl.QUIT:
                    self.game_over = True
                elif event.type == pgl.KEYDOWN:
                    self.pressed_key = event.key
