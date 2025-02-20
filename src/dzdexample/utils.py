# This file contains little helper function

import requests
from pathlib import Path
from dzdexample.log import get_logger
from dzdexample.config import Config


def download_file(url: str) -> bytes:
    # Connect to the url
    response = requests.get(url)
    # Check for errors while download
    response.raise_for_status()
    # return content
    return response.content


def write_bytes_to_file(content: bytes, target_file_path: str | Path) -> Path:
    target_file_path = Path(target_file_path)
    # create dirctory of target file
    target_file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(target_file_path, "wb") as file_object:
        file_object.write(content)
