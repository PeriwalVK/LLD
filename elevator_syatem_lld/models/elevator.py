from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from elevator_syatem_lld.constants import Direction, ElevatorState


@dataclass
class Elevator:
    elevator_id: int
    current_floor: int = 0
    direction: Direction = Direction.IDLE
    state: ElevatorState = ElevatorState.IDLE
    pending_stops: List[int] = field(default_factory=list)

    def add_stop(self, floor: int) -> None:
        if floor not in self.pending_stops:
            self.pending_stops.append(floor)
        self._sort_stops()
        if self.current_floor != floor:
            self.state = ElevatorState.MOVING

    def step(self) -> None:
        """Moves one floor toward the next stop and consumes it on arrival."""
        if self.state == ElevatorState.OUT_OF_SERVICE:
            return
        if not self.pending_stops:
            self.direction = Direction.IDLE
            self.state = ElevatorState.IDLE
            return

        next_stop = self.pending_stops[0]
        if next_stop > self.current_floor:
            self.direction = Direction.UP
            self.current_floor += 1
            self.state = ElevatorState.MOVING
        elif next_stop < self.current_floor:
            self.direction = Direction.DOWN
            self.current_floor -= 1
            self.state = ElevatorState.MOVING
        else:
            self.pending_stops.pop(0)
            if not self.pending_stops:
                self.direction = Direction.IDLE
                self.state = ElevatorState.IDLE

    def is_idle(self) -> bool:
        return self.state == ElevatorState.IDLE and not self.pending_stops

    def _sort_stops(self) -> None:
        # Direction-aware ordering keeps movement natural and simple.
        if self.direction == Direction.DOWN:
            self.pending_stops.sort(reverse=True)
        else:
            self.pending_stops.sort()

