from Elevator_System.constants import ElevatorDirection


class ElevatorselectionUtils:
    # def cost_to_move(self, src_floor_number: int, dest_floor_number: int, direction: str) -> int:
    #     return abs(src_floor_number - dest_floor_number)
    def cost_to_move(
        src_floor_number: int, dst_floor_number: int, curr_direction: ElevatorDirection
    ):
        priority = [
            curr_direction,
            ElevatorDirection.IDLE,
            ElevatorDirection.DOWN
            if curr_direction == ElevatorDirection.UP
            else ElevatorDirection.UP,
        ]
        if curr_direction == ElevatorDirection.UP:
            return src_floor_number - dst_floor_number
        elif curr_direction == ElevatorDirection.DOWN:
            return dst_floor_number - src_floor_number
        else:  # ElevatorDirection.IDLE
            return abs(dst_floor_number - src_floor_number)
