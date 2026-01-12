import sys
import os



""" Get the absolute path of the folder containing main.py """
root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # path/to/project_root

""" Add that folder to the list of places Python looks for modules """
if root_folder not in sys.path:
    sys.path.insert(0, root_folder) 
    # adds root_folder to start of sys.path list, so it gets prioritised while looking at imports


if __name__ == "__main__":
    from logging_system.models.logger import Logger 

    logger = Logger()
    print("")
    
    logger.info("This is info")
    print("")
    
    logger.error("This is error")
    print("")
    
    logger.debug("This is debug")
    print("")
    
    logger.fatal("This is fatal")
    print("")