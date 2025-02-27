import os
import sys
from pathlib import Path

dot_env_file_path = Path(Path(__file__).parent, "test_care_sites.env")
os.environ["PLIS_ETL_DOT_ENV_FILE"] = str(dot_env_file_path.resolve())

if __name__ == "__main__":
    # Get the directory where this main module is located
    MODULE_DIR = Path(Path(__file__).parent.parent.parent, "src/plisetl")

    # Get the parent directory of the script (one level up)
    MODULE_PARENT_DIR = MODULE_DIR.parent.absolute()

    # Add the parent directory to Python's search path for modules
    # This allows us to import local modules when running the script
    sys.path.insert(0, os.path.normpath(MODULE_PARENT_DIR))

from plisetl.main import run
from plisetl.database.caresite_crud import CaresideCRUD
from plisetl.database.person_crud import PersonCRUD

# clean database
CaresideCRUD().truncate_table(table_not_exists_ok=True)
PersonCRUD().truncate_table(table_not_exists_ok=True)

# run actual ETL proces
run()
