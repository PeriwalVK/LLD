from enum import Enum


class Symbol(Enum):
    HARD_WALL = "#"
    TRANSPARENT_WALL = "o"
    EMPTY = " "
    
    FOOD = "+"

    SNAKE_HEAD = "@"
    SNAKE_BODY = "*"
    
class Direction(Enum):
    UP = "W"
    DOWN = "S"
    LEFT = "A"
    RIGHT = "D"

class GameStatus(Enum):
    IDLE = "IDLE"
    IN_PROGRESS = "IN_PROGRESS"
    GAME_OVER = "GAME_OVER"