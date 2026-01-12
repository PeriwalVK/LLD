from Elevator_System.constants import ElevatorDirection


class ElevatorCallRequest:
    def __init__(self, src_floor: int, direction: ElevatorDirection):
        self.src_floor: int = src_floor
        self.direction: ElevatorDirection = direction
    
    
    # def set_destination(self, dst_floor: int):
    #     self.dst_floor = dst_floor
    #     if self.dst_floor < self.src_floor  and self.direction == ElevatorDirection.UP:
    #         self.direction = ElevatorDirection.DOWN
    #     elif self.dst_floor > self.src_floor and self.direction == ElevatorDirection.DOWN:
    #         self.direction = ElevatorDirection.UP

class ElevatorDropRequest:
    def __init__(self, dst_floor: int = None):
        self.dst_floor: int = dst_floor
    
    
    # def set_destination(self, dst_floor: int):
    #     self.dst_floor = dst_floor
    #     if self.dst_floor < self.src_floor  and self.direction == ElevatorDirection.UP:
    #         self.direction = ElevatorDirection.DOWN
    #     elif self.dst_floor > self.src_floor and self.direction == ElevatorDirection.DOWN:
    #         self.direction = ElevatorDirection.UP

