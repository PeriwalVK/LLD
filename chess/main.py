from __future__ import annotations

import sys
import os


""" Get the absolute path of the folder containing main.py """
root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # path/to/project_root

""" Add that folder to the list of places Python looks for modules """
if root_folder not in sys.path:
    sys.path.insert(0, root_folder) # adds root_folder to start of sys.path list, so it gets prioritised


# for path in sys.path:
#     print(path)


from chess.models.game_center import Game
from chess.utils import SquareUtil


if __name__ == "__main__":
    g = Game()
    g.initialise()
    g.play()
    