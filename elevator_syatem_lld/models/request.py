from dataclasses import dataclass

from elevator_syatem_lld.constants import Direction


@dataclass(frozen=True)
class HallRequest:
    source_floor: int
    direction: Direction


@dataclass(frozen=True)
class CarRequest:
    elevator_id: int
    destination_floor: int

