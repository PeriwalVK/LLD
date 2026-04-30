from __future__ import annotations

import os
import sys


root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if root_folder not in sys.path:
    sys.path.insert(0, root_folder)


from parking_lot.constants import VehicleType
from parking_lot.models.parking_ticket import ParkingTicket
from parking_lot.models.parking_lot import ParkingLot
from parking_lot.models.strategy.fare_strategy import SimpleFareStrategy
from parking_lot.models.strategy.parking_strategy import GreedyParkingStrategy, OptimisedParkingStrategy, Parkingstrategy
from parking_lot.models.vehicle import Vehicle
from parking_lot.models.strategy.payment_strategy import CardPaymentStrategy, CashPaymentStrategy, PaymentStrategy, UPIPaymentStrategy



if __name__ == "__main__":
    # ########### Parking strategies ###########################
    simple_parking_strategy: Parkingstrategy = GreedyParkingStrategy()
    optimised_parking_strategy: Parkingstrategy = OptimisedParkingStrategy()


    # ########### Fare strategies ###########################
    simple_fare_strategy = SimpleFareStrategy()
    
    
    # ########### Payment strategies ###########################
    cash_payment_strategy: PaymentStrategy = CashPaymentStrategy()
    card_payment_strategy: PaymentStrategy = CardPaymentStrategy()
    upi_payment_strategy: PaymentStrategy = UPIPaymentStrategy()

    parking_lot = ParkingLot()

    v1: Vehicle = Vehicle("KA-01-HH-1234", VehicleType.CAR)
    v2: Vehicle = Vehicle("KA-02-HH-1235", VehicleType.BIKE)
    v3: Vehicle = Vehicle("KA-03-HH-1236", VehicleType.TRUCK)
    v4: Vehicle = Vehicle("KA-04-HH-1237", VehicleType.BIKE)
    v5: Vehicle = Vehicle("KA-05-HH-1238", VehicleType.CAR)

    t1: ParkingTicket  = parking_lot.park_vehicle(v1, 0, simple_fare_strategy, optimised_parking_strategy)
    t2: ParkingTicket = parking_lot.park_vehicle(v2, 10, simple_fare_strategy, optimised_parking_strategy)
    t3: ParkingTicket = parking_lot.park_vehicle(v3, 20, simple_fare_strategy, optimised_parking_strategy)
    t4: ParkingTicket = parking_lot.park_vehicle(v4, 30, simple_fare_strategy, optimised_parking_strategy)
    t5: ParkingTicket = parking_lot.park_vehicle(v5, 40, simple_fare_strategy, optimised_parking_strategy)

    print("")

    for t, exit_epoch, payment_strategy in [
        (t1, 10000, cash_payment_strategy),
        (t2, 20000, card_payment_strategy),
        (t3, 30000, upi_payment_strategy),
        (t4, 40000, cash_payment_strategy),
        (t5, 50000, card_payment_strategy)
    ]:
        
        if t:
            parking_lot.unpark_vehicle(t, exit_epoch, payment_strategy)
        # p.unpark_vehicle(t1, 10000, cash_payment_strategy)
        # p.unpark_vehicle(t2, 20000, card_payment_strategy)
        # p.unpark_vehicle(t3, 30000, upi_payment_strategy)
        # p.unpark_vehicle(t4, 40000, cash_payment_strategy)
        # p.unpark_vehicle(t5, 50000, card_payment_strategy)