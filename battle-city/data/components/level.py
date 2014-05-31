import ConfigParser
import pygame
from pygame.locals import *
from map import *


SCREEN_WIDTH = 416
SCREEN_HEIGHT = 480
MAP_TILE_WIDTH = 32
MAP_TILE_HEIGHT = 32
LEVEL01 = "level01.png"
MAP = "../../resources/maps/level01.map"


class Level(object):
    def load_file(self, filename="level01.map"):
        self.map = []
        self.key = {}
        parser = ConfigParser.ConfigParser()
        parser.read(filename)
        self.tileset = parser.get("level", "tileset")
        self.map = parser.get("level", "map").split("\n")
        for section in parser.sections():
            if len(section) == 1:
                desc = dict(parser.items(section))
                self.key[section] = desc
        self.width = len(self.map[0])
        self.height = len(self.map)

    def get_tile(self, x, y):
        try:
            char = self.map[y][x]
        except IndexError:
            return {}
        try:
            return self.key[char]
        except KeyError:
            return {}

    def get_tile(self, x, y):
        """Find out what's at the specified position of the map"""
        try:
            char = self.map[y][x]
        except IndexEror:
            return {}
        try:
            return self.key[char]
        except KeyError:
            return {}

    def get_bool(self, x, y, flag):
        """Find out if the specified flag is set on the specified position on the map"""
        value = self.get_tile(x, y).get(flag)
        return value in (True, 1, 'yes', 'true', 'True', 'Yes', '1', 'on', 'On')

    def is_tile(self, x, y, tile_type):
        """Is the specified position a tile of the given type?"""
        return self.get_tile(x, y).get("name") == tile_type

    def is_blocking(self, x, y):
        """Is the specified postion a blocking element?"""
        if not 0 <= x < self.width or not 0 <= y < self.height:
            return True
        return self.get_bool(x, y, 'block')

    def is_destroyable(self, x, y):
        """Is the specified position a tile which can be destroyed?"""

    def render(self):
        tiles = MAP_CACHE[self.tileset]
        image = pygame.Surface((self.width*MAP_TILE_WIDTH, self.height*MAP_TILE_HEIGHT))
        overlays = {}
        for map_y, line in enumerate(self.map):
            for map_x, c in enumerate(line):
                # if the position is an obstacle
                if self.is_tile(map_x, map_y, "brick"):
                    tile = 1, 0
                elif self.is_tile(map_x, map_y, "steel"):
                    tile = 2, 0
                # if the position is blank
                else:
                    tile = 0, 0
                    pass # overlays...
                tile_image = tiles[tile[0]][tile[1]]
                image.blit(tile_image,
                        (map_x*MAP_TILE_WIDTH, map_y*MAP_TILE_HEIGHT))
        return image

if __name__ == "__main__":
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    MAP_CACHE = { LEVEL01: load_tile_table(LEVEL01, MAP_TILE_WIDTH, MAP_TILE_HEIGHT)}

    level = Level()
    level.load_file(MAP)

    clock = pygame.time.Clock()

    # overlays...
    screen.blit(level.render(), (0, 0))
    #overlays...
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
