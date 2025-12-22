from typing import Tuple

from chess.exceptions import Invalid_Square_Name_Exception, Invalid_Square_Position_Exception


class SquareUtil:

    def square_name_to_position(square_name: str) -> Tuple[int,int]:
        square_name = square_name.lower()

        # if len(square_name) !=2:
        #     raise Invalid_Square_Name_Exception(f"invalid square_name: must of of length 2")
        
        file, rank = square_name[0], square_name[1]
        # if file not in "abcdefgh":
        #     raise Invalid_Square_Name_Exception(f"invalid square_name: invalid file {file}")
        # if rank not in "12345678":
        #     raise Invalid_Square_Name_Exception(f"invalid square_name: invalid rank {rank}")
        
        return 8-int(rank), ord(file)-ord("a")

    def position_to_square_name(row: int, col: int) -> str:
        if row < 0 or row > 7 or col < 0 or col > 7:
            raise Invalid_Square_Position_Exception(f"invalid position: {row}, {col} is not a valid position")
        
        return chr(ord("a")+col) + str(8-row)

