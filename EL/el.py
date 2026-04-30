from enum import Enum
from abc import ABC, abstractmethod
import random
import time


class Direction(Enum):
    UP = 1
    DOWN = -1
    IDLE = 0


class RequestFromFloor:
    """
    Represents a request made from a floor.
    """

    def __init__(self, floor: int, direction: Direction):
        self.floor = floor
        self.direction = direction


class RequestFromElevator:
    """
    Represents a request made from inside an elevator car (destination selection).
    """

    def __init__(self, elevator_id: int, destination_floor: int):
        self.elevator_id = elevator_id
        self.destination_floor = destination_floor


def opposite_direction(direction: Direction):
    if direction == Direction.UP:
        return Direction.DOWN
    elif direction == Direction.DOWN:
        return Direction.UP
    else:
        return Direction.IDLE

class Elevator:
    """
    Represents a single elevator.
    """

    def __init__(self, elevator_id: int, current_floor: int = 0):
        self.id = elevator_id
        
        self.current_floor = current_floor
        self.direction = Direction.IDLE

        self.floor_requests = {
            Direction.UP: [],
            Direction.DOWN: []
        }

    def add_request(self, floor: int):
        """
        Add a target floor to elevator queue.
        """
        # self.target_floors.add(floor)
        if floor >= self.current_floor and floor not in self.floor_requests[Direction.UP]:
            self.floor_requests[Direction.UP].append(floor)
            self.floor_requests[Direction.UP].sort()
        elif floor < self.current_floor and floor not in self.floor_requests[Direction.DOWN]:
            self.floor_requests[Direction.DOWN].append(floor)
            self.floor_requests[Direction.DOWN].sort(reverse=True)
    
    def has_req(self) -> bool:
        return self.floor_requests[Direction.UP] or self.floor_requests[Direction.DOWN]

    def step(self):
        """
        Move elevator by ONE step (one floor).
        """

        self._update_direction()
        
        if self.direction == Direction.IDLE:
            return
        
        target = self.floor_requests[self.direction][0]

        if target > self.current_floor:
            # self.direction = Direction.UP
            self.current_floor += 1

        elif target < self.current_floor:
            # self.direction = Direction.DOWN
            self.current_floor -= 1

        else:
            print(f"Elevator {self.id} STOPPED at floor {self.current_floor}")
            self.floor_requests[self.direction].remove(target)
            self._update_direction()
            # self.direction = Direction.IDLE
    
    def _update_direction(self):

        if self.direction == Direction.IDLE:
            if self.has_req():
                self.direction = Direction.UP if self.floor_requests[Direction.UP] else Direction.DOWN
        else:
            if not self.has_req():
                self.direction = Direction.IDLE
            else:
                if not self.floor_requests[self.direction]:
                    self.direction = opposite_direction(self.direction)



class ElevatorAssignmentStrategy(ABC):
    """
    Strategy interface for selecting elevator.
    """

    @abstractmethod
    def select_elevator(self, elevators, request):
        pass


class NearestElevatorStrategy(ElevatorAssignmentStrategy):
    """
    Assign the nearest elevator.
    """

    def select_elevator(self, elevators, request):

        best_elevator = []
        min_distance = float("inf")

        for elevator in elevators:

            distance = abs(elevator.current_floor - request.floor)

            if distance < min_distance:
                min_distance = distance
                best_elevator = [elevator]
            elif distance == min_distance:
                best_elevator.append(elevator)

        if best_elevator:
            return random.choice(best_elevator)
        return None


class ElevatorController:
    """
    Handles elevator assignment using strategy.
    """

    def __init__(self, elevators, strategy: ElevatorAssignmentStrategy):
        self.elevators = elevators
        self.strategy = strategy

    def assign_elevator(self, request_from_floor: RequestFromFloor):

        elevator = self.strategy.select_elevator(self.elevators, request_from_floor)

        elevator.add_request(request_from_floor.floor)

        print(f"Request at floor {request_from_floor.floor} assigned to Elevator {elevator.id}")

        return elevator

    def assign_inside_request(self, request_from_elevator: RequestFromElevator):
        elevator = self._get_elevator_by_id(request_from_elevator.elevator_id)
        elevator.add_request(request_from_elevator.destination_floor)
        print(
            f"Inside request: Elevator {elevator.id} got destination {request_from_elevator.destination_floor}"
        )
        return elevator

    def _get_elevator_by_id(self, elevator_id: int):
        for elevator in self.elevators:
            if elevator.id == elevator_id:
                return elevator
        raise ValueError(f"Invalid elevator id: {elevator_id}")


class ElevatorSystem:
    """
    Main system managing elevators.
    """

    def __init__(self, num_elevators: int):

        self.elevators = [Elevator(i, 2) for i in range(num_elevators)]

        strategy = NearestElevatorStrategy()
        self.controller = ElevatorController(self.elevators, strategy)

    def request_elevator(self, floor: int, direction: Direction):

        request_from_floor = RequestFromFloor(floor, direction)

        self.controller.assign_elevator(request_from_floor)

    def request_from_inside_elevator(self, elevator_id: int, destination_floor: int):
        request_from_elevator = RequestFromElevator(elevator_id, destination_floor)
        self.controller.assign_inside_request(request_from_elevator)

    def step(self):
        """
        System scheduler step.
        Moves all elevators once.
        """

        while any(elevator.has_req() for elevator in self.elevators): 
            for elevator in self.elevators:
                if not elevator.has_req():
                    continue
                elevator.step()
                print(
                    f"Elevator {elevator.id} reached floor {elevator.current_floor} direction {elevator.direction}"
                )
        
            print()

    def print_elevator_status(self):
        for elevator in self.elevators:
            print(
                f"Elevator {elevator.id} NOW at floor {elevator.current_floor} direction {elevator.direction}"
            )

# -----------------------------
# Example Simulation
# -----------------------------

system = ElevatorSystem(2)

system.request_elevator(5, Direction.UP)
system.request_elevator(2, Direction.DOWN)
system.request_elevator(1, Direction.UP)
system.request_elevator(3, Direction.DOWN)
system.request_from_inside_elevator(0, 8)
system.request_from_inside_elevator(1, 0)


for _ in range(10):
    system.step()
    time.sleep(0.2)

system.print_elevator_status()