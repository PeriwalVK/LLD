from ast import Dict
from typing import List

from Elevator_System.constants import BuildingConstants, ElevatorDirection
from Elevator_System.models.elevator import Elevator
from Elevator_System.models.floor import Floor
from Elevator_System.models.request import ElevatorCallRequest, ElevatorDropRequest
from Elevator_System.models.strategy.elevator_selection_strategy import ElevatorSelectionStrategy


class ElevatorController:
    def __init__(self, selection_strategy: ElevatorSelectionStrategy=None):
        self.elevators: List[Elevator] = list()
        self.floors_dict: Dict[int, Floor] = dict()
        self.floor_cnt: int = 0
        self.selection_strategy: ElevatorSelectionStrategy = selection_strategy
        # self.up_requests: Dict[int, ElevatorRequest] = {floor: [] for floor in range(BuildingConstants.MIN_FLOOR, BuildingConstants.MAX_FLOOR + 1)}
        # self.down_requests: Dict[int, ElevatorRequest] = {floor: [] for floor in range(BuildingConstants.MIN_FLOOR, BuildingConstants.MAX_FLOOR + 1)}
    
    # def request_exists(self, floor_number: int, curr_direction: ElevatorDirection) -> bool:
    #     pass

    def add_elevator(self, elevator: Elevator):
        self.elevators.append(elevator)
    
    def add_floor(self, floor: Floor):
        self.floors_dict[floor.floor_number] = floor
        self.floor_cnt += 1
    
    def set_strategy(self, strategy: ElevatorSelectionStrategy):
        self.selection_strategy = strategy

    def make_external_request(self, request: ElevatorCallRequest):
        if self.selection_strategy:
            elevator = self.selection_strategy.select_elevator(request, self.elevators)
            elevator.assign_external_request(request)
        else:
            print("No Selection Strategy, please set a strategy before")

        