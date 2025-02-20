import os
import sys
from pathlib import Path

if __name__ == "__main__":
    # Get the directory where this script is located
    MODULE_DIR = Path(__file__).parent

    # Get the parent directory of the script (one level up)
    MODULE_PARENT_DIR = MODULE_DIR.parent.absolute()

    # Add the parent directory to Python's search path for modules
    # This allows us to import local modules when running the script
    sys.path.insert(0, os.path.normpath(MODULE_PARENT_DIR))

from dzdexample.database._connection import init_db

# Now we can import modules from our local project directory
from dzdexample.log import get_logger
from dzdexample.config import Config

config = Config()


def run():
    init_db()
