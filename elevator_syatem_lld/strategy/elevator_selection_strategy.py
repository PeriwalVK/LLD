from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable

from elevator_syatem_lld.constants import ElevatorState
from elevator_syatem_lld.models.elevator import Elevator
from elevator_syatem_lld.models.request import HallRequest


class ElevatorSelectionStrategy(ABC):
    @abstractmethod
    def select(self, elevators: Iterable[Elevator], request: HallRequest) -> Elevator:
        pass


class NearestCarStrategy(ElevatorSelectionStrategy):
    """
    Picks nearest non-out-of-service car.
    Idle cars are slightly preferred in tie-break.
    """

    def select(self, elevators: Iterable[Elevator], request: HallRequest) -> Elevator:
        available = [e for e in elevators if e.state != ElevatorState.OUT_OF_SERVICE]
        if not available:
            raise ValueError("No available elevators")

        def score(e: Elevator) -> tuple[int, int]:
            distance = abs(e.current_floor - request.source_floor)
            busy_penalty = 0 if e.is_idle() else 1
            return (distance, busy_penalty)

        return min(available, key=score)

