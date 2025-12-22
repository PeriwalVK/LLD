from abc import ABC

from Tic_Tac_Toe.models.board import Board
from Tic_Tac_Toe.models.player import HumanPlayerStrategy, Player
from Tic_Tac_Toe.constants import GameState, Symbol


class BoardGame(ABC):
    def play(self):
        pass
    
    def switch_player(self):
        pass

    def show_result(self):
        pass

class TicTacToeGame(BoardGame):
    def __init__(self, board_size=3):
        self.player_cnt = 2
        self.board = Board(board_size)
        self.players = [
            Player(Symbol.X, HumanPlayerStrategy()), 
            Player(Symbol.O, HumanPlayerStrategy())
        ]

        self.current_player_idx = 0
        self.game_state = GameState.IN_PROGRESS
        self.winner_idx: int = -1

    def play(self):
        print("Tic-Tac-Toe Game Started!")
        self.board.print_board()
        while self.game_state == GameState.IN_PROGRESS:
            print(f"Player {self.players[self.current_player_idx].symbol.value}'s turn")

            self.players[self.current_player_idx].make_move(self.board)

            self.game_state = self.board.update_game_state()
            
            if self.game_state == GameState.IN_PROGRESS:
                self.switch_player()
            
            self.board.print_board()
            

        self.show_result()
    
    def switch_player(self):
        self.current_player_idx = (self.current_player_idx + 1) % self.player_cnt

    def show_result(self):
        print(self.game_state.value)
    

    
