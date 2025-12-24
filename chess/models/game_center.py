
from __future__ import annotations

from typing import List
from chess.constants import Colour, GameStatus
from chess.models.board import Board
from chess.models.move import Move
from chess.models.player import Player, PlayerFactory


class Game:
    def __init__(self, player_white: Player, player_black: Player):
        self.board = Board()
        self.player_white = player_white
        self.player_black = player_black

        self._players = [self.player_white, self.player_black]
        self._players_cnt = 2
        self.current_player_idx = 0

        self.moves_log: List[Move] = []
    
    def is_game_over(self):
        return self.board.get_game_status() != GameStatus.IN_PROGRESS and self.board.get_game_status() != GameStatus.IDLE
    

    def initialise(self):
        self.board.initialise()

    def switch_player(self):
        self.current_player_idx = (self.current_player_idx + 1) % self._players_cnt
    
    def display_board(self):
        self.board.display_board(emoji=True)

    
    def _make_move(self, move: Move):
        current_square, target_square = move.get_start_square(), move.get_end_square()

        curr_piece = current_square.get_piece()
        
        if target_square.has_piece():
            target_square.get_piece().kill()
        
        curr_piece.mark_moved()
        current_square.remove_piece()
        target_square.put_piece(curr_piece)
        

    def play(self):
        self.display_board()
        self.board.set_game_status(GameStatus.IN_PROGRESS)

        while not self.is_game_over():
            current_player = self._players[self.current_player_idx]
            move: Move = current_player.calc_next_move(self.board)

            
            self._make_move(move)
            self.moves_log.append(move)
            
            self.display_board()
            
            if self.is_game_over():
                break
            else:
                self.switch_player()
        
        print(f"Game over: {self.board.get_game_status().value}")

        




            
        
        
