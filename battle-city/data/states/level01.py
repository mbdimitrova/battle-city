import pygame
import pygame.locals
from ..components.map import load_tile_table
from ..components.level import *



MAP_TILE_WIDTH = 32
MAP_TILE_HEIGHT = 32
LEVEL01 = "level01.png"
LEVEL01_MAP= "level01.map"

def initialize_level01():
    level = Level()
    level.load_file(LEVEL01_MAP)

    clock = pygame.time.Clock()

    # overlays...
    screen.blit(level.render(), (0, 0))

    pygame.display.flip()

    game_over = False
    while not game_over:
        # draw all objects here
        #overlays
        pygame.display.flip()
        clock.tick(15)
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                game_over = True
            elif event.type == pygame.locals.KEYDOWN:
                pressed_key = event.key
