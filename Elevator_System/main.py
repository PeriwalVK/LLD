from __future__ import annotations

import os
import sys
from typing import Dict, List

from Elevator_System.constants import BuildingConstants
from Elevator_System.models import elevator
from Elevator_System.models.controllers.building_controller import BuildingController
from Elevator_System.models.controllers.elevator_controller import ElevatorController
from Elevator_System.models.elevator import Elevator
from Elevator_System.models.floor import Floor
from Elevator_System.models.strategy import elevator_selection_strategy
from Elevator_System.models.strategy.elevator_selection_strategy import MinCostStrategy




root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if root_folder not in sys.path:
    sys.path.insert(0, root_folder)





if __name__ == "__main__":

    min_cost_strategy = MinCostStrategy()
    elevator_controller = ElevatorController(min_cost_strategy)


    my_floors: List[Floor] = []
    for i in range(BuildingConstants.MIN_FLOOR, BuildingConstants.MAX_FLOOR + 1):
        floor = Floor(i, elevator_controller)
        elevator_controller.add_floor(floor)
        my_floors.append(floor)

    # my_floors_dict: Dict[int, Floor] = {floor.floor_number: floor for floor in my_floors}


    my_elevators: List[Elevator] = []
    for i in range(BuildingConstants.ELEVATORS_COUNT):
        elevator = Elevator(i, elevator_controller)
        elevator_controller.add_elevator(elevator)
        my_elevators.append(elevator)

    
    


