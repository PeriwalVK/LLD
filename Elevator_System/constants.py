from enum import Enum


class ElevatorDirection(Enum):
    UP = "UP"
    DOWN = "DOWN"
    IDLE = "IDLE" # IDLE state

class ElevatorStatus(Enum):
    IDLE = "IDLE" # waiting for request
    MOVING = "MOVING" # moving
    STOPPED = "STOPPED" # stopped temporary
    MAINTAINANCE = "MAINTAINANCE" # under maintainance

class DoorStatus(Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"


class BuildingConstants:
    MAX_FLOOR = 10
    MIN_FLOOR = -2
    ELEVATORS_COUNT = 3
