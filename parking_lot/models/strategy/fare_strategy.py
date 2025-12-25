from abc import ABC
import math

from parking_lot.constants import VehicleType


class FareStrategy(ABC):
    def calculate_fare(self, vehicle_type: VehicleType, duration_seconds: int) -> int:
        pass

class SimpleFareStrategy(FareStrategy):
    def __init__(self):
        self.fare_map = { # per hour
            VehicleType.BIKE: 10,
            VehicleType.CAR: 20,
            VehicleType.TRUCK: 30
        }
        self.default_fare = 20

    def calculate_fare(self, vehicle_type: VehicleType, duration_seconds: int) -> int:
        fare = math.ceil(duration_seconds/3600) * self.fare_map.get(vehicle_type, self.default_fare)
        print(f"[SimpleFareStrategy]: Fare for vehicle_type {vehicle_type.value} for duration {duration_seconds} is ${fare}.")
        return fare