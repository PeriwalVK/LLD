from enum import Enum
from re import X


class Symbol(Enum):
    X = "X"
    O = "O"
    EMPTY = " "

class GameState(Enum):
    IN_PROGRESS = "Game is in Progress"
    DRAW = "Game is drawn"
    X_WON = "Player X won"
    O_WON = "Player O won"