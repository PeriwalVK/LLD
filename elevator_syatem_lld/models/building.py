from dataclasses import dataclass
from typing import List

from elevator_syatem_lld.exceptions import InvalidFloorError
from elevator_syatem_lld.models.elevator import Elevator


@dataclass
class Building:
    total_floors: int
    elevators: List[Elevator]

    def validate_floor(self, floor: int) -> None:
        if floor < 0 or floor >= self.total_floors:
            raise InvalidFloorError(f"Invalid floor: {floor}")

