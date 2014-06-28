import unittest
from code.level import *

class TestLevel(unittest.TestCase):

    def setUp(self):
        self.level = Level("level01", 32, 32)

    def test_level_created(self):
        self.assertTrue(self.level != None, "level is None")

    def test_map_added(self):
        self.assertTrue(self.level.map, "map is empty")

    def test_player_added(self):
        self.assertTrue(self.level.player, "no player")

    def test_tile_type(self):
        self.assertTrue(self.level.tile_type(0, 0, 'floor'),
                        "tile type is % s" % self.level.get_tile(0, 0).get("name"))

        self.assertTrue(self.level.tile_type(0, 7, 'steel'),
                        "tile type is % s" % self.level.get_tile(0, 7).get("name"))

        self.assertTrue(self.level.tile_type(3, 14, 'player'),
                        "tile type is % s" % self.level.get_tile(3, 14).get("name"))

    def test_is_blocking(self):
        self.assertTrue(self.level.is_blocking(1, 1),
                        "% s is not blocking" % self.level.get_tile(1, 1).get("name"))

        self.assertFalse(self.level.is_blocking(8, 2),
                        "% s is blocking" % self.level.get_tile(8, 2).get("name"))

    def test_is_player_out(self):
        for position, player in self.level.player.items():
            (x, y) = position
            self.assertFalse(self.level.is_out(x, y),
                             "player is outside")

    def test_are_bircks_destroyable(self):
        for position, brick in self.level.bricks.items():
            (x, y) = position
            self.assertTrue(self.level.is_destroyable(x, y),
                            "brick on (%d, %d) is not destroyable" % (x, y))

if __name__ == '__main__':
    unittest.main()
