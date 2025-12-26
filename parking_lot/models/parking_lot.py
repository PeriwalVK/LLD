from typing import Dict, List
from parking_lot.constants import DefaultValues, ParkingTicketStatus, VehicleType
from parking_lot.exceptions import NoParkingSpotAvailableException
from parking_lot.models.parking_spot import ParkingSpot
from parking_lot.models.parking_ticket import ParkingTicket
from parking_lot.models.strategy.fare_strategy import FareStrategy
from parking_lot.models.strategy.parking_strategy import Parkingstrategy
from parking_lot.models.strategy.payment_strategy import PaymentStrategy
from parking_lot.models.vehicle import Vehicle


class ParkingLot:
    def __init__(self, parking_strategy: Parkingstrategy):
        
        self.capacity = DefaultValues.PARKING_LOT_SIZE

        self.parking_spots: Dict[VehicleType, List[ParkingSpot]] = {
            VehicleType.CAR: [ParkingSpot(f"{VehicleType.CAR.value}_{i}", VehicleType.CAR) for i in range(DefaultValues.CAR_SPOT_COUNT)],
            VehicleType.BIKE: [ParkingSpot(f"{VehicleType.BIKE.value}_{i}", VehicleType.BIKE) for i in range(DefaultValues.BIKE_SPOT_COUNT)],
            VehicleType.TRUCK: [ParkingSpot(f"{VehicleType.TRUCK.value}_{i}", VehicleType.TRUCK) for i in range(DefaultValues.TRUCK_SPOT_COUNT)],
        }
        self.parking_strategy: Parkingstrategy = parking_strategy
        # self.fare_strategy: FareStrategy = fare_strategy

        self.parking_tickets: Dict[ParkingTicketStatus, List[ParkingTicket]] = {
            ParkingTicketStatus.IN: [],
            ParkingTicketStatus.OUT: []
        }

        self.total_earnings = 0

    def set_parking_strategy(self, parking_strategy: Parkingstrategy):
        self.parking_strategy = parking_strategy
    
    def _vehicle_enters(self, ticket: ParkingTicket, entry_epoch: int):
        ticket.punch_in(entry_epoch)
        self.parking_tickets[ParkingTicketStatus.IN].append(ticket)
        
    
    def _vehicle_exits(self, ticket: ParkingTicket, exit_epoch: int):
        ticket.punch_out(exit_epoch)
        self.parking_tickets[ParkingTicketStatus.IN].remove(ticket)
        self.parking_tickets[ParkingTicketStatus.OUT].append(ticket)
        


    def park_vehicle(self, vehicle: Vehicle, entry_epoch: int, fare_strategy: FareStrategy) -> ParkingTicket:
        try:
            print(f"[ParkingLot]: {vehicle.vehicle_type.value} {vehicle.vehicle_number} is trying to enter the parking lot...")
            parking_spot: ParkingSpot = self.parking_strategy.fetch_parking_spot(self.parking_spots, vehicle.vehicle_type)

            ticket = ParkingTicket(vehicle, parking_spot, fare_strategy)
            self._vehicle_enters(ticket, entry_epoch)
            print(f"[ParkingLot]: {vehicle.vehicle_type.value} {vehicle.vehicle_number} has been parked at {parking_spot.spot_id}. Ticket Number: {ticket.id}\n")
            return ticket
        except NoParkingSpotAvailableException as e:
            print(f"[ParkingLot]: No Parking Spot Available for {vehicle.vehicle_type.value} {vehicle.vehicle_number}...\n")
    
    def _increase_earnings(self, fare: int):
        self.total_earnings += fare
        print(f"[ParkingLot]: Total Earnings: ${self.total_earnings}")

    def unpark_vehicle(self, ticket: ParkingTicket, exit_epoch: int, payment_strategy: PaymentStrategy) -> None:
        print(f"[ParkingLot]: {ticket.vehicle.vehicle_type.value} {ticket.vehicle.vehicle_number} is trying to exit the parking lot...")
        fare = ticket.calculate_fare(exit_epoch)
        ticket.make_payment(fare, payment_strategy)
        self._vehicle_exits(ticket, exit_epoch)
        self._increase_earnings(fare)

        print(f"[ParkingLot]: {ticket.vehicle.vehicle_type.value} {ticket.vehicle.vehicle_number} Exited the Parking Lot.\n")

