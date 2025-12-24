from __future__ import annotations

from collections import deque
import random
from typing import TYPE_CHECKING, List

from snake_and_food.constants import Direction, Symbol
from snake_and_food.models.cells import Cell
if TYPE_CHECKING:
    from snake_and_food.models.game import Game


class Board:
    def __init__(self, game: Game, rows: int, cols: int, walled:bool):
        self.game: Game = game
        self.game_rows: int = rows
        self.game_cols: int = cols

        self.grid_rows: int = rows+2
        self.grid_cols: int = cols+2
        self.walled: bool = walled

        self.grid: List[List[Cell]] = [[Cell(i,j) for j in range(self.grid_cols)] for i in range(self.grid_rows)]
        
        self.food: Cell = None
        self.snake: List[Cell] = deque()
        self.snake_dir: Direction = Direction.RIGHT

    

        
    def initialise(self):
        border_symbol = Symbol.HARD_WALL if self.walled else Symbol.TRANSPARENT_WALL

        for i in range(self.grid_rows):
            self.grid[i][0].set_symbol(border_symbol)
            self.grid[i][self.grid_cols - 1].set_symbol(border_symbol)
        for j in range(self.grid_cols):
            self.grid[0][j].set_symbol(border_symbol)
            self.grid[self.grid_rows - 1][j].set_symbol(border_symbol)
        
        self.grid[1][1].set_symbol(Symbol.SNAKE_HEAD)
        self.snake.append(self.grid[1][1])
        self.snake_dir = Direction.RIGHT
    
    def display(self):
        for row in self.grid:
            print(''.join([str(cell) for cell in row]))
    
    
    def generate_food(self):
        if self._no_food_left():
            # for each in random.sample(range(self.game_rows * self.game_cols),self.game_rows * self.game_cols):
            #     game_row, game_col = (each // self.game_cols, each % self.game_cols)
            #     if self.grid[game_row + 1][game_col + 1].get_symbol() == Symbol.EMPTY:
            #         self.grid[game_row + 1][game_col + 1].set_symbol(Symbol.FOOD)
            #         self.food = self.grid[game_row + 1][game_col + 1]
            #         return

            for row in random.sample(range(self.game_rows), self.game_rows):
                for col in random.sample(range(self.game_cols), self.game_cols):
                    # game_row, game_col = (each // self.game_cols, each % self.game_cols)
                    if self.grid[row + 1][col + 1].get_symbol() == Symbol.EMPTY:
                        self.grid[row + 1][col + 1].set_symbol(Symbol.FOOD)
                        self.food = self.grid[row + 1][col + 1]
                        return
            
            self.game.mark_game_over("NO PLACE LEFT FOR NEW FOOD")
            

            
    
    def _get_snake_head(self) -> Cell:
        return self.snake[-1]
    
    def _get_snake_next_cell(self) -> Cell:
        snake_head = self._get_snake_head()

        if self.snake_dir == Direction.UP:
            r,c = snake_head.row - 1, snake_head.col
            if not self.walled and self.grid[r][c].get_symbol() == Symbol.TRANSPARENT_WALL:
               r = self.grid_rows - 2 
        
        elif self.snake_dir == Direction.DOWN:
            r,c = snake_head.row + 1, snake_head.col
            if self.grid[r][c].get_symbol() == Symbol.TRANSPARENT_WALL:
               r = 1 
        elif self.snake_dir == Direction.LEFT:
            r,c = snake_head.row, snake_head.col - 1
            if self.grid[r][c].get_symbol() == Symbol.TRANSPARENT_WALL:
               c = self.grid_cols - 2 
        else: # self.snake_dir == Direction.RIGHT
            r,c = snake_head.row, snake_head.col + 1
            if self.grid[r][c].get_symbol() == Symbol.TRANSPARENT_WALL:
               c = 1
        
        return self.grid[r][c]
        
    
    def _can_move_snake(self) -> bool:
        return self._get_snake_next_cell().get_symbol() in [Symbol.EMPTY, Symbol.FOOD]
    
    def _no_food_left(self) -> bool:
        return self.food == None
             
        
    def move_snake(self): # move the snake
        if self._can_move_snake():
            next_cell = self._get_snake_next_cell()

            curr_head = self._get_snake_head()
            curr_head.set_symbol(Symbol.SNAKE_BODY)
            
            if next_cell.get_symbol() == Symbol.FOOD:
                self.game.increase_score(1)
                self.food = None
            else:
                popped_cell = self.snake.popleft()
                popped_cell.set_symbol(Symbol.EMPTY)
            
            
            next_cell.set_symbol(Symbol.SNAKE_HEAD)
            self.snake.append(next_cell)

        else:
            self.game.mark_game_over()
    

    def set_snake_dir(self, direction: Direction):
        self.snake_dir = direction

        
            

        




    

        