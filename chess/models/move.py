from __future__ import annotations
from typing import TYPE_CHECKING

from chess.constants import Colour

if TYPE_CHECKING:
    from chess.models.square import Square
    from chess.models.board import Board


class Move:
    def __init__(self, start: Square, end: Square):
        self.start: Square = start
        self.end: Square = end
    
    def get_start_square(self) -> Square:
        return self.start
    
    def get_end_square(self):
        return self.end
    
    def is_valid_move(self, board: Board, colour: Colour):
        if not self.start.has_piece():
            print("Invalid move: starting square is empty")
            return False
        
        start_piece = self.start.get_piece()
        
        if start_piece.get_colour() != colour:
            print(f"Invalid move: starting square doesn't have a {colour.value} piece")
            return False
        
        if self.end.has_piece() and self.end.get_piece().get_colour() == colour:
            print(f"Invalid move: ending square has a {colour.value} piece")
            return False
        
        return start_piece.can_move(move=self, board=board)
        

        

        