"""
Game UI module for Gobblet game
Handles rendering and user interaction.
"""

import pygame
import sys
import math
from game_logic_1 import *
from game_dimensions_1 import *
from typing import Optional,Tuple

class GobbletGame :
    """
    Main UI calss for Gobblet game

    Attributes:
        display (pygame.Surface): Main game window
        time (pygame.time.Clock): Game clock for controllng frame rate
        game_state (GobbletGameLogic): Current game state
        font_size (pygame.font.Font): Main font for rendering the text
        small_font_size (pygame.font.Font): Smaller font for rendering the text
    """
    def __init__(self) :
        """
        Initialize the game window, clock and the fonts.
        """
        pygame.init() # pylint: disable=no-member
        self.display = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption("Gobblet Game")
        self.time = pygame.time.Clock()
        self.game_state = GobbletGameLogic()
        self.font_size = pygame.font.SysFont(None,36)
        self.small_font_size = pygame.font.SysFont(None,24)
    def board_display(self) -> None:
        """
        Draw the game board with grid lines
        """
        for i in range(SIZE_BOARD+1) :
            pygame.draw.line(self.display, BLACK, (BOARD_X+i*SIZE_CELL,BOARD_Y),
                             (BOARD_X+i*SIZE_CELL,BOARD_Y+SIZE_BOARD*SIZE_CELL),2)
            pygame.draw.line(self.display, BLACK, (BOARD_X, BOARD_Y+i*SIZE_CELL),
                             (BOARD_X+SIZE_BOARD*SIZE_CELL, BOARD_Y+i*SIZE_CELL),2)
    def draw_player_reserves(self) :
        """
        Draw the player's reserve pieces on the screen
        """
        reserve_y = 70
        for size_len in range(len(SIZE_PIECES)) :
            for i in range(self.game_state.pieces_of_player[Players.RED][size_len]) :
                reserve_x = BOARD_X + size_len * 150 + i * 65
                pygame.draw.circle(self.display, RED,(reserve_x, reserve_y),SIZE_PIECES[size_len])
                pygame.draw.circle(self.display,BLACK,(reserve_x,reserve_y),SIZE_PIECES[size_len],2)
        reserve_y = HEIGHT-70
        for size_len in range(len(SIZE_PIECES)) :
            for i in range(self.game_state.pieces_of_player[Players.BLUE][size_len]) :
                reserve_x = BOARD_X + size_len * 150 + i * 65
                pygame.draw.circle(self.display,BLUE,(reserve_x,reserve_y),SIZE_PIECES[size_len])
                pygame.draw.circle(self.display,BLACK,(reserve_x,reserve_y),SIZE_PIECES[size_len],2)
    def pieces_display(self) :
        """
        Display the pieces on the game board
        """
        for row in range(SIZE_BOARD) :
            for col in range(SIZE_BOARD) :
                store = self.game_state.board[row][col]
                if store :
                    size, player = store[-1]
                    if player == Players.RED :
                        color = RED
                    else :
                        color = BLUE
                    center_x = BOARD_X + col * SIZE_CELL + SIZE_CELL // 2
                    center_y = BOARD_Y + row * SIZE_CELL + SIZE_CELL // 2
                    radius = SIZE_PIECES[size]
                    pygame.draw.circle(self.display,color, (center_x,center_y), radius)
                    pygame.draw.circle(self.display, BLACK, (center_x,center_y), radius, 2)
        self.draw_player_reserves()
        if self.game_state.piece_taken is not None :
            size, player = self.game_state.piece_taken
            color = BLUE
            if player == Players.RED :
                color = RED
            else :
                color = BLUE
            position = pygame.mouse.get_pos()
            pygame.draw.circle(self.display, color, position, SIZE_PIECES[size])
            pygame.draw.circle(self.display, BLACK, position, SIZE_PIECES[size], 2)
    def game_information_display(self) :
        """
        Display game information like current player and winner
        """
        player_data = ""
        if self.game_state.present_player == Players.RED :
            player_data = f"Current Player : RED"
        else :
            player_data = f"Current Player : BLUE"
        player_suf = self.font_size.render(player_data, True, BLACK)
        self.display.blit(player_suf, (20,10))
        if self.game_state.winner :
            winner_data = ""
            if self.game_state.winner == Players.RED :
                winner_data = f"RED Wins!!"
            else :
                winner_data = f"BLUE Wins!!"
            winner_suf = self.font_size.render(winner_data,True,GREEN)
            self.display.blit(winner_suf,(WIDTH-200,10))
            restart_data = "Press R to restart"
            restart_suf = self.small_font_size.render(restart_data,True,BLACK)
            self.display.blit(restart_suf,(WIDTH-200,50))
        else :
            instr = "Click on a piece to select, and click again to place"
            instr_suf = self.small_font_size.render(instr,True,BLACK)
            self.display.blit(instr_suf,(WIDTH-350,10))
    def reserve_click_check(self,position) :
        """
        Check if a reserve piece was clicked
        
        Args:
            position: Mouse click position (x, y)
            
        Returns:
            bool: True if a reserve piece was selected, False otherwise
        """

        if self.game_state.winner :
            return False
        x,y = position
        reserve_y = 70
        if abs(y-reserve_y) <= 30 :
            for size_len in range(len(SIZE_PIECES)) :
                for i in range(self.game_state.pieces_of_player[Players.RED][size_len]) :
                    reserve_x = BOARD_X + size_len * 150 + i * 65
                    dist = math.sqrt((x-reserve_x)**2 + (y-reserve_y)**2)
                    if dist<=SIZE_PIECES[size_len] and self.game_state.present_player==Players.RED :
                        self.game_state.piece_taken = (size_len,Players.RED)
                        self.game_state.piece_taken_from = "reserve"
                        self.game_state.pieces_of_player[Players.RED][size_len] -= 1
                        return True
        reserve_y = HEIGHT - 70
        if abs(y-reserve_y) <= 30 :
            for size_len in range(len(SIZE_PIECES)) :
                for i in range(self.game_state.pieces_of_player[Players.BLUE][size_len]) :
                    reserve_x = BOARD_X + size_len * 150 + i * 65
                    dist = math.sqrt((x-reserve_x)**2 + (y-reserve_y)**2)
                    if dist<=SIZE_PIECES[size_len] and self.game_state.present_player==Players.BLUE :
                        self.game_state.piece_taken = (size_len,Players.BLUE)
                        self.game_state.piece_taken_from = "reserve"
                        self.game_state.pieces_of_player[Players.BLUE][size_len] -= 1
                        return True
        return False
    def board_click_check(self,position) :
        """
        Check if a board cell was clicked
        
        Args:
            position: Mouse click position (x, y)
            
        Returns:
            tuple or None: (row, col) of clicked cell or None if click was outside the board
        """
        x,y = position
        if x < BOARD_X and x >= BOARD_X+SIZE_BOARD*SIZE_CELL :
            return None
        if y < BOARD_Y and y >= BOARD_Y+SIZE_BOARD*SIZE_CELL :
            return None
        row = (y - BOARD_Y)//SIZE_CELL
        col = (x - BOARD_X)//SIZE_CELL
        return (row,col)
    def mouse_click_handling(self,position) :
        # x,y = position
        """
        Handle mouse clicks for piece selection and placement
        
        Args:
            position: Mouse click position (x, y)
        """
        if self.game_state.winner :
            return
        if not self.game_state.piece_taken and self.reserve_click_check(position) :
            return
        board_position = self.board_click_check(position)
        if board_position :
            row, col = board_position
            if self.game_state.piece_taken :
                size, player = self.game_state.piece_taken
                if self.game_state.able_to_place_piece(row,col,size) :
                    self.game_state.place_piece(row,col,size)
                    self.game_state.piece_taken = None
                    if self.game_state.conditions_win() :
                        print(f"Player {self.game_state.winner.name} wins!!")
                    else :
                        self.game_state.change_turn_of_player()
                else :
                    if self.game_state.piece_taken_from == "reserve" :
                        size, player = self.game_state.piece_taken
                        self.game_state.pieces_of_player[player][size] += 1
                    elif self.game_state.piece_taken_from :
                        prev_row, prev_col = self.game_state.piece_taken_from
                        self.game_state.board[prev_row][prev_col].append(self.game_state.piece_taken)
                    self.game_state.piece_taken = None
                    self.game_state.piece_taken_from = None
            else :
                top_piece = self.game_state.top_piece_present(row,col)
                if top_piece and top_piece[1] == self.game_state.present_player :
                    self.game_state.piece_taken = self.game_state.remove_piece(row,col)
                    self.game_state.piece_taken_from = (row,col)
    def run(self) :
        """Main game loop"""
        currently_running = True
        while currently_running :
            for Event in pygame.event.get() :
                if Event.type == pygame.QUIT :  # pylint: disable=no-member
                    currently_running = False
                elif Event.type == pygame.MOUSEBUTTONDOWN :  # pylint: disable=no-member
                    if Event.button == 1 :
                        self.mouse_click_handling(Event.pos)
                elif Event.type == pygame.KEYDOWN :  # pylint: disable=no-member
                    if Event.key == pygame.K_r :  # pylint: disable=no-member
                        self.game_state = GobbletGameLogic()
            self.display.fill(WHITE)
            self.board_display()
            self.pieces_display()
            self.game_information_display()
            pygame.display.flip()
            self.time.tick(60)
        pygame.quit()  # pylint: disable=no-member
        sys.exit()
