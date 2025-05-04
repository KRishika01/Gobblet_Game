"""
Main entry point for the Gobblet game.
This module initializes and runs the Gobblet game using Pygame
"""

import pygame
import sys
from game_handling import GobbletGame
from game_logic import GobbletGameLogic
from game_dimensions import *

def main() :
    """
    Initialize and run the Gobblet game.
    Sets up the Pygame environment and starts the game loop.
    """
    pygame.init()
    OriginalGame = GobbletGame()
    OriginalGame.run()

if __name__ == "__main__" :
    main()
