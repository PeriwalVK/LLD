from parking_lot.constants import VehicleType


class ParkingSpot:
    def __init__(self, spot_id: str, vehicle_type: VehicleType, is_available: bool = True):
        self.spot_id: str = spot_id
        self.vehicle_type: VehicleType = vehicle_type
        self.is_available: bool = is_available
    
    def available(self) -> bool:
        return self.is_available

    def release(self):
        self.is_available = True
        print(f"[ParkingSpot]: parking spot_id {self.spot_id} is now released")
    
    def occupy(self):
        self.is_available = False
        print(f"[ParkingSpot]: parking spot_id {self.spot_id} is now occupied")
     