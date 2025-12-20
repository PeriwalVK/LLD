from typing import List

from Tic_Tac_Toe.models.position import Position
from Tic_Tac_Toe.constants import GameState, Symbol


class Board:
    def __init__(self, size=3):
        self.size = size
        self.cells: List[List[Symbol]] = [[Symbol.EMPTY for _ in range(size)] for _ in range(size)]
        self.game_state: GameState = GameState.IN_PROGRESS


    def print_board(self):
        for row in self.cells:
            print(' | '.join([cell.value for cell in row]))
            print('-' * (self.size * 3 + 1))
    
    def is_valid_move(self, position: Position) -> bool:
        return position.row >= 0 and position.row < self.size and position.col >= 0 and position.col < self.size and self.cells[position.row][position.col] == Symbol.EMPTY

    def make_move(self, position: Position, symbol:Symbol):
        self.cells[position.row][position.col] = symbol
    
    def _is_winning_line(self, curr_symbol:Symbol, line: List[Symbol]) -> bool:
        for symbol in line:
            if symbol != curr_symbol or symbol == Symbol.EMPTY:
                return False
        return True
    
    def _check_win(self, symbol: Symbol) -> bool:
        
        for i in range(self.size):
            if self._is_winning_line(symbol, [self.cells[i][j] for j in range(self.size)]):
                return True
            if self._is_winning_line(symbol, [self.cells[j][i] for j in range(self.size)]):
                return True
        
        if self._is_winning_line(symbol, [self.cells[i][i] for i in range(self.size)]):
            return True
        if self._is_winning_line(symbol, [self.cells[i][self.size-1-i] for i in range(self.size)]):
            return True
    
    def _check_draw(self) -> bool:
        for row in self.cells:
            for cell in row:
                if cell == Symbol.EMPTY:
                    return False
        return True
    
    def update_game_state(self) -> GameState:
        if self._check_win(Symbol.X):
            self.game_state = GameState.X_WON
        elif self._check_win(Symbol.O):
            self.game_state = GameState.O_WON
        elif self._check_draw():
            self.game_state = GameState.DRAW
        else:
            self.game_state = GameState.IN_PROGRESS
        
        return self.game_state


            

        
