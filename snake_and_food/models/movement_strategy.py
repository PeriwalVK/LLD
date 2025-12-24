from abc import ABC


class MovementStrategy(ABC):
    def __init__(self, board: Board):
        self.board = board