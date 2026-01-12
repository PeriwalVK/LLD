from typing import Dict, List

from Elevator_System.constants import ElevatorDirection
from Elevator_System.models.elevator import Elevator
from Elevator_System.models.request import ElevatorCallRequest, ElevatorDropRequest


class ElevatorPriorityQueue:
    def __init__(self, elevator: Elevator):
        # as a queue: pop from last
        self.elevator: Elevator = elevator
        self._call_request_queue: Dict[ElevatorDirection, List[ElevatorCallRequest]] = {
            ElevatorDirection.UP: [],
            ElevatorDirection.DOWN: [],
        }
        self._drop_request_queue: List[ElevatorDropRequest] = []

    def call_is_empty(self, direction: ElevatorDirection):
        return not self._call_request_queue[direction]

    def drop_is_empty(self):
        return not self._drop_request_queue

    def is_empty(self):
        return (
            self.call_is_empty(ElevatorDirection.UP)
            and self.call_is_empty(ElevatorDirection.DOWN)
            and self.drop_is_empty()
        )
        #     self._call_request_queue[ElevatorDirection.UP]
        #     or self._call_request_queue[ElevatorDirection.DOWN]
        #     or self._drop_request_queue
        # )

    def insert_call_request(self, request: ElevatorCallRequest):
        self._call_request_queue[request.direction].append(request)

    def insert_drop_request(self, request: ElevatorDropRequest):
        self._drop_request_queue.append(request)
        # self.queue.append(item)

    def pop_call_request(self, direction: ElevatorDirection) -> ElevatorCallRequest:
        return self._call_request_queue[direction].pop()

    def pop_drop_request(self) -> ElevatorDropRequest:
        return self._drop_request_queue.pop()

    def top_call_request(self, direction: ElevatorDirection):
        return self._call_request_queue[direction][-1]

    def top_drop_request(self):
        return self._drop_request_queue[-1]

    def sort_call_requests(self, direction: ElevatorDirection):
        self._call_request_queue[direction].sort(
            reversed=direction == ElevatorDirection.UP,
            key=lambda x: (x.src_floor - self.elevator.current_floor.floor_number)
            % self.elevator_controller.floor_cnt,
        )

    def sort_drop_requests(self):
        self._drop_request_queue.sort(
            reverse=self.elevator.direction == ElevatorDirection.UP,
            key=lambda x: (x.dst_floor - self.elevator.current_floor.floor_number)
            % self.elevator_controller.floor_cnt,
        )

    def next_floor(self, direction: ElevatorDirection) -> bool:
        # if direction == ElevatorDirection.UP:
        #     return not self.call_is_empty(direction)

        return (
            direction == ElevatorDirection.UP
            and (
                (
                    (not self.call_is_empty(direction))
                    and self.top_call_request(direction).src_floor
                    > self.elevator.current_floor.floor_number
                )
                or (
                    (not self.drop_is_empty())
                    and self.top_drop_request().dst_floor
                    > self.elevator.current_floor.floor_number
                )
            )
        ) or (
            direction == ElevatorDirection.DOWN
            and (
                (
                    (not self.call_is_empty(direction))
                    and self.top_call_request(direction).src_floor
                    < self.elevator.current_floor.floor_number
                )
                or (
                    (not self.drop_is_empty(direction))
                    and self.top_drop_request().dst_floor
                    < self.elevator.current_floor.floor_number
                )
            )
        )
