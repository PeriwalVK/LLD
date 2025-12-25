from parking_lot.constants import ParkingTicketStatus
from parking_lot.models.parking_spot import ParkingSpot
from parking_lot.models.strategy.fare_strategy import FareStrategy
from parking_lot.models.strategy.payment_strategy import PaymentStrategy
from parking_lot.models.vehicle import Vehicle


class ParkingTicket:
    def __init__(self, vehicle: Vehicle, parking_spot: ParkingSpot, fare_strategy: FareStrategy):
        self.id = f"{vehicle.vehicle_number}_{parking_spot.spot_id}"
        self.vehicle: Vehicle = vehicle
        self.parking_spot: ParkingSpot = parking_spot
        self.fare_strategy: FareStrategy = fare_strategy
        self.entry_epoch: int = None
        self.exit_epoch: int = None
            
    def punch_in(self, entry_epoch: int) -> None:
        self.set_entry_epoch(entry_epoch)
        self.status = ParkingTicketStatus.IN
        self.parking_spot.occupy()
    
    def punch_out(self, exit_epoch: int) -> None:
        self.set_exit_epoch(exit_epoch)
        self.status = ParkingTicketStatus.OUT
        self.parking_spot.release()
    
    def set_entry_epoch(self, entry_epoch: int) -> None:
        self.entry_epoch = entry_epoch

    def set_exit_epoch(self, exit_epoch: int) -> None:
        self.exit_epoch = exit_epoch
    
    def calculate_fare(self, exit_epoch: int) -> int:
        return self.fare_strategy.calculate_fare(self.vehicle.vehicle_type, exit_epoch - self.entry_epoch)
    
    def make_payment(self, fare: int, payment_strategy: PaymentStrategy) -> None:
        payment_strategy.make_payment(fare)
    
    

    


