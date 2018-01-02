"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

import unittest

import isolation
import game_agent

from importlib import reload


class IsolationTest(unittest.TestCase):
    """Unit tests for isolation agents"""

    def setUp(self):
        reload(game_agent)
        self.player1 = "Player1"
        self.player2 = "Player2"
        self.game = isolation.Board(self.player1, self.player2)

    # def test_example(self):
    #     # TODO: All methods must start with "test_"

    def test_terminal_test(self):
        # Set for testing purposes
        self.time_left = lambda : 10.0
        self.TIMER_THRESHOLD = 10.0

        # Returns true if depth = 0
        self.assertTrue(game_agent.MinimaxPlayer.terminal_test(self, self.game, 0))


if __name__ == '__main__':
    unittest.main()
