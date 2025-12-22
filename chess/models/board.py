
from __future__ import annotations


from typing import List
from multipledispatch import dispatch

from chess.constants import Colour, GameStatus
from chess.models import square
from chess.models.move import Move
from chess.models.square import Square
from chess.models.pieces import Rook, Knight, Bishop, Queen, King, BlackPawn, WhitePawn



class Board:
    def __init__(self):
        self.squares: List[List[Square]] = [[Square(row, col) for col in range(8)] for row in range(8)]
        self.game_status: GameStatus = GameStatus.IDLE

    def get_game_status(self):
        return self.game_status
    
    def set_game_status(self, game_status: GameStatus):
        self.game_status = game_status
    
    def initialise(self):
        for colour, row in [(Colour.BLACK, 0), (Colour.WHITE, 7)]:
            self.squares[row][0].put_piece(Rook(colour))
            self.squares[row][1].put_piece(Knight(colour))
            self.squares[row][2].put_piece(Bishop(colour))
            self.squares[row][3].put_piece(Queen(colour))
            self.squares[row][4].put_piece(King(colour))
            self.squares[row][5].put_piece(Bishop(colour))
            self.squares[row][6].put_piece(Knight(colour))
            self.squares[row][7].put_piece(Rook(colour))
        
        
        for col in range(8):
            self.squares[1][col].put_piece(BlackPawn())
            self.squares[6][col].put_piece(WhitePawn())
        
    def display_board(self, emoji=False):

        print("   " + "____" * 8 )

        for row in range(8):
            print(" | ".join([str(8-row)]+[cell.__str__(emoji=emoji) for cell in self.squares[row]] + [""]))
            print("  |" + "___|"*8)
        
        print("   ".join([" ", "a", "b", "c", "d", "e", "f", "g", "h", ""]))
    
    @dispatch(int, int)
    def get_square_at(self, row: int, col: int):
        return self.squares[row][col]
    
    @dispatch(str)
    def get_square_at(self, square_name: str):
        row, col = square.SquareUtil.square_name_to_position(square_name)
        return self.squares[row][col]
    
    def is_valid_move(self, move: Move, colour: Colour):
        start_square, end_square = move.get_start_square(), move.get_end_square()

        if not start_square.has_piece():
            print("Invalid move: starting square is empty")
            return False
        
        start_piece = start_square.get_piece()
        
        if start_piece.get_colour() != colour:
            print(f"Invalid move: starting square doesn't have a {colour.value} piece")
            return False
        
        if end_square.has_piece() and end_square.get_piece().get_colour() == colour:
            print(f"Invalid move: ending square has a {colour.value} piece")
            return False
        
        return start_piece.can_move(move=move, board=self)
        

        
    
    
        






# b = Board()
# b.initialise()
# b.display_board()

