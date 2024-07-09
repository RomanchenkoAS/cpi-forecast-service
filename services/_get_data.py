import os

import pandas as pd
import requests
from tools import parse_dates

import config

URL = "https://rosstat.gov.ru/storage/mediabank/Nedel_ipc.xlsx"
FILENAME = "Nedel_ipc.xlsx"
FILEPATH = os.path.join(config.DATA_DIR, FILENAME)


def get_data(url: str) -> None:
    """Download stats sheet from Rosstat website"""
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


def xlsx_to_combined_data_csv(xlsx_file_path: str) -> pd.DataFrame:
    """Turn xlsx into dataframe"""
    xls = pd.ExcelFile(xlsx_file_path)
    sheet_names = xls.sheet_names

    pd.set_option("display.max_columns", 4)
    pd.set_option("display.expand_frame_repr", False)

    years = []

    for sheet_name in sheet_names[1:]:
        # Read the sheet into a DataFrame
        df_current = pd.read_excel(xlsx_file_path, sheet_name=sheet_name, skiprows=3)

        # Drop 'info' rows: where only first cell is filled
        df_current = df_current[~df_current.iloc[:, 1:].isna().all(axis=1)]

        # Transform str dates in header into datetime format
        new_headers = [df_current.columns[0]] + [
            parse_dates(str(header), int(sheet_name))
            for header in df_current.columns[1:]
        ]
        df_current.columns = new_headers

        years.append(df_current)

    combined_df = pd.concat([df.set_index("Наименование") for df in years], axis=1)
    combined_df.sort_index(inplace=True)
    filename = os.path.join(config.DATA_DIR, "train_data.csv")
    combined_df.to_csv(filename)
    print(f"Combined data saved successfully to {filename}")

    return combined_df


def xlsx_to_csv(xlsx_file_path: str) -> None:
    """Turn xlsx into csvs"""
    xls = pd.ExcelFile(xlsx_file_path)
    sheet_names = xls.sheet_names

    # Iterate over the sheet names, starting from the second sheet
    # First sheet is index page
    for sheet_name in sheet_names[1:]:
        csv_file_name = f"{sheet_name}.csv"
        csv_file_path = os.path.join(config.DATA_DIR, csv_file_name)

        # Read the sheet into a DataFrame
        df = pd.read_excel(xlsx_file_path, sheet_name=sheet_name, skiprows=3)

        # Drop 'info' rows: where only first cell is filled
        df = df[~df.iloc[:, 1:].isna().all(axis=1)]

        # Save the DataFrame to a .csv file
        df.to_csv(csv_file_path, index=False)

        print(f"File successfully converted and saved to {csv_file_path}")


def create_csvs() -> None:
    if not os.path.isfile(FILEPATH):
        print(f"The file '{FILENAME}' does not exist.")
        get_data(URL)

    xlsx_to_csv(FILEPATH)


def read_csvs(filename: str) -> pd.DataFrame:
    if not os.path.isfile(filename):
        raise RuntimeError(f"The file '{filename}' does not exist.")

    df = pd.read_csv(filename)
    print(df)
    return df


def compose_dataset():
    pass


if __name__ == "__main__":
    create_csvs()
    # read_csvs(os.path.join(config.DATA_DIR, "2024.csv"))

    # xlsx_to_dataframe(FILEPATH)

    xlsx_to_combined_data_csv(FILEPATH)