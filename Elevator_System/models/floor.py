from Elevator_System.constants import ElevatorDirection
from Elevator_System.models.controllers.elevator_controller import ElevatorController
from Elevator_System.models.door import Door
from Elevator_System.models.request import ElevatorCallRequest


class Floor:
    def __init__(self, floor_number: int, elevator_controller: ElevatorController = None):
        self.floor_number = floor_number
        self.elevator_controller: ElevatorController = elevator_controller
        
        # self.door: Door = Door()
        # self.displays = []

    def set_elevator_controller(self, elevator_controller: ElevatorController):
        self.elevator_controller = elevator_controller
    
    def press_button(self, direction: ElevatorDirection):
        if self.elevator_controller: 
            self.elevator_controller.make_external_request(ElevatorCallRequest(self.floor_number, direction))
        else:
            print("No Elevator Controller")
    
