### Objects ###
# Elevator
# Buttons
# External Buttons
# Internal Buttons
# Requests
# Elevator events
# Door
# Elevator Door
# Floor Door
# Displays
# Floor Number Screen
# Floors

### Data Sturcutres ###
# upRequests priority queue
# downRequests priority queue
# Pending requests Dictionary

### Object Relationships ###
# Elevator has a Elevator Door, Internal Buttons, Floor Number screen
# Floors have floor door, floor number screen, external buttons
# Elevator Door is a door
# Internal buttons are buttons
# Floor number screens are displays

### Design Patterns ###
# Pub/Sub: Elevator is the subject and publisher, all buttons and displays sub
# elevator to figure out what to display and when to light up
# Req/Rep: Buttons send elevator request which then generates a response

### Future work ###
# Multithreading, multi elevators
# Elevator controller/strategy that can be swapped out

from enum import Enum
from abc import ABC, abstractmethod
from typing import List
# from turtle import up

NUMBER_OF_FLOORS = 10


class DoorType(Enum):
    floor = "FLOOR"
    elevator = "ELEVATOR"


class DoorStatus(Enum):
    open = "OPEN"
    closed = "CLOSED"


class Door:
    def __init__(
        self, typeD: DoorType, location=None, status: DoorStatus = DoorStatus.closed
    ):
        self.location = location
        self.typeD: DoorType = typeD
        self.status: DoorStatus = status

    def open(self):
        self.status = DoorStatus.open

    def close(self):
        self.status = DoorStatus.closed


class ElevatorDoor(Door):
    def __init__(self):
        super().__init__(DoorType.elevator)


class FloorDoor(Door):
    def __init__(self, location):
        super().__init__(DoorType.floor, location)


class ButtonType(Enum):
    internal = "INTERNAL"
    external = "EXTERNAL"


class ButtonStatus(Enum):
    pressed = "PRESSED"
    unpressed = "UNPRESSED"


class Button(ABC):
    def __init__(
        self, typeB: ButtonType, status: ButtonStatus = ButtonStatus.unpressed
    ):
        self.typeB: ButtonType = typeB
        self.status: ButtonStatus = status

    def press(self):
        self.status = ButtonStatus.pressed
        self.sendRequest()

    def unpress(self):
        # Pub published fulfilled requeset
        self.status = ButtonStatus.unpressed

    @abstractmethod
    def sendRequest(self):
        pass


class ElevatorGoToFloorButton(Button):
    def __init__(self, goToFloor: int):
        super().__init__(ButtonType.internal)
        self.goToFloor: int = goToFloor

    def sendRequest(self):
        if self.goToFloor > elevator.location:
            request = Request(
                RequestType.internal,
                RequestDirection.up,
                elevator.location,
                self.goToFloor,
            )
            elevator.request(request)
        else:
            request = Request(
                RequestType.internal,
                RequestDirection.down,
                elevator.location,
                self.goToFloor,
            )
            elevator.request(request)


class FloorButtonType(Enum):
    up = "UP"
    down = "DOWN"


class FloorButton(Button):
    def __init__(self, typeFB: FloorButtonType, location: int):
        super().__init__(ButtonType.external)
        self.location: int = location
        self.typeFB: FloorButtonType = typeFB

    def sendRequest(self):
        print("Sending Floor Button Request", self.location, self.typeFB)
        if self.typeFB == FloorButtonType.up:
            request = Request(
                RequestType.external, RequestDirection.up, self.location, self.location
            )
            elevator.request(request)

        else:
            request = Request(
                RequestType.external,
                RequestDirection.down,
                self.location,
                self.location,
            )
            elevator.request(request)


floor = FloorButton(FloorButtonType.up, 0)


class RequestType(Enum):
    internal = "INTERNAL"
    external = "EXTERNAL"


class RequestDirection(Enum):
    up = 1
    down = 0


class Request:
    def __init__(
        self, typeR: RequestType, direction: RequestDirection, origin: int, target: int
    ):
        self.typeR: RequestType = typeR
        self.direction: RequestDirection = direction
        self.origin: int = origin
        self.target: int = target


class ElevatorStatus(Enum):
    down = 0
    up = 1
    idle = 2


class Elevator:
    def __init__(self, location: int = 0):
        self.location: int = 0
        self.status: ElevatorStatus = ElevatorStatus.idle
        self.door: ElevatorDoor = ElevatorDoor()
        self.goTobuttons = [ElevatorGoToFloorButton(i) for i in range(NUMBER_OF_FLOORS)]
        # self.display
        # self.open button
        # selt.close
        # phone, emergency
        # weight limit
        self.upRequests: List[Request] = []
        self.downRequests: List[Request] = []

    def run(self):
        while self.upRequests or self.downRequests:
            self.processRequests()

    def processRequests(self):
        if self.upRequests:
            self.processUpRequests()
            self.processDownRequests()

        else:
            self.processDownRequests()

    def processUpRequests(self):
        "Process uprequests by closest floor first"
        while self.upRequests:
            # Set status to moving up
            # Pop closest up request off the stack
            # Close Door
            # Move to request floor
            # Open door
            # Wait a few seconds
            # Remove any up or down requests that happen to coincide with the current floor or add pending requests that coincide with origin
            # Publish event for fulfilled request, unpressing buttons and changing displays
            # close door
            self.status = ElevatorStatus.up
            current_request = self.upRequests.pop(0)
            self.door.close()
            self.location = current_request.target
            self.door.open()
            if current_request.target == current_request.origin:
                print("Picking up people for Up Request, on floor:", self.location)

            else:
                print("Letting people off for Up Request, on floor:", self.location)
            self.door.close()

        self.status = ElevatorStatus.idle

    def processDownRequests(self):
        "Process downRequests by closest floor first"
        while self.downRequests:
            # Set status to moving up
            # Pop closest up request off the stack
            # Close Door
            # Move to request floor
            # Open door
            # Wait a few seconds
            # Remove any up or down requests that happen to coincide with the current floor or add pending requests that coincide with origin
            # close door
            self.status = ElevatorStatus.down
            current_request = self.downRequests.pop(0)
            self.door.close()
            self.location = current_request.target
            # Open Floor Door
            self.door.open()
            if current_request.target == current_request.origin:
                print("Picking up people for Down Request, on floor:", self.location)

            else:
                print("Letting people off for Down Request, on floor:", self.location)
            self.door.close()
        self.status = ElevatorStatus.idle

    def request(self, request: Request):
        if request.direction == RequestDirection.up:
            self.upRequests.append(request)
            self.upRequests.sort(key=lambda x: x.target)

        else:
            self.downRequests.append(request)
            self.downRequests.sort(key=lambda x: -x.target)


class Floor:
    def __init__(self, location):
        self.location = location
        self.upButton = FloorButton(FloorButtonType.up, location)
        self.downButton = FloorButton(FloorButtonType.down, location)
        self.door = FloorDoor(location)

    def pressFloorButton(self, direction):
        if direction == FloorButtonType.up:
            self.upButton.press()
        else:
            self.downButton.press()


elevator = Elevator()

Floors = [Floor(i) for i in range(NUMBER_OF_FLOORS)]


Floors[4].pressFloorButton(FloorButtonType.up)
elevator.location = 4
elevator.goTobuttons[2].press()
elevator.run()

print()
print("RUN 2")

elevator.goTobuttons[9].press()
elevator.goTobuttons[5].press()
elevator.goTobuttons[7].press()
elevator.goTobuttons[0].press()
elevator.goTobuttons[1].press()

elevator.run()
