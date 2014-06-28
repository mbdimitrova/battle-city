import pygame as pg
import pygame.locals as pgl
import math
from .level import *
from .sprite import *
from .tank import *
from .destroyable import *


TILE_WIDTH = 32
TILE_HEIGHT = 32


class Game(object):
    """The main game object"""
    def __init__(self, current_level):
        self.pressed_key = None
        self.game_over = False
        self.create_level(Level(current_level, TILE_WIDTH, TILE_HEIGHT))
        self.screen = pg.display.get_surface()
        self.killed = 0

    def create_level(self, level):
        """Creates a level and sets it as the current one"""
        self.sprites = SortedUpdates()
        self.overlays = pygame.sprite.RenderUpdates()
        self.level = level

        self.background = self.level.render(self.level.name)

        for position, tile in level.enemies.items():
            if tile.get("enemy") == "true":
                sprite = Tank(position, "left", 1)
                self.sprites.add(sprite)

        for position, tile in level.player.items():
             if tile.get("player") == "true":
                sprite = Player(position, "up", 3)
                self.player = sprite
                self.sprites.add(sprite)

        for position, tile in level.bricks.items():
            sprite = BricksTile(position)
            self.sprites.add(sprite)

        for position, tile in level.base.items():
            sprite = PlayerBase(position)
            self.base = sprite
            self.sprites.add(sprite)

    def control(self):
        """Handle the game controls"""
        keys = pg.key.get_pressed()

        def is_pressed(key):
            """Check is the specified key is pressed"""
            return self.pressed_key == key or keys[key]

        if is_pressed(pgl.K_UP):
            self.move_tank(self.player, "up")
        elif is_pressed(pgl.K_DOWN):
            self.move_tank(self.player, "down")
        elif is_pressed(pgl.K_LEFT):
            self.move_tank(self.player, "left")
        elif is_pressed(pgl.K_RIGHT):
            self.move_tank(self.player, "right")
        if is_pressed(pgl.K_SPACE):
            self.tank_shoot(self.player)

        self.pressed_key = None

    def move_tank(self, tank, direction):
        """Move the player in the specified direction"""
        tank.direction = direction
        (next_x, next_y) = tank.next_position()
        if not self.level.is_blocking(next_x, next_y) and not self.level.is_out(next_x, next_y):
            tank.move()

    def tank_shoot(self, tank):
        (next_x, next_y) = tank.next_position()
        if not self.level.is_blocking(next_x, next_y) or self.level.is_destroyable(next_x, next_y):
            bullet = tank.shoot()
            self.sprites.add(bullet)
            self.level.bullets.append(bullet)

    def update_bullets(self):
        for position, bullet in enumerate(self.level.bullets):
            (x, y) = bullet.position
            (next_x, next_y) = bullet.next_position()

            if self.is_enemy((next_x, next_y)):
                self.sprites.remove(bullet)
                self.level.bullets.remove(bullet)
                self.destroy((next_x, next_y))
                self.killed += 1

            if self.level.is_blocking(x, y):
                self.sprites.remove(bullet)
                self.level.bullets.remove(bullet)
                if self.level.is_destroyable(x, y):
                    self.destroy(bullet.position)
                    if self.level.is_base(x, y):
                        self.game_over = True

            elif self.level.is_out(x, y):
                self.sprites.remove(bullet)
                self.level.bullets.remove(bullet)

            elif self.level.is_wall(next_x, next_y) and not self.level.is_destroyable(next_x, next_y):
                self.sprites.remove(bullet)
                self.level.bullets.remove(bullet)

            elif self.player.position == (next_x, next_y):
                if self.player.is_killed():
                    self.game_over = True

            else:
                bullet.move()

    def is_enemy(self, position):
        """Is there an enemy tank on the given position?"""
        for sprite in self.sprites:
            if sprite.position == position and isinstance(sprite, Tank) and not isinstance(sprite, Player):
                return True
        return False

    def create_enemy(self):
        for position, tile in self.level.enemies.items():
            if tile.get("enemy") == "true":
                sprite = Tank(position, "left", 1)
                self.sprites.add(sprite)

    def destroy(self, position):
        """Destroy the element on the given position"""
        (x, y) = position
        for sprite in self.sprites:
            if sprite.position == position:
                brick = sprite
                self.sprites.remove(brick)

        if self.level.is_wall(x, y):
            self.level.bricks.pop(position)
            self.level.set_tile(x, y)

    def target_direction(self, enemy_position, enemy_direction):
        """Return the direction of the closest target for the given enemy tank"""
        delta_base = self.delta(self.base.position, enemy_position)
        delta_player = self.delta(self.player.position, enemy_position)
        if delta_base < delta_player:
            return self.find_direction(enemy_position, self.base.position)
        return self.find_direction(enemy_position, self.player.position)

    def find_direction(self, enemy_position, target_position):
        """Find the direction in which the enemy tank should move"""
        if enemy_position[0] < target_position[0]:
            return "right"
        elif enemy_position[0] > target_position[0]:
            return "left"
        else:
            if enemy_position[1] < target_position[1]:
                return "down"
            return "up"

    def delta(self, enemy_position, target_position):
        """Find the distance in tiles to the target"""
        coordinates = [x - y for x, y in zip(enemy_position, target_position)]
        return sum(int(math.fabs(x)) for x in coordinates)

    def control_enemies(self):
        """Controls the enemy tanks and their shooting"""
        for sprite in self.sprites:
            if isinstance(sprite, Tank) and not isinstance(sprite, Player):
                direction = self.target_direction(sprite.position, sprite.direction)
                sprite.move_to(direction)
                self.tank_shoot(sprite)

    def main(self):
        """The main game loop"""
        clock = pg.time.Clock()

        # Draw the screen
        self.screen.blit(self.background, (0, 0))
        self.overlays.draw(self.screen)
        pg.display.flip()
        # higher numbers => slower enemies
        enemy_control_time = 15
        enemy_create_time = 100
        timer = 0
        player_wins = 5

        while not self.game_over:
            #Update bullets' positions and enemy tanks
            self.update_bullets()
            if timer % enemy_control_time == 0:
                self.control_enemies()
                timer += 1
            elif timer >= enemy_create_time:
                self.create_enemy()
                timer = 0
            else:
                timer += 1

            # Update sprites
            self.sprites.clear(self.screen, self.background)
            self.sprites.update()

            self.control()
            self.player.update()
            dirty = self.sprites.draw(self.screen)
            self.overlays.draw(self.screen)
            pg.display.update(dirty)

            if self.killed >= player_wins:
                print("YOU WIN!")
                self.game_over = True
            clock.tick(10)

            for event in pg.event.get():
                if event.type == pgl.QUIT:
                    self.game_over = True
                elif event.type == pgl.KEYDOWN:
                    self.pressed_key = event.key

        print("GAME OVER")
