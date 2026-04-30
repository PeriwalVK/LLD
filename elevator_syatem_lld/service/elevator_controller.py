from __future__ import annotations

from elevator_syatem_lld.models.building import Building
from elevator_syatem_lld.models.elevator import Elevator
from elevator_syatem_lld.models.request import CarRequest, HallRequest
from elevator_syatem_lld.strategy.elevator_selection_strategy import ElevatorSelectionStrategy


class ElevatorController:
    def __init__(self, building: Building, selection_strategy: ElevatorSelectionStrategy):
        self._building = building
        self._selection_strategy = selection_strategy

    def request_elevator(self, request: HallRequest) -> Elevator:
        self._building.validate_floor(request.source_floor)
        elevator = self._selection_strategy.select(self._building.elevators, request)
        elevator.add_stop(request.source_floor)
        return elevator

    def select_floor(self, request: CarRequest) -> Elevator:
        self._building.validate_floor(request.destination_floor)
        elevator = self._get_elevator(request.elevator_id)
        elevator.add_stop(request.destination_floor)
        return elevator

    def tick(self) -> None:
        """Simulates one time step for all elevators."""
        for elevator in self._building.elevators:
            elevator.step()

    def snapshot(self) -> list[str]:
        rows: list[str] = []
        for e in self._building.elevators:
            rows.append(
                f"Elevator#{e.elevator_id} floor={e.current_floor} "
                f"dir={e.direction.name} state={e.state.name} stops={e.pending_stops}"
            )
        return rows

    def _get_elevator(self, elevator_id: int) -> Elevator:
        for e in self._building.elevators:
            if e.elevator_id == elevator_id:
                return e
        raise ValueError(f"Unknown elevator id: {elevator_id}")

