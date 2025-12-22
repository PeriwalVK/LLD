from __future__ import annotations


from typing import Tuple
from chess.models.pieces import Piece
from chess.utils import SquareUtil


class Square:
    def __init__(self, x:int, y:int, piece: Piece = None):
        self.row = x
        self.col = y

        self.square = SquareUtil.position_to_square_name(self.row, self.col)

        self.piece: Piece = piece

    def get_square(self) -> str:
        return self.square
    
    def get_row_col(self) -> Tuple[int,int]:
        return self.row, self.col
    
    def has_piece(self) -> bool:
        return self.piece and self.piece.is_alive()

    def get_piece(self) -> Piece:
        return self.piece

    def put_piece(self, piece: Piece) -> None:
        self.piece = piece
    
    def remove_piece(self) -> None:
        self.piece = None
    
    def __str__(self, emoji=False) -> str:
        return self.get_piece().__str__(emoji=emoji) if self.has_piece() else "."