from __future__ import annotations
from abc import ABC
from typing import TYPE_CHECKING, Dict, List

from parking_lot.constants import VehicleType
from parking_lot.exceptions import NoParkingSpotAvailableException
from parking_lot.models.parking_spot import ParkingSpot

if TYPE_CHECKING:
    from parking_lot.models.parking_lot import ParkingLot


class Parkingstrategy(ABC):
    def __init__(self):
        pass
    def fetch_parking_spot(self, parking_spots: Dict[VehicleType, List[ParkingSpot]], vehicle_type: VehicleType) -> ParkingSpot:
        pass

class GreedyParkingStrategy(Parkingstrategy):

    def __init__(self):
        super().__init__()

    def fetch_parking_spot(self, parking_spots: Dict[VehicleType, List[ParkingSpot]], vehicle_type: VehicleType) -> ParkingSpot:
        for spot in parking_spots[vehicle_type]:
            if spot.available():
                print(f"[GreedyParkingStrategy]: spot {spot.spot_id} is available for {vehicle_type.value}")
                return spot
        raise NoParkingSpotAvailableException(f"[GreedyParkingStrategy]: No parking spot available for {vehicle_type.value}")

class OptimisedParkingStrategy(Parkingstrategy):

    def __init__(self):
        super().__init__()
        self.priority: List[VehicleType] = [VehicleType.BIKE, VehicleType.CAR, VehicleType.TRUCK]

    def fetch_parking_spot(self, parking_spots: Dict[VehicleType, List[ParkingSpot]], vehicle_type: VehicleType) -> ParkingSpot:
        index = self.priority.index(vehicle_type)
        for _each_vehicle_type in self.priority[index:]:
            print(f"[OptimisedParkingStrategy]: finding a {_each_vehicle_type.value} parking spot...")
            for spot in parking_spots[_each_vehicle_type]:
                if spot.available():
                    print(f"[OptimisedParkingStrategy]: spot {spot.spot_id} is available for {vehicle_type.value}")
                    return spot
            
        raise NoParkingSpotAvailableException(f"[OptimisedParkingStrategy]: No parking spot available for {vehicle_type.value}")