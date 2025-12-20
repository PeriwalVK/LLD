from abc import ABC, abstractmethod
from typing import override
from Tic_Tac_Toe.models.board import Board
from Tic_Tac_Toe.constants import Symbol
from Tic_Tac_Toe.models.position import Position

class IPlayerStrategy(ABC):
    @abstractmethod
    def make_move(self, board: Board, symbol: Symbol):
        pass

class HumanPlayerStrategy(IPlayerStrategy):
    @override
    def make_move(self, board: Board, symbol: Symbol):

        row, col = map(int, input("Enter row and col (separated by space): ").split())
        position = Position(row-1, col-1)
        while not board.is_valid_move(position):
            print("Invalid move. Try again.")
            row, col = map(int, input("Enter row and col (separated by space): ").split())
            position = Position(row-1, col-1)
        
        board.make_move(position, symbol)
        

class Player:
    def __init__(self, symbol: Symbol, strategy: IPlayerStrategy):
        # self.name = name
        self.symbol: Symbol = symbol
        self.strategy: IPlayerStrategy = strategy
    
    def make_move(self, board: Board):
        self.strategy.make_move(board, self.symbol)