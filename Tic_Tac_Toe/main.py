import sys
import os


""" Get the absolute path of the folder containing main.py """
root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # path/to/project_root

""" Add that folder to the list of places Python looks for modules """
if root_folder not in sys.path:
    sys.path.insert(0, root_folder) 
    # adds root_folder to start of sys.path list, so it gets prioritised while looking at imports



from Tic_Tac_Toe.models.game_center import TicTacToeGame

if __name__ == "__main__":
    game = TicTacToeGame()
    game.play()

    