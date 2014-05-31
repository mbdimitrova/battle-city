import pygame
import pygame.locals


def load_tile_table(filename, width, height):
    image = pygame.image.load("../../resources/graphics/%s" % filename).convert()
    image_width, image_height = image.get_size()
    tile_table = []
    for tile_x in range(0, image_width/width):
        line = []
        tile_table.append(line)
        for tile_y in range(0, image_height/height):
            rectangle = (tile_x*width, tile_y*height, width, height)
            line.append(image.subsurface(rectangle))
    return tile_table

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((64, 32))
    screen.fill((255, 255, 255))
    table = load_tile_table("../../resources/graphics/level01.png", 32, 32)
    for x, row in enumerate(table):
        for y, tile in enumerate(row):
            screen.blit(tile, (x*32, y*32))
    pygame.display.flip()
    while pygame.event.wait().type != pygame.locals.QUIT:
        pass
