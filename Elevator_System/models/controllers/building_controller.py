from Elevator_System.models.controllers.elevator_controller import ElevatorController


class BuildingController:
    def __init__(self, elevator_controller: ElevatorController):
        self.elevator_controller = elevator_controller
        