# This file contains little helper function
from typing import Optional
import requests
import hashlib
from pathlib import Path
from plisetl.log import get_logger
from plisetl.config import Config

config = Config()


def download_file(url: str) -> bytes:
    """Download a file as bytes

    Args:
        url (str): _description_

    Returns:
        bytes: _description_
    """
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


def pseudonymize_value_to_int(value: str | int | float, length=16) -> int:
    return (
        int(
            hashlib.sha256(
                (str(value) + config.PSEUDONYMIZATION_SECRET).encode("utf-8")
            ).hexdigest(),
            base=16,
        )
        % 10**length
    )


def pseudonymize_value_to_str(
    value: str | int | float, length=16, prefix: Optional[str] = ""
) -> str:
    """_summary_

    Args:
        value (str | int | float): The value to be pseudonymized
        length (int, optional): _description_. Defaults to 16.
        prefix (Optional[str], optional): A string that will be put in front of the pseudonymized value. That can be helpfull to identify the class/origin of the value. Defaults to "".

    Returns:
        str: _description_
    """
    return prefix + str(
        int(
            hashlib.sha256(
                (str(value) + config.PSEUDONYMIZATION_SECRET).encode("utf-8")
            ).hexdigest(),
            base=16,
        )
        % 10**length
    )
