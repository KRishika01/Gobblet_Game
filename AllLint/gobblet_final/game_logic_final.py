"""
Game State or Game logic module for Gobblet game.
Manages game board, player turns, and win conditions.
"""
from typing import List, Tuple, Optional
from game_dimensions_final import SIZE_BOARD,SIZE_PIECES,NUM_PIECES_SIZE, Players

class GobbletGameLogic :
    """
    Manages the game state or the game logic for the Gobblet game.

    Attributes :
        board (List[List[List[Tuple[int, Players]]]]): 3D board representing pieces stacks
        present_player (Players): Present player's turn
        piece_taken (Optional[Tuple[int, Players]]): Currently selected piece
        piece_taken_from (Optional[Tuple[int, int] or str]): Origin of selected piece
        winner (Optiona[Players]): Winning player, if any
    """
    def __init__(self):
        # Initialize the board as a 3x3 grid of stacks
        self.board = [[[] for _ in range(SIZE_BOARD)] for _ in range(SIZE_BOARD)]
        self.present_player = Players.RED
        self.piece_taken = None
        self.piece_taken_from = None
        self.winner = None
        # Initialize player pieces (off-board pieces)
        self.pieces_of_player = {
            Players.RED: {size: NUM_PIECES_SIZE for size in range(len(SIZE_PIECES))},
            Players.BLUE: {size: NUM_PIECES_SIZE for size in range(len(SIZE_PIECES))}
        }
    def change_turn_of_player(self) -> None:
        """Switch turn between the players."""
        if self.present_player == Players.RED :
            self.present_player = Players.BLUE
        else :
            self.present_player = Players.RED
    def top_piece_present(self,row: int,col: int) :
        """
        Get the top piece from a specific board location.

        Args:
            row (int): Row index
            col (int): Column index
        
        Returns:
            Optional piece tuple or None
        """
        if 0 <= row < SIZE_BOARD and 0 <= col < SIZE_BOARD and self.board[row][col] :
            return self.board[row][col][-1]
        return None
    def able_to_place_piece(self,row: int,col: int,size: int) -> bool:
        """
        Check if a piece can be placed at a specified location.

        Args: 
            row (int): Destination row
            col (int): Destination column
            size (int): Size of the piece

        Returns:
            bool: Whether piece placement is valid or not
        """
        if not (0 <= row < SIZE_BOARD and 0 <= col < SIZE_BOARD) :
            return False
        top_piece = self.top_piece_present(row,col)
        if top_piece is not None :
            size_of_top_piece,piece = top_piece
            if size_of_top_piece >= size :
                return False
        return True
    def place_piece(self,row:int,col: int,size: int) -> bool:
        """
        Place a piece on the board.

        Args :
            row (int): Destination row.
            col (int): Destination column.
            size (int): Size of the piece

        Returns:
            bool: Whether piece was successfully placed or not.
        """
        if self.able_to_place_piece(row,col,size) :
            self.board[row][col].append((size, self.present_player))
            return True
        return False
    def remove_piece(self,row,col) -> Optional[Tuple[int, Players]]:
        """
        Removes amd return the top piece from a board location,

        Args: 
            row (int): Source row.
            col (int): Source column

        Returns :
            Optional piece tuple 
        """
        if 0 <= row < SIZE_BOARD and 0 <= col < SIZE_BOARD and self.board[row][col] :
            removed_piece = self.board[row][col].pop()
            return removed_piece
        return None
    def line_match_check(self,pieces: List[Optional[Tuple[int, Players]]]) -> bool :
        """
        Check if a line of pieces constitutes a win.

        Args:
            pieces (List): Line of pieces to check

        Returns: 
            bool: Whether the line is a winning line or not
        """
        if None in pieces :
            return False
        initial_player = None
        if pieces[0]:
            initial_player = pieces[0][1]
        else :
            initial_player = None
        if not initial_player :
            return False
        for piece in pieces :
            if not piece :
                return False
            if piece[1] != initial_player :
                return False
        self.winner = initial_player
        return True
    def conditions_win(self) -> bool:
        """
        Check if current move results in a win

        Returns :
            bool: Whether a winning condition is met or not
        """
        for row in range(SIZE_BOARD) :
            line = []
            for col in range(SIZE_BOARD) :
                line.append(self.top_piece_present(row,col))
            if self.line_match_check(line) :
                return True
        for col in range(SIZE_BOARD) :
            line = []
            for row in range(SIZE_BOARD) :
                line.append(self.top_piece_present(row,col))
            if self.line_match_check(line) :
                return True
        diagonal_val_1 = []
        diagonal_val_2 = []
        for i in range(SIZE_BOARD) :
            diagonal_val_1.append(self.top_piece_present(i,i))
        if self.line_match_check(diagonal_val_1) :
            return True
        for i in range(SIZE_BOARD) :
            diagonal_val_2.append(self.top_piece_present(i,SIZE_BOARD-i-1))
        if self.line_match_check(diagonal_val_2) :
            return True
        return False
