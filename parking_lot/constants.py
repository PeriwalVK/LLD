from enum import Enum


class VehicleType(Enum):
    CAR = "CAR"
    BIKE = "BIKE"
    TRUCK = "TRUCK"

class ParkingTicketStatus(Enum):
    IN = "IN"
    OUT = "OUT"

class DefaultValues:
    
    CAR_SPOT_COUNT = 2
    BIKE_SPOT_COUNT = 1
    TRUCK_SPOT_COUNT = 1

    PARKING_LOT_SIZE = CAR_SPOT_COUNT + BIKE_SPOT_COUNT + TRUCK_SPOT_COUNT

