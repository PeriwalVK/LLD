from chess.constants import Colour
from models.board import Board
from models.player import Player


class Game:
    def __init__(self):
        self.board = Board()
        self.player_white = Player("player_white", Colour.WHITE)
        self.player_black = Player("player_black", Colour.BLACK)
        self.white_turn = True

    def initialise(self):
        self.board.initialise()

    def start(self):
        x=1
        
