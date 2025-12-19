from constants import Colour
from abc import ABC, abstractmethod
# from cell import Cell


class Piece(ABC):

    def __init__(self, colour: Colour):
        self.colour = colour

    @abstractmethod
    def __str__(self):
        pass
    
    


class Pawn(Piece):
    def __init__(self, colour: Colour):
        super().__init__(colour)
        self.alive = True
        self.has_moved = False



class BlackPawn(Pawn):
    def __init__(self):
        super().__init__(Colour.BLACK)
    
    def __str__(self):
        return "p"


class WhitePawn(Pawn):
    def __init__(self):
        super().__init__(Colour.WHITE)
    
    def __str__(self):
        return "P"

    
class Knight(Piece):
    def __init__(self, colour: Colour):
        super().__init__(colour)
        self.alive = True
    
    def __str__(self):
        return "N" if self.colour == Colour.WHITE else "n"



class Bishop(Piece):
    def __init__(self, colour: Colour):
        super().__init__(colour)
        self.alive = True

    def __str__(self):
        return "B" if self.colour == Colour.WHITE else "b"


class Rook(Piece):
    def __init__(self, colour: Colour):
        super().__init__(colour)
        self.alive = True
        self.has_moved = False
    
    def __str__(self):
        return "R" if self.colour == Colour.WHITE else "r"



class Queen(Piece):
    def __init__(self, colour: Colour):
        super().__init__(colour)
        self.alive = True
    
    def __str__(self):
        return "Q" if self.colour == Colour.WHITE else "q"



class King(Piece):
    def __init__(self, colour: Colour):
        super().__init__(colour)
        self.alive = True
        self.has_moved = False
    
    def __str__(self):
        return "K" if self.colour == Colour.WHITE else "k"





