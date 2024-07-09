import os

import pandas as pd
import requests
from tools import parse_dates

import config


def ensure_directory_exists(directory_path):
    """
    Ensure that the directory at the given path exists. If it does not exist, create it.

    :param directory_path: Path to the directory
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Directory {directory_path} created.")
    else:
        print(f"Directory {directory_path} already exists.")


def get_data(url: str, path: str) -> None:
    """
        Download stats sheet from Rosstat website
    """
    if not os.path.isdir(config.DATA_DIR):
        os.makedirs(config.DATA_DIR)

    response = requests.get(url, stream=True)

    if response.status_code != 200:
        raise RuntimeError(f"Status code {response.status_code}")

    file_path = os.path.join(config.DATA_DIR, url.split("/")[-1])

    # Open the file in binary write mode
    with open(file_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)

    print(f"File downloaded successfully and saved to {file_path}")


def main():
    URL = config.ROSSTAT_CPI_DATA_URL
    FILEPATH = os.path.join(config.DATA_DIR, "data.xlsx")

    get_data(URL, FILEPATH)

if __name__ == "__main__":
    main()