from abc import ABC, abstractmethod
from typing import Dict, List
from Elevator_System.constants import ElevatorDirection
from Elevator_System.models.elevator import Elevator
from Elevator_System.models.floor import Floor
from Elevator_System.models.request import ElevatorCallRequest




class ElevatorSelectionStrategy(ABC):
    def __init__(self):
        # self.elevators: List[Elevator] = elevators
        # self.floors: Dict[int, Floor] = floors_dict
        pass
    @abstractmethod
    def select_elevator(self, request: ElevatorCallRequest, elevators: List[Elevator]) -> Elevator:
        pass

class MinCostStrategy(ElevatorSelectionStrategy):
    def __init__(self):
        super().__init__()
    
    # def _lambda(src_floor_number: int, direction: ElevatorDirection):
        
    
    def select_elevator(self, request: ElevatorCallRequest, elevators: List[Elevator]) -> Elevator:
        priority = [
            request.direction, 
            ElevatorDirection.IDLE, 
            ElevatorDirection.DOWN if request.direction == ElevatorDirection.UP else ElevatorDirection.UP
        ]
        feasible_dir = [
            request.direction, 
            ElevatorDirection.IDLE, 
            # ElevatorDirection.DOWN if direction == ElevatorDirection.UP else ElevatorDirection.UP
        ]

        # sorted_elevators = sorted(
        #     self.elevators, 
        #     key=lambda x: (abs(x.current_floor.floor_number - src_floor_number), priority.index(x.direction))
        # )
        # elevator = sorted_elevators[0]
        min_elevator = elevators[0]
        min_dir = min_elevator.direction
        min_distance = abs(min_elevator.current_floor.floor_number - src_floor_number)
        for elevator in elevators[1:]:
            if elevator.direction == direlevator.current_floor.floor_number <= src_floor_number:
                return elevator

        if direction == ElevatorDirection.UP:
            filtered_elevators = [
                elevator for elevator in sorted_elevators if elevator.direction in priority[:2] and elevator.current_floor.floor_number <= src_floor_number]
        # assigned_elevator = next((elevator for elevator in filtered_elevators if elevator is not None), None)

        if 

        for elevator in elevators:
            if elevator.direction == direction and elevator.current_floor.floor_number <= src_floor_number:
                return elevator
        
        # # filtered_ = [elevator for elevator in self.elevators if elevator.direction in feasible_dir]
        # sorted(self.elevators, key=lambda elevator: (abs(elevator.current_floor.floor_number - src_floor_number), feasible_dir.index(x.direction))
        # assigned_elevator = None
        # min_distance = float('inf')
        
        # for elevator in self.elevators:
        #     distance = abs(elevator.current_floor.floor_number - src_floor_number)
        #     if feasible_dir_found:
        #         distance = distance
        #     else:
        #         pass

                
        #     if distance < min_distance and elevator.direction in [direction, ElevatorDirection.IDLE]:
        #         min_distance = distance
        #         assigned_elevator = elevator
        #     elif distance == min_distance and \
        #         (elevator.direction == direction or ):
                
        # return assigned_elevator
        
    