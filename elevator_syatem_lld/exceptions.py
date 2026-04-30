class ElevatorSystemError(Exception):
    """Base exception for elevator_syatem_lld."""


class InvalidFloorError(ElevatorSystemError):
    pass


class ElevatorUnavailableError(ElevatorSystemError):
    pass

