"""Module containing game constants and dimensional parameters."""
from enum import Enum

Width = 800
Height = 800
Size_of_Board = 3
Size_of_Cell = 150
Board_X = (Width - Size_of_Board * Size_of_Cell) // 2
Board_Y = 150
Size_of_pieces = [20,30,50]
Num_pieces_per_size = 2

White = (255,255,255)
Black = (0,0,0)
Brown = (139,69,19)
Red = (255,0,0)
Blue = (0,0,255)
Green = (0,128,0)

class Players(Enum) :
    """Enum reprsenting the game players"""
    Red = 1
    Blue = 0
