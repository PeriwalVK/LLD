from __future__ import annotations

import sys
import os


""" Get the absolute path of the folder containing main.py """
root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # path/to/project_root

""" Add that folder to the list of places Python looks for modules """
if root_folder not in sys.path:
    sys.path.insert(0, root_folder) 
    # adds root_folder to start of sys.path list, so it gets prioritised while looking at imports


# for path in sys.path:
#     print(path)


from snake_and_food.models.game import Game
from snake_and_food.models.game_observer import GameObserver

if __name__ == "__main__":

    rows, cols = map(int, input("Enter rows and cols (separated by space): ").split())

    
    g = Game(rows, cols, walled=False)
    game_observer = GameObserver(g)
    g.register_observer(game_observer)
    g.initialise()
    g.play()
    # g.display_board()

    # g.board.generate_food()
    