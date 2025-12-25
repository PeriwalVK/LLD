from __future__ import annotations

import os
import sys




root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if root_folder not in sys.path:
    sys.path.insert(0, root_folder)


from parking_lot.constants import VehicleType
from parking_lot.models.parking_lot import ParkingLot
from parking_lot.models.strategy.fare_strategy import SimpleFareStrategy
from parking_lot.models.strategy.parking_strategy import GreedyParkingStrategy, Parkingstrategy
from parking_lot.models.vehicle import Vehicle
from parking_lot.models.strategy.payment_strategy import CardPaymentStrategy, CashPaymentStrategy, UPIPaymentStrategy



if __name__ == "__main__":
    parking_strategy: Parkingstrategy = GreedyParkingStrategy()
    
    simple_fare_strategy = SimpleFareStrategy()
    
    cash_payment_strategy = CashPaymentStrategy()
    card_payment_strategy = CardPaymentStrategy()
    upi_payment_strategy = UPIPaymentStrategy()

    p = ParkingLot(parking_strategy)

    v1: Vehicle = Vehicle("KA-01-HH-1234", VehicleType.CAR)
    v2: Vehicle = Vehicle("KA-02-HH-1235", VehicleType.BIKE)
    v3: Vehicle = Vehicle("KA-03-HH-1236", VehicleType.TRUCK)
    v4: Vehicle = Vehicle("KA-04-HH-1237", VehicleType.BIKE)
    v5: Vehicle = Vehicle("KA-05-HH-1238", VehicleType.CAR)

    t1 = p.park_vehicle(v1, 0, simple_fare_strategy)
    t2 = p.park_vehicle(v2, 10, simple_fare_strategy)
    t3 = p.park_vehicle(v3, 20, simple_fare_strategy)
    t4 = p.park_vehicle(v4, 30, simple_fare_strategy)
    t5 = p.park_vehicle(v5, 40, simple_fare_strategy)

    print("")

    for t, exit_epoch, strategy in [
        (t1, 10000, cash_payment_strategy),
        (t2, 20000, card_payment_strategy),
        (t3, 30000, upi_payment_strategy),
        (t4, 40000, cash_payment_strategy),
        (t5, 50000, card_payment_strategy)
    ]:
        
        if t:
            p.unpark_vehicle(t, exit_epoch, strategy)
        # p.unpark_vehicle(t1, 10000, cash_payment_strategy)
        # p.unpark_vehicle(t2, 20000, card_payment_strategy)
        # p.unpark_vehicle(t3, 30000, upi_payment_strategy)
        # p.unpark_vehicle(t4, 40000, cash_payment_strategy)
        # p.unpark_vehicle(t5, 50000, card_payment_strategy)