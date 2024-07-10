import os
import re
import stat
from datetime import date, datetime

import pandas as pd


def parse_dates(date_str: str, year: int) -> date:
    """
    Parse date string in format YYYY-MM-DD from vintage's column title
    Each vintage have a date in format like 'на 16 января'
    """

    # Clean string
    date_str = date_str.replace("*", "").lstrip("на ")

    month_mapping = {
        "января": 1,
        "февраля": 2,
        "марта": 3,
        "апреля": 4,
        "мая": 5,
        "июня": 6,
        "июля": 7,
        "августа": 8,
        "сентября": 9,
        "октября": 10,
        "ноября": 11,
        "декабря": 12,
    }

    parts = date_str.split()
    day = int(parts[0])
    month_name = parts[1]

    month = month_mapping[month_name]

    date_obj = datetime(year, month, day).date()

    return date_obj


def transliterate(name):
    """
    Автор: LarsKort
    Дата: 16/07/2011; 1:05 GMT-4;
    https://gist.github.com/ledovsky/6398962
    """
    # Слоаврь с заменами
    dictionary = {
        "а": "a",
        "б": "b",
        "в": "v",
        "г": "g",
        "д": "d",
        "е": "e",
        "ё": "e",
        "ж": "zh",
        "з": "z",
        "и": "i",
        "й": "i",
        "к": "k",
        "л": "l",
        "м": "m",
        "н": "n",
        "о": "o",
        "п": "p",
        "р": "r",
        "с": "s",
        "т": "t",
        "у": "u",
        "ф": "f",
        "х": "h",
        "ц": "c",
        "ч": "cz",
        "ш": "sh",
        "щ": "scz",
        "ъ": "",
        "ы": "y",
        "ь": "b",
        "э": "e",
        "ю": "u",
        "я": "ja",
    }

    # Циклически заменяем все буквы в строке
    for key in dictionary:
        name = name.replace(key, dictionary[key])
    return name


def slugify(word: str) -> str:
    """
    Converts to lowercase, removes non-word characters (alphanumerics and underscores)
    and converts spaces to hyphens. Also strips leading and trailing whitespace.

    :param word: Cyrillic word string
    """
    word = transliterate(word.lower())
    word = re.sub(r"[^\w\s-]", "", word).strip()
    word = re.sub(r"[-\s]+", "-", word)
    return word


def ensure_directory_exists_and_writable(dir_path: str):
    """
    Ensure that the directory at the given path exists and is writable.
    If the directory exists but is not writable, modify its permissions.

    :param dir_path: Path to the directory
    """
    # Check if the directory exists
    if not os.path.exists(dir_path):
        try:
            # Create the directory
            os.makedirs(dir_path)
            print(f"Directory '{dir_path}' created.")  # logger.info
        except Exception as e:
            raise PermissionError(f"Unable to create directory '{dir_path}': {e}")

    # Check if the directory is writable
    if not os.access(dir_path, os.W_OK):
        try:
            # Modify directory permissions to be writable
            os.chmod(dir_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
            print(f"Permissions of directory '{dir_path}' have been modified to be writable.")  # logger.info
        except Exception as e:
            raise PermissionError(f"Unable to modify permissions of directory '{dir_path}': {e}")

    if os.access(dir_path, os.W_OK):
        print(f"Directory '{dir_path}' is writable.")  # logger.info
    else:
        raise PermissionError(f"Directory '{dir_path}' is not writable after attempting to modify permissions.")


# def read_csv(file_name: str) -> pd.DataFrame:
#     """
#     Read csv file to dataframe
#     """
#     if not os.path.isfile(file_name):
#         raise RuntimeError(f"The file '{file_name}' does not exist.")
#
#     df = pd.read_csv(file_name)
#     return df


def print_full_df(df: pd.DataFrame) -> None:
    """
    Configure pandas to display dataframe in full.
    """
    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", None)
    print(df)
