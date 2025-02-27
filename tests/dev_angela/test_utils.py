import os
import sys
from pathlib import Path

if __name__ == "__main__":
    # Get the directory where this main module is located
    MODULE_DIR = Path(Path(__file__).parent.parent.parent, "src/plisetl")

    # Get the parent directory of the script (one level up)
    MODULE_PARENT_DIR = MODULE_DIR.parent.absolute()

    # Add the parent directory to Python's search path for modules
    # This allows us to import local modules when running the script
    sys.path.insert(0, os.path.normpath(MODULE_PARENT_DIR))

from plisetl.utils import download_file, write_bytes_to_file


downloaded_file_content = download_file(
    "https://cloud.apps.dzd-ev.org/s/S8AnkZLA8n7XaKQ/download"
)
write_bytes_to_file(downloaded_file_content, Path(Path(__file__).parent, "test.md"))
