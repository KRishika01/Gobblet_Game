"""
Game UI module for Gobblet game
Handles rendering and user interaction.
"""

import pygame
import sys
import math
from game_logic import *
from game_dimensions import *
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
        self.display = pygame.display.set_mode((Width,Height))
        pygame.display.set_caption("Gobblet Game")
        self.time = pygame.time.Clock()
        self.game_state = GobbletGameLogic()
        self.font_size = pygame.font.SysFont(None,36)
        self.small_font_size = pygame.font.SysFont(None,24)
    def board_display(self) -> None:
        """
        Draw the game board with grid lines
        """
        for i in range(Size_of_Board+1) :
            pygame.draw.line(self.display, Black, (Board_X+i*Size_of_Cell,Board_Y),
                             (Board_X+i*Size_of_Cell,Board_Y+Size_of_Board*Size_of_Cell),2)
            pygame.draw.line(self.display, Black, (Board_X, Board_Y+i*Size_of_Cell),
                             (Board_X+Size_of_Board*Size_of_Cell, Board_Y+i*Size_of_Cell),2)
    def draw_player_reserves(self) :
        reserve_y = 70
        for size_len in range(len(Size_of_pieces)) :
            for i in range(self.game_state.pieces_of_player[Players.Red][size_len]) :
                reserve_x = Board_X + size_len * 150 + i * 65
                pygame.draw.circle(self.display, Red,(reserve_x, reserve_y),Size_of_pieces[size_len])
                pygame.draw.circle(self.display,Black,(reserve_x,reserve_y),Size_of_pieces[size_len],2)
        reserve_y = Height-70
        for size_len in range(len(Size_of_pieces)) :
            for i in range(self.game_state.pieces_of_player[Players.Blue][size_len]) :
                reserve_x = Board_X + size_len * 150 + i * 65
                pygame.draw.circle(self.display,Blue,(reserve_x,reserve_y),Size_of_pieces[size_len])
                pygame.draw.circle(self.display,Black,(reserve_x,reserve_y),Size_of_pieces[size_len],2)
    def pieces_display(self) :
        for row in range(Size_of_Board) :
            for col in range(Size_of_Board) :
                store = self.game_state.board[row][col]
                if store :
                    size, player = store[-1]
                    if player == Players.Red :
                        color = Red
                    else :
                        color = Blue
                    center_x = Board_X + col * Size_of_Cell + Size_of_Cell // 2
                    center_y = Board_Y + row * Size_of_Cell + Size_of_Cell // 2
                    radius = Size_of_pieces[size]
                    pygame.draw.circle(self.display,color, (center_x,center_y), radius)
                    pygame.draw.circle(self.display, Black, (center_x,center_y), radius, 2)
        self.draw_player_reserves()
        if self.game_state.piece_taken is not None :
            size, player = self.game_state.piece_taken
            color = Blue
            if player == Players.Red :
                color = Red
            else :
                color = Blue
            position = pygame.mouse.get_pos()
            pygame.draw.circle(self.display, color, position, Size_of_pieces[size])
            pygame.draw.circle(self.display, Black, position, Size_of_pieces[size], 2)
    def game_information_display(self) :
        player_data = ""
        if self.game_state.present_player == Players.Red :
            player_data = f"Current Player : RED"
        else :
            player_data = f"Current Player : BLUE"
        player_suf = self.font_size.render(player_data, True, Black)
        self.display.blit(player_suf, (20,10))
        if self.game_state.winner :
            winner_data = ""
            if self.game_state.winner == Players.Red :
                winner_data = f"RED Wins!!"
            else :
                winner_data = f"BLUE Wins!!"
            winner_suf = self.font_size.render(winner_data,True,Green)
            self.display.blit(winner_suf,(Width-200,10))
            restart_data = "Press R to restart"
            restart_suf = self.small_font_size.render(restart_data,True,Black)
            self.display.blit(restart_suf,(Width-200,50))
        else :
            instr = "Click on a piece to select, and click again to place"
            instr_suf = self.small_font_size.render(instr,True,Black)
            self.display.blit(instr_suf,(Width-350,10))
    def reserve_click_check(self,position) :
        if self.game_state.winner :
            return False
        x,y = position
        reserve_y = 70
        if abs(y-reserve_y) <= 30 :
            for size_len in range(len(Size_of_pieces)) :
                for i in range(self.game_state.pieces_of_player[Players.Red][size_len]) :
                    reserve_x = Board_X + size_len * 150 + i * 65
                    dist = math.sqrt((x-reserve_x)**2 + (y-reserve_y)**2)
                    if dist<=Size_of_pieces[size_len] and self.game_state.present_player==Players.Red :
                        self.game_state.piece_taken = (size_len,Players.Red)
                        self.game_state.piece_taken_from = "reserve"
                        self.game_state.pieces_of_player[Players.Red][size_len] -= 1
                        return True
        reserve_y = Height - 70
        if abs(y-reserve_y) <= 30 :
            for size_len in range(len(Size_of_pieces)) :
                for i in range(self.game_state.pieces_of_player[Players.Blue][size_len]) :
                    reserve_x = Board_X + size_len * 150 + i * 65
                    dist = math.sqrt((x-reserve_x)**2 + (y-reserve_y)**2)
                    if dist<=Size_of_pieces[size_len] and self.game_state.present_player==Players.Blue :
                        self.game_state.piece_taken = (size_len,Players.Blue)
                        self.game_state.piece_taken_from = "reserve"
                        self.game_state.pieces_of_player[Players.Blue][size_len] -= 1
                        return True
        return False
    def board_click_check(self,position) :
        x,y = position
        if x < Board_X and x >= Board_X+Size_of_Board*Size_of_Cell :
            return None
        if y < Board_Y and y >= Board_Y+Size_of_Board*Size_of_Cell :
            return None
        row = (y - Board_Y)//Size_of_Cell
        col = (x - Board_X)//Size_of_Cell
        return (row,col)
    def mouse_click_handling(self,position) :
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
                if Event.type == pygame.QUIT :
                    currently_running = False
                elif Event.type == pygame.MOUSEBUTTONDOWN :
                    if Event.button == 1 :
                        self.mouse_click_handling(Event.pos)
                elif Event.type == pygame.KEYDOWN :
                    if Event.key == pygame.K_r :
                        self.game_state = GobbletGameLogic()
            self.display.fill(White)
            self.board_display()
            self.pieces_display()
            self.game_information_display()
            pygame.display.flip()
            self.time.tick(60)
        pygame.quit()
        sys.exit()
