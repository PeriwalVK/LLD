from ast import Dict
from typing import List
from Elevator_System.constants import (
    BuildingConstants,
    ElevatorDirection,
    ElevatorStatus,
)
from Elevator_System.models.controllers.elevator_controller import ElevatorController
from Elevator_System.models.door import Door
from Elevator_System.models.floor import Floor
from Elevator_System.models.queue import ElevatorPriorityQueue
from Elevator_System.models.request import ElevatorCallRequest, ElevatorDropRequest


def cost_function(
    src_floor_no: int, dst_floor_no: int, curr_direction: ElevatorDirection
):
    if curr_direction == ElevatorDirection.UP:
        same_dir_cost = -1 if dst_floor_no > src_floor_no else 1
        distance_cost = (-1) * same_dir_cost * abs(src_floor_no - dst_floor_no)
        return (same_dir_cost, distance_cost)
    elif curr_direction == ElevatorDirection.DOWN:
        same_dir_cost = -1 if src_floor_no > dst_floor_no else 1
        distance_cost = (-1) * same_dir_cost * abs(src_floor_no - dst_floor_no)
        return (same_dir_cost, distance_cost)
    else:  # ElevatorDirection.IDLE
        same_dir_cost = 0
        distance_cost = abs(src_floor_no - dst_floor_no)
        return (same_dir_cost, distance_cost)


class Elevator:
    # def __init__(self, id: int, floors_dict: Dict[int, Floor]):
    def __init__(self, id: int, elevator_controller: ElevatorController):
        self.id: int = id
        # self.floors_dict: Dict[int, Floor] = floors_dict
        self.elevator_controller: ElevatorController = elevator_controller

        # self.door: Door = Door()
        # self.min_floor: Floor = floors_dict[BuildingConstants.MIN_FLOOR]
        # self.max_floor: Floor = floors_dict[BuildingConstants.MAX_FLOOR]
        self.current_floor: Floor = self.elevator_controller.floors_dict.values()[
            0
        ].floor_number

        self.direction: ElevatorDirection = ElevatorDirection.IDLE
        self.status: ElevatorStatus = ElevatorStatus.IDLE

        # self._offset = (-1)*BuildingConstants.MIN_FLOOR

        # # as a queue: pop from last
        # self._call_request_queue: Dict[ElevatorDirection, List[ElevatorCallRequest]] = {
        #     ElevatorDirection.UP: [],
        #     ElevatorDirection.DOWN: [],
        # }
        # self._drop_request_queue: List[ElevatorDropRequest] = []

        self._queue = ElevatorPriorityQueue(self)

        # self.requests: Dict[ElevatorDirection, List[ElevatorDropRequest]] = {
        #     ElevatorDirection.UP: [],
        #     ElevatorDirection.DOWN: []
        # }
        # self.requests: List[bool] = [False for _ in range(BuildingConstants.MIN_FLOOR, BuildingConstants.MAX_FLOOR + 1)]

    # def next_move(self) -> Floor:
    #     if self.direction == ElevatorDirection.UP:
    #         self.current_floor = self.current_floor.floor_number + 1
    #     elif self.direction == ElevatorDirection.DOWN:
    #         self.current_floor = self.current_floor.floor_number - 1

    # def get_next_floor(self) -> ElevatorDropRequest:
    #     if self.requests[self.direction]:
    #         next = self.requests[self.direction][-1]
    #         if (self.direction == ElevatorDirection.UP and next.dst_floor > self.current_floor.floor_number) or (self.direction == ElevatorDirection.DOWN and next.dst_floor > self.current_floor.floor_number):
    #             return self.requests[self.direction].pop()
    #     else:
    #         return None

    # def add_request(self, request: ElevatorRequest):
    #     self.requests[request.direction].append(request)
    #     self._sort_requests()

    # def no_requests(self) -> bool:
    #     return not any(self.requests)

    def run(self):
        while not self._queue.is_empty():
            self._process_requests()

    def _process_requests(self):
        # if self._call_requests[ElevatorDirection.UP] or self._call_requests[ElevatorDirection.DOWN] or self._drop_requests:
        self._process_up_requests()
        self._process_down_requests()

    def _process_up_requests(self):
        while self._queue.next_floor(ElevatorDirection.UP):
            self.direction = ElevatorDirection.UP
            self._step(ElevatorDirection.UP)
            # go to floor

        self.status = ElevatorStatus.IDLE

    def _process_down_requests(self):
        while self._queue.next_floor(ElevatorDirection.DOWN):
            self.direction = ElevatorDirection.DOWN
            self._step(ElevatorDirection.DOWN)
            # go to floor

        self.status = ElevatorStatus.IDLE

    # def _next_floor(self, direction: ElevatorDirection) -> bool:
    #     return (
    #         direction == ElevatorDirection.UP
    #         and (
    #             (
    #                 self._call_request_queue[direction][-1].src_floor
    #                 > self.current_floor.floor_number
    #             )
    #             or (
    #                 self._drop_request_queue[-1].dst_floor
    #                 > self.current_floor.floor_number
    #             )
    #         )
    #     ) or (
    #         direction == ElevatorDirection.DOWN
    #         and (
    #             (
    #                 self._call_request_queue[direction][-1].src_floor
    #                 < self.current_floor.floor_number
    #             )
    #             or (
    #                 self._drop_request_queue[-1].dst_floor
    #                 < self.current_floor.floor_number
    #             )
    #         )
    #     )

    def _step(self, direction: ElevatorDirection):
        if direction == ElevatorDirection.UP:
            self.current_floor = self.current_floor.floor_number + 1
        elif direction == ElevatorDirection.DOWN:
            self.current_floor = self.current_floor.floor_number - 1
        
        if not self._queue.call_is_empty() and self._queue.top_call_request(direction).src_floor == self.current_floor.floor_number:
            self._queue.pop_call_request(direction)
        if not self._queue.drop_is_empty() and self._queue.top_drop_request().dst_floor == self.current_floor.floor_number:
            self._queue.pop_drop_request()
            # self.status = ElevatorStatus.IDLE

    def assign_external_request(self, request: ElevatorCallRequest):
        self._call_request_queue[request.direction].append(request)
        self._sort_call_requests(request.direction)

    def press_button(self, dst_floor_number: int):
        self._queue.insert_drop_request(ElevatorDropRequest(dst_floor_number))
        self._queue.sort_drop_requests()
        # self._drop_request_queue.append(ElevatorDropRequest(dst_floor_number))
        # self._sort_drop_requests()

    # def _sort_call_requests(self, direction: ElevatorDirection):
    #     # if direction == ElevatorDirection.UP:
    #     self._call_request_queue[direction].sort(
    #         reversed=direction == ElevatorDirection.UP,
    #         key=lambda x: (x.src_floor - self.current_floor.floor_number)
    #         % self.elevator_controller.floor_cnt,
    #     )
    #     # else: # ElevatorDirection.DOWN
    #     #     self._call_requests[direction].sort(
    #     #         key=lambda x: (x.src_floor - self.current_floor.floor_number)%self.elevator_controller.floor_cnt
    #     #     )

    # def _sort_drop_requests(self):
    #     self._drop_request_queue.sort(
    #         reverse=self.direction == ElevatorDirection.UP,
    #         key=lambda x: (x.dst_floor - self.current_floor.floor_number)
    #         % self.elevator_controller.floor_cnt,
    #     )

    # def _sort_requests(self):
    #     # multiplier = -1 if self.direction == ElevatorDirection.UP else 1

    #     # for direction in self.requests.keys():
    #     for direction in [ElevatorDirection.UP, ElevatorDirection.DOWN]:
    #         self.requests[direction].sort(
    #             reversed=True,
    #             key=lambda x: cost_function(x.src_floor, x.dst_floor, direction),
    #         )
