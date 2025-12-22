from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from chess.constants import Colour
from chess.models.move import Move

if TYPE_CHECKING:
    from chess.models.board import Board


class Piece(ABC):

    def __init__(self, colour: Colour):
        self._colour: Colour = colour
        self._is_alive: bool = True
        self._has_moved: bool = False
    
    def is_alive(self) -> bool:
        return self._is_alive
    
    def kill(self) -> None:
        self._is_alive = False

    def has_moved(self) -> bool:
        return self._has_moved
    
    def mark_moved(self) -> None:
        self._has_moved = True
    
    def get_colour(self) -> Colour:
        return self._colour
    

    @abstractmethod
    def can_move(self, move: Move, board: Board):
        pass
    

    @abstractmethod
    def __str__(self, emoji=False):
        pass
    
    


class Pawn(Piece):
    def __init__(self, colour: Colour):
        super().__init__(colour)
    
    
    
    
    



class BlackPawn(Pawn):
    def __init__(self):
        super().__init__(Colour.BLACK)
    
    def __str__(self, emoji=False):
        return "♙" if emoji else "p"
    
    def _is_en_passant(self, move: Move):
        return False
        # TODO: impl

    def _is_promotion(self, move: Move):
        return move.get_end_square().get_row_col()[0] == 7
    

    def can_move(self, move: Move, board: Board):
        if self._is_en_passant(move):
            return True
        else:
            curr_square, target_square = move.get_start_square(), move.get_end_square()
            curr_row, curr_col = curr_square.get_row_col()
            target_row, target_col = target_square.get_row_col()
            if target_square.has_piece():
                if target_square.get_piece().get_colour() == self._colour:
                    print("can't move: target square has same coloured piece")
                    return False
                else:
                    verdict = (target_row - curr_row == 1) and abs(target_col - curr_col) == 1
                    print(f"checking if can kill: {verdict}")        
                    return verdict
            
            else:

                # has_moved = target_row > curr_row
                same_col = target_col == curr_col
                single_step = target_row - curr_row == 1
                double_step = (not self._has_moved) and target_row - curr_row == 2
                
                return same_col and (single_step or double_step)
            

            





class WhitePawn(Pawn):
    def __init__(self):
        super().__init__(Colour.WHITE)
    
    def __str__(self, emoji=False):
        return "♟" if emoji else "P"
    
    def _is_en_passant(self, move: Move):
        return False
        # TODO: impl


    def _is_promotion(self, move: Move):
        return move.get_end_square().get_row_col()[0] == 0
    
    
    def can_move(self, move: Move, board: Board):
        if self._is_en_passant(move):
            return True
        else:
            curr_square, target_square = move.get_start_square(), move.get_end_square()
            curr_row, curr_col = curr_square.get_row_col()
            target_row, target_col = target_square.get_row_col()
            if target_square.has_piece():
                if target_square.get_piece().get_colour() == self._colour:
                    print("can't move: target square has same coloured piece")
                    return False
                else:        
                    verdict = target_row - curr_row == -1 and abs(target_col - curr_col) == 1
                    print(f"checking if can kill: {verdict}")        
                    return verdict
            
            else:
                # has_moved = target_row > curr_row
                same_col = target_col == curr_col
                single_step = target_row - curr_row == -1
                double_step = (not self._has_moved) and target_row - curr_row == -2
                
                return same_col and (single_step or double_step)

    
class Knight(Piece):
    def __init__(self, colour: Colour):
        super().__init__(colour)
    
    def __str__(self, emoji=False):
        if emoji:
            return "♞" if self._colour == Colour.WHITE else "♘"
        else:
            return "N" if self._colour == Colour.WHITE else "n"
    
    def can_move(self, move: Move, board: Board):
        curr_row, curr_col = move.get_start_square().get_row_col()
        target_row, target_col = move.get_end_square().get_row_col()

        row_diff = abs(curr_row - target_row)
        col_diff = abs(curr_col - target_col)

        return row_diff == 2 and col_diff == 1 or row_diff == 1 and col_diff == 2




class Bishop(Piece):
    def __init__(self, colour: Colour):
        super().__init__(colour)

    def __str__(self, emoji=False):
        if emoji:
            return "♝" if self._colour == Colour.WHITE else "♗"
        else:
            return "B" if self._colour == Colour.WHITE else "b"
    
    def can_move(self, move: Move, board: Board):
        curr_row, curr_col = move.get_start_square().get_row_col()
        target_row, target_col = move.get_end_square().get_row_col()

        row_diff = abs(curr_row - target_row)
        col_diff = abs(curr_col - target_col)

        has_moved = (row_diff != 0 or col_diff != 0)
        diagonal_move = row_diff == col_diff

        return has_moved and diagonal_move 


class Rook(Piece):
    def __init__(self, colour: Colour):
        super().__init__(colour)
    
    def __str__(self, emoji=False):
        if emoji:
            return "♜" if self._colour == Colour.WHITE else "♖"
        else:
            return "R" if self._colour == Colour.WHITE else "r"
    
    def can_move(self, move: Move, board: Board):
        curr_row, curr_col = move.get_start_square().get_row_col()
        target_row, target_col = move.get_end_square().get_row_col()

        row_diff = abs(curr_row - target_row)
        col_diff = abs(curr_col - target_col)

        has_moved = (row_diff != 0 or col_diff != 0)
        straight_move = row_diff == 0 or col_diff == 0

        return has_moved and straight_move




class Queen(Piece):
    def __init__(self, colour: Colour):
        super().__init__(colour)
    
    def __str__(self, emoji=False):
        if emoji:
            return "♛" if self._colour == Colour.WHITE else "♕"
        else:
            return "Q" if self._colour == Colour.WHITE else "q"
    
    def can_move(self, move: Move, board: Board):
        curr_row, curr_col = move.get_start_square().get_row_col()
        target_row, target_col = move.get_end_square().get_row_col()

        row_diff = abs(curr_row - target_row)
        col_diff = abs(curr_col - target_col)

        has_moved = (row_diff != 0 or col_diff != 0)
        diagonal_move = row_diff == col_diff
        straight_move = row_diff == 0 or col_diff == 0

        return has_moved and (diagonal_move or straight_move)




class King(Piece):
    def __init__(self, colour: Colour):
        super().__init__(colour)
    
    def __str__(self, emoji=False):
        if emoji:
            return "♚" if self._colour == Colour.WHITE else "♔"
        else:
            return "K" if self._colour == Colour.WHITE else "k"
    
    def _is_castling_move(self, move: Move) -> bool:
        return False 
        # TODO: impl 
    
    def can_move(self, move: Move, board: Board):
        if self._is_castling_move(move):
            return True
        else:
            curr_row, curr_col = move.get_start_square().get_row_col()
            target_row, target_col = move.get_end_square().get_row_col()

            row_diff = abs(curr_row - target_row)
            col_diff = abs(curr_col - target_col)

            has_moved = (row_diff != 0 or col_diff != 0)
            diagonal_step = row_diff == 1 and col_diff == 1
            straight_step = row_diff + col_diff == 1

            return has_moved and (diagonal_step or straight_step)






