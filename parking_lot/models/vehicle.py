from parking_lot.constants import VehicleType


class Vehicle:
    def __init__(self, vehicle_number: str, vehicle_type: VehicleType):
        self.vehicle_number = vehicle_number
        self.vehicle_type = vehicle_type