from __future__ import annotations
from abc import ABC
from typing import TYPE_CHECKING

from parking_lot.constants import VehicleType
from parking_lot.exceptions import NoParkingSpotAvailableException
from parking_lot.models.parking_spot import ParkingSpot

if TYPE_CHECKING:
    from parking_lot.models.parking_lot import ParkingLot


class Parkingstrategy(ABC):
    def __init__(self):
        pass
    def fetch_parking_spot(self, parking_lot: ParkingLot) -> ParkingSpot:
        pass

class GreedyParkingStrategy(Parkingstrategy):

    def __init__(self):
        super().__init__()

    def fetch_parking_spot(self, parking_lot: ParkingLot, vehicle_type: VehicleType) -> ParkingSpot:
        for spot in parking_lot.parking_spots[vehicle_type]:
            if spot.available():
                return spot
        raise NoParkingSpotAvailableException("[GreedyParkingStrategy]: No parking spot available")