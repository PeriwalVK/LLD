

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Tuple
from chess.constants import Colour
from chess.exceptions import Invalid_Square_Name_Exception
from chess.models.board import Board
from chess.models.move import Move
from chess.utils import SquareUtil

class IPlayStrategy(ABC):
    @abstractmethod
    def calc_next_move(self, board: Board, colour: Colour) -> Move:
        pass

class HumanPlayStrategy(IPlayStrategy):

    def _is_valid_input(self, _input: str) -> bool:
        _input = _input.lower()
        verdict = len(_input) == 5 and _input[0] in "abcdefgh" and _input[1] in "12345678" and _input[2] in " -" and _input[3] in "abcdefgh" and _input[4] in "12345678" and _input[:2] != _input[3:]
        verdict = verdict or (len(_input) == 4 and _input[0] in "abcdefgh" and _input[1] in "12345678" and _input[2] in "abcdefgh" and _input[3] in "12345678" and _input[:2] != _input[2:])
        if not verdict:
            print("invalid input: enter valid input in the form `src-dst` (ex: `e2-e4`)")
        return verdict

    def _parse_square_names(self,_input: str) -> Tuple[str, str]:
        assert len(_input) in [4, 5]
        if len(_input) == 4:
            return _input[:2], _input[2:]
        else:
            return _input[:2], _input[3:]
        


    def _take_move_as_input(self, board: Board, colour: Colour) -> Move:
        while True:
            # try:
            _input = input(f"Enter {colour.value}'s move: ")
            if not self._is_valid_input(_input):
                continue

            src, dst = self._parse_square_names(_input)

            

            position_from: Tuple[int, int] = SquareUtil.square_name_to_position(src)
            position_to: Tuple[int, int] = SquareUtil.square_name_to_position(dst)

            return Move(
                board.get_square_at(*position_from),
                board.get_square_at(*position_to)
            )

            # except Invalid_Square_Name_Exception as e:
            #     print(e)
            #     print("retrying...")
            

        
    def calc_next_move(self, board: Board, colour: Colour) -> Move:
        move = self._take_move_as_input(board, colour)
        while not board.is_valid_move(move, colour):
            print("inside fetch next move ==> invalid move ")
            move = self._take_move_as_input(board, colour)
        
        return move

        

class PlayerFactory:
    human_play_strategy = HumanPlayStrategy()

    @staticmethod
    def get_player(name: str, colour: Colour, is_human: bool) -> Player:
        if is_human:
            return Player(name, colour, PlayerFactory.human_play_strategy)
        else:
            # TODO: Implement AIPlayStrategy
            raise NotImplementedError("AI player not yet implemented")


        


class Player:
    def __init__(self, name: str, colour: Colour, play_strategy: IPlayStrategy):
        self.name: str = name
        self.colour: Colour = colour
        self.play_strategy: IPlayStrategy = play_strategy
    
    def calc_next_move(self, board: Board) -> Move:
        return self.play_strategy.calc_next_move(board, self.colour)

        
    
