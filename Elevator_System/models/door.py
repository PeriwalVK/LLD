from Elevator_System.constants import DoorStatus


class Door:
    def __init__(self):
        self.status: DoorStatus = DoorStatus.CLOSED
    
    def open(self):
        self.status = DoorStatus.OPEN
    
    def close(self):
        self.status = DoorStatus.CLOSED
    
    def is_open(self):
        return self.status == DoorStatus.OPEN