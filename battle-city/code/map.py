import pygame
import pygame.locals


class TileCache:
    """Load the tilesets lazily into global cache"""

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cache = {}

    def __getitem__(self, filename):
        """Return a table of tiles, load from disk if needed"""

        key = (filename, self.width, self.height)
        try:
            return self.cache[key]
        except KeyError:
            tile_table = self.load_tile_table(filename, self.width, self.height)
            self.cache[key] = tile_table
            return tile_table

    def load_tile_table(self, filename, width, height):
        """Load an image and split it into tiles"""

        image = pygame.image.load("resources/graphics/stage.png").convert()
        image_width, image_height = image.get_size()
        tile_table = []
        for tile_x in range(0, image_width // width):
            line = []
            tile_table.append(line)
            for tile_y in range(0, image_height // height):
                rectangle = (tile_x * width, tile_y * height, width, height)
                line.append(image.subsurface(rectangle))
        return tile_table
