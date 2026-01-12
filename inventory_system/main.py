import os
import sys


root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if root_folder not in sys.path:
    sys.path.insert(0, root_folder)



if __name__ == "__main__":

    pass