import configparser
import pygame
from pygame.locals import *
from .map import *


class Level(object):
    """Load and store map of the level and its items"""
    def __init__(self, filename, tile_width, tile_height):
        self.name = filename
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.tileset = ''
        self.map = []
        self.key = {}
        self.tanks = {}
        self.bullets = []
        self.map_width = 0
        self.map_height = 0
        self.load_map_file(filename)

    def load_map_file(self, filename):
        parser = configparser.ConfigParser()
        parser.read("resources/maps/%s.map" % filename)
        self.tileset = parser.get("level", "tileset")
        self.map = parser.get("level", "map").split("\n")

        for section in parser.sections():
            if len(section) == 1:
                description = dict(parser.items(section))
                self.key[section] = description
        self.map_width = len(self.map[0])
        self.map_height = len(self.map)

        for y, line in enumerate(self.map):
            for x, c in enumerate(line):
                if not self.is_wall(x, y) and 'sprite' in self.key[c]:
                    self.tanks[(x, y)] = self.key[c]
        print("[level.py] self.tanks", self.tanks)

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

    def is_flagged(self, x, y, flag):
        """Find out if the flag is set on the given position on the map"""
        value = self.get_tile(x, y).get(flag)
        return value == 'true'

    def tile_type(self, x, y, tile_type):
        """Is the specified position a tile of the given type?"""
        return self.get_tile(x, y).get("name") == tile_type

    def is_wall(self, x, y):
        """Is the specified position a wall?"""
        return self.is_flagged(x, y, 'wall')

    def is_blocking(self, x, y):
        """Is the specified postion a blocking element?"""
        if not 0 <= x < self.map_width or not 0 <= y < self.map_height:
            return True
        return self.is_flagged(x, y, 'block')

    def is_destroyable(self, x, y):
        """Is the specified position a tile which can be destroyed?"""
        return self.is_flagged(x, y, 'destroyable')

    def render(self, filename):
        """Draw the level"""
        pygame.init()
        view_width = self.map_width * self.tile_width
        view_height = self.map_height * self.tile_height
        screen = pygame.display.set_mode((view_width, view_height))
        image = pygame.Surface((view_width, view_height))

        self.map_cache = TileCache("stage.png",
                                   self.tile_width, self.tile_height)

        tiles = self.map_cache[self.tileset]

        for map_y, line in enumerate(self.map):
            for map_x, c in enumerate(line):

                # if the position is an obstacle
                if self.tile_type(map_x, map_y, "brick"):
                    tile = 1, 0
                elif self.tile_type(map_x, map_y, "steel"):
                    tile = 2, 0

                # if the position is the base
                elif self.tile_type(map_x, map_y, "base"):
                    tile = 6, 0

                else:
                    tile = 0, 0

                tile_image = tiles[tile[0]][tile[1]]
                image.blit(tile_image, (map_x * self.tile_width,
                                        map_y * self.tile_height))

        return image
