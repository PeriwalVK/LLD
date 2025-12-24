from snake_and_food.constants import Direction, GameStatus
from snake_and_food.models.board import Board
from snake_and_food.models.game_observer import GameObserver


class Game:
    def __init__(self, rows: int, cols: int, walled:bool=False):
        
        self.board: Board = Board(self, rows, cols, walled=walled)

        self.score: int = 0
        self.game_status: GameStatus = GameStatus.IDLE
        self.observers = []

    def register_observer(self, game_observer: GameObserver):
        self.observers.append(game_observer)

    def notify_move_made(self):
        for observer in self.observers:
            observer.on_move_made()
    
    def notify_game_over(self):
        for observer in self.observers:
            observer.on_game_over()
    
    def notify_score_changed(self):
        for observer in self.observers:
            observer.on_score_changed()

    def initialise(self):
        self.board.initialise()
        self.game_status = GameStatus.IN_PROGRESS
    
    def display_board(self):
        self.board.display()

    def increase_score(self, by:int=1):
        self.score += by
        self.notify_score_changed()

    def mark_game_over(self, msg:str=None):
        if msg:
            print(msg)
        self.game_status = GameStatus.GAME_OVER
        self.notify_game_over()
    
    def is_game_over(self):
        return self.game_status == GameStatus.GAME_OVER
    
    def fetch_direction(self) -> Direction:
        dir = input("enter direction [W: UP, A: LEFT, S: DOWN, D: RIGHT]: ").upper()
        # print(f"entered sdirection is '{dir}'")
        if dir not in ["", "W", "A", "S", "D"]:
            print("INVALID DIRECTION, try again...")
            return self.fetch_direction()
        return self.board.snake_dir if dir == "" else Direction(dir)
    
    def make_move(self):
        self.board.set_snake_dir(self.fetch_direction())
        self.board.move_snake()
        self.notify_move_made()

    def play(self):
        self.board.generate_food()
        while not self.is_game_over():
            self.display_board()
            self.make_move()
            self.board.generate_food()
        
        self.display_board()
        print(f"GAME OVER: your score is {self.score}")
    

        