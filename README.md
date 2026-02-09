<!-- python -m chess.main -->

## (1) add below to .vscode/settings.json file
    {
      "python.analysis.extraPaths": [
        "./",
      ],
      "python.analysis.autoImportCompletions": true
    }

## (2) Add this to top of every lld project's main file (ex: chess/main.py, tictactoe/main.py) 
==> it adds project root folder to sys path to handle relative imports 

    import sys
    import os

     
    """ Get the absolute path of the folder containing main.py """
    root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # path/to/project_root

    """ Add that folder to the list of places Python looks for modules """
    if root_folder not in sys.path:
        sys.path.insert(0, root_folder) 
        # adds root_folder to start of sys.path list,
        # so it gets prioritised
