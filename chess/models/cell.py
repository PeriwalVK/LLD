
from chess.models.pieces import Piece


class Cell:
    def __init__(self, x:int, y:int, piece: Piece = None):
        self.x = x
        self.y = y
        self.piece = piece
    
    def get_piece(self):
        return self.piece

    def put_piece(self, piece: Piece):
        self.piece = piece
    
    def remove_piece(self):
        self.piece = None
    
    def __str__(self):
        return str(self.piece) if self.piece else "."