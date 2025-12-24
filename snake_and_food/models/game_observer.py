from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from snake_and_food.models.game import Game


class GameObserver:
    def __init__(self, subject: Game):
        self.subject = subject

    def on_move_made(self):
        print(f"GameObserver: move_made: snake moved one step {self.subject.board.snake_dir.name}")

    def on_game_over(self):
        print("GameObserver: game over")
    
    def on_score_changed(self):
        print(f"GameObserver: score changed to {self.subject.score}")
    