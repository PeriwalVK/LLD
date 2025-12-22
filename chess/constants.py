"""Module providing constants"""


from enum import Enum


class Colour(Enum):
    WHITE = "WHITE"
    BLACK = "BLACK"

class GameStatus(Enum):
    IDLE = "IDLE"
    IN_PROGRESS = "IN_PROGRESS"

    WHITE_WON = "WHITE_WON"
    BLACK_WON = "BLACK_WON"

    STALEMATE = "STALEMATE"
    DRAW = "DRAW"