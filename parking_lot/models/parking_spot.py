from parking_lot.constants import VehicleType
from parking_lot.models.vehicle import Vehicle


class ParkingSpot:
    def __init__(self, spot_id: str, vehicle_type: VehicleType, is_available: bool = True):
        self.spot_id: str = spot_id
        self.vehicle_type: VehicleType = vehicle_type
        self.is_available: bool = is_available
        self.vehicle: Vehicle = None
    
    def available(self) -> bool:
        return self.is_available

    def release(self):
        self.is_available = True
        self.vehicle = None
        print(f"[ParkingSpot]: parking spot_id {self.spot_id} is now released")
    
    def occupy(self, vehicle: Vehicle):
        self.is_available = False
        self.vehicle = vehicle
        print(f"[ParkingSpot]: parking spot_id {self.spot_id} is now occupied by {vehicle.vehicle_type.value} {vehicle.vehicle_number}")
     