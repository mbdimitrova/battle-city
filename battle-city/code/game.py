import pygame as pg
import pygame.locals as pgl
from .level import *
from .sprite import *


TILE_WIDTH = 32
TILE_HEIGHT = 32

class Game(object):
    """The main game object"""
    def __init__(self, current_level):
        self.pressed_key = None
        self.game_over = False
        self.level = Level(current_level, TILE_WIDTH, TILE_HEIGHT)
        self.sprites = SortedUpdates()
        self.background = self.level.render(current_level)
        self.screen = pg.display.get_surface()

    def control(self):
        pass #TODO

    def main(self):
        """The main game loop"""
        clock = pg.time.Clock()
        
        # Draw the screen
        self.screen.blit(self.background, (0, 0))
        pg.display.flip()

        #Main loop
        while not self.game_over:
            self.sprites.clear(self.screen, self.background)
            self.sprites.update()
            clock.tick(15)
            for event in pg.event.get():
                if event.type == pgl.QUIT:
                    self.game_over = True
                elif event.type == pgl.KEYDOWN:
                    self.pressed_key = event.key
