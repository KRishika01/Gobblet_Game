"""Module containing game constants and dimensional parameters."""
from enum import Enum

WIDTH = 800
HEIGHT = 800
SIZE_BOARD = 3
SIZE_CELL = 150
BOARD_X = (WIDTH - SIZE_BOARD * SIZE_CELL) // 2
BOARD_Y = 150
SIZE_PIECES = [20,30,50]
NUM_PIECES_SIZE = 2

WHITE = (255,255,255)
BLACK = (0,0,0)
BROWN = (139,69,19)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,128,0)

class Players(Enum) :
    """Enum reprsenting the game players"""
    RED = 1
    BLUE = 0
