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

        self.background = self.level.render(self.level.name)

        for position, tile in level.tanks.items():
            if tile.get("player") == "true":
                sprite = Player(position, "up", 3)
                self.player = sprite
            if tile.get("enemy") == "true":
                sprite = Tank(position, "left", 1)
                self.enemy = sprite
            self.sprites.add(sprite)

    def control(self):
        """Handle the game controls"""
        keys = pg.key.get_pressed()

        def is_pressed(key):
            """Check is the specified key is pressed"""
            return self.pressed_key == key or keys[key]

        def move(direction):
            """Move the player in the specified direction"""
            self.player.direction = direction
            (next_x, next_y) = self.player.next_position()
            if not self.level.is_blocking(next_x, next_y):
                self.player.move()

        def shoot():
            (next_x, next_y) = self.player.next_position()
            bullet = self.player.shoot()
            self.sprites.add(bullet)
            self.level.bullets.append(bullet)

        if is_pressed(pgl.K_UP):
            move("up")
        elif is_pressed(pgl.K_DOWN):
            move("down")
        elif is_pressed(pgl.K_LEFT):
            move("left")
        elif is_pressed(pgl.K_RIGHT):
            move("right")
        if is_pressed(pgl.K_SPACE):
            bullet = shoot()

        self.pressed_key = None

    def update_bullets(self):
        for position, bullet in enumerate(self.level.bullets):
            bullet.move()


    def main(self):
        """The main game loop"""
        clock = pg.time.Clock()

        # Draw the screen
        self.screen.blit(self.background, (0, 0))
        self.overlays.draw(self.screen)
        pg.display.flip()

        while not self.game_over:
            #Update bullets' positions
            self.update_bullets()

            # Update sprites
            self.sprites.clear(self.screen, self.background)
            self.sprites.update()

            self.control()
            self.player.update()
            dirty = self.sprites.draw(self.screen)
            self.overlays.draw(self.screen)
            pg.display.update(dirty)
            clock.tick(10)

            for event in pg.event.get():
                if event.type == pgl.QUIT:
                    self.game_over = True
                elif event.type == pgl.KEYDOWN:
                    self.pressed_key = event.key
