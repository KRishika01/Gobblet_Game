"""
Main entry point for the Gobblet game.
This module initializes and runs the Gobblet game using Pygame
"""

import pygame
# import sys
from game_handling_2 import GobbletGame
# from game_logic_1 import GobbletGameLogic
# from game_dimensions_1 import *

def main() :
    """
    Initialize and run the Gobblet game.
    Sets up the Pygame environment and starts the game loop.
    """
    pygame.init()  # pylint: disable=no-member
    original_game = GobbletGame()
    original_game.run()

if __name__ == "__main__" :
    main()
