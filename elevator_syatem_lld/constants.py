from enum import Enum, auto


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    IDLE = auto()


class ElevatorState(Enum):
    MOVING = auto()
    IDLE = auto()
    OUT_OF_SERVICE = auto()

