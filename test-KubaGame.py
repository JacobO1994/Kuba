import unittest
from KubaGame import *


class MyTestCase(unittest.TestCase):
    def test_winner(self):
        game = KubaGame(("Jake", 'W'), ("Kenna", 'B'))
        game.make_move("Jake", (6, 5), "F")
        game.make_move("Kenna", (0, 6), "B")
        game.make_move("Jake", (4, 5), "L")
        game.make_move("Kenna", (0, 5), "B")
        game.make_move("Jake", (4, 4), "L")
        game.make_move("Kenna", (2, 6), "L")
        game.make_move("Jake", (4, 3), "L")
        game.make_move("Kenna", (2, 5), "L")
        game.make_move("Jake", (4, 2), "L")
        game.make_move("Kenna", (2, 4), "L")
        game.make_move("Jake", (4, 1), "L")
        game.make_move("Kenna", (2, 3), "L")
        game.make_move("Jake", (0, 0), "B")
        game.make_move("Kenna", (5, 0), "R")
        game.make_move("Jake", (4, 0), "F")
        game.make_move("Kenna", (5, 1), "R")
        game.make_move("Jake", (3, 0), "R")
        game.make_move("Kenna", (5, 2), "R")
        game.make_move("Jake", (3, 1), "R")
        game.make_move("Kenna", (5, 3), "R")
        game.make_move("Jake", (3, 2), "R")
        game.make_move("Kenna", (5, 4), "R")
        game.make_move("Jake", (3, 3), "R")
        game.make_move("Kenna", (6, 0), "F")
        game.make_move("Jake", (3, 4), "R")
        self.assertEqual("Jake", game.get_winner())

    def test_capture_one_left_board(self):
        game = KubaGame(("Jake", 'W'), ("Kenna", 'B'))
        game.make_move("Jake", (6, 6), 'F')
        game.make_move("Kenna", (0, 6), 'B')
        game.make_move("Jake", (5, 6), 'F')
        game.make_move("Kenna", (6, 0), 'R')
        game.make_move("Jake", (3, 6), 'L')
        game.make_move("Kenna", (6, 1), 'R')
        game.make_move("Jake", (3, 5), 'L')
        self.assertEqual(1, game.get_captured("Jake"))

    def test_capture_one_right_board(self):
        game = KubaGame(("Jake", 'W'), ("Kenna", 'B'))
        game.make_move("Kenna", (6, 0), 'F')
        game.make_move("Jake", (0, 0), 'R')
        game.make_move("Kenna", (5, 0), 'F')
        game.make_move("Jake", (0, 1), "R")
        game.make_move("Kenna", (3, 0), "R")
        game.make_move("Jake", (0, 2), "R")
        game.make_move("Kenna", (3, 1), "R")
        self.assertEqual(1, game.get_captured("Kenna"))

    def test_capture_one_top_board(self):
        game = KubaGame(("Jake", 'W'), ("Kenna", 'B'))
        game.make_move("Kenna", (6, 0), 'R')
        game.make_move("Jake", (0, 0), 'B')
        game.make_move("Kenna", (6, 1), 'R')
        game.make_move("Jake", (1, 0), 'B')
        game.make_move("Kenna", (6, 3), 'F')
        game.make_move("Jake", (2, 0), 'B')
        game.make_move("Kenna", (5, 3), 'F')
        self.assertEqual(1, game.get_captured("Kenna"))

    def test_ko_rule(self):
        """ Tests if the Ko Rule is violated & handled properly"""
        game = KubaGame(("Jake", 'W'), ("Kenna", 'B'))
        game.make_move("Kenna", (6, 0), 'F')
        game.make_move("Jake", (0, 0), 'B')
        game.make_move("Kenna", (5, 0), 'F')
        game.make_move("Jake", (1, 0), 'B')
        test = game.make_move("Kenna", (5, 0), 'F')
        self.assertEqual(False, test)                   # Tests that the move results in a Ko rule violation & thus False result
        player_remains_up = game.get_current_turn()
        self.assertEqual("Kenna", player_remains_up)    # This test ensures that the player stays up to move after attempting a Ko-Rule violation


if __name__ == '__main__':
    unittest.main()
