




from typing import List

from chess.constants import Colour
from chess.models.cell import Cell
from chess.models.pieces import Rook, Knight, Bishop, Queen, King, Pawn, BlackPawn, WhitePawn




class Board:
    def __init__(self):
        # self.cells = [[Cell() for i in range(8)] for j in range(8,0,-1)]
        self.cells: List[List[Cell]] = [[Cell(row, col) for col in range(8)] for row in range(8)]
    
    def initialise(self):
        for colour, row in [(Colour.BLACK, 0), (Colour.WHITE, 7)]:
            self.cells[row][0].put_piece(Rook(colour))
            self.cells[row][1].put_piece(Knight(colour))
            self.cells[row][2].put_piece(Bishop(colour))
            self.cells[row][3].put_piece(Queen(colour))
            self.cells[row][4].put_piece(King(colour))
            self.cells[row][5].put_piece(Bishop(colour))
            self.cells[row][6].put_piece(Knight(colour))
            self.cells[row][7].put_piece(Rook(colour))
        
        # for colour, row in [(Colour.BLACK, 1), (Colour.WHITE, 6)]:
        #     for col in range(8):
        #         self.cells[row][col].put_piece(Pawn(colour))
        
        for col in range(8):
            self.cells[1][col].put_piece(BlackPawn())
            self.cells[6][col].put_piece(WhitePawn())
        
    def display_board(self):
        for row in self.cells:
            for cell in row:
                print(cell, end=" ") # print all the cells of same row in same line, adds " " instead of newline
            print() # here it adds newline
                


# b = Board()
# b.initialise()
# b.display_board()

