from __future__ import annotations

import os
import sys

root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_folder not in sys.path:
    sys.path.insert(0, root_folder)

from elevator_syatem_lld.constants import Direction
from elevator_syatem_lld.models.building import Building
from elevator_syatem_lld.models.elevator import Elevator
from elevator_syatem_lld.models.request import CarRequest, HallRequest
from elevator_syatem_lld.service.elevator_controller import ElevatorController
from elevator_syatem_lld.strategy.elevator_selection_strategy import NearestCarStrategy


def print_state(controller: ElevatorController, title: str) -> None:
    print(f"\n--- {title} ---")
    for row in controller.snapshot():
        print(row)


if __name__ == "__main__":
    building = Building(
        total_floors=15,
        elevators=[
            Elevator(elevator_id=1, current_floor=0),
            Elevator(elevator_id=2, current_floor=7),
            Elevator(elevator_id=3, current_floor=12),
        ],
    )
    controller = ElevatorController(building, NearestCarStrategy())

    print_state(controller, "Initial")

    hall = HallRequest(source_floor=5, direction=Direction.UP)
    assigned = controller.request_elevator(hall)
    print(f"\nHall request at floor {hall.source_floor} assigned to Elevator#{assigned.elevator_id}")

    for i in range(5):
        controller.tick()
        print_state(controller, f"After tick {i + 1}")

    controller.select_floor(CarRequest(elevator_id=assigned.elevator_id, destination_floor=11))
    print_state(controller, "Passenger selected destination 11")

    for i in range(8):
        controller.tick()
        print_state(controller, f"Travel tick {i + 1}")

