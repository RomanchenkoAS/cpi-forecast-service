import os

import pandas as pd
import requests

import config
from services.tools import ensure_directory_exists_and_writable, parse_dates


def download_data_sheet(url: str, path: str = config.DATA_DIR) -> str:
    """
    Download stats sheet from Rosstat website

    :param url: Rosstat file download URL
    :param path: Path to download directory, by default set to DATA_DIR from config.py
    :return: Path to downloaded file
    """
    ensure_directory_exists_and_writable(path)

    response = requests.get(url, stream=True)

    if response.status_code != 200:
        raise RuntimeError(
            f"Failed to download file. Status code: {response.status_code}"
        )

    file_path = os.path.join(config.DATA_DIR, "data.xlsx")

    # Open the file in binary write mode
    with open(file_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)

    print(f"File downloaded successfully and saved to {file_path}")

    return file_path


def xlsx_to_csv(xlsx_file_path: str) -> str:
    """
    Turn multiple xlsx sheets into one csv file
    :param xlsx_file_path: Path to xlsx file
    :return: Path to converted file
    """

    xls = pd.ExcelFile(xlsx_file_path)
    sheet_names = xls.sheet_names

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
    filename = os.path.join(config.DATA_DIR, "data.csv")
    combined_df.to_csv(filename)
    print(f"Combined data saved successfully to {filename}")

    return filename


def main():
    data_download_url = config.ROSSTAT_CPI_DATA_URL

    file_path_xlsx = download_data_sheet(data_download_url, config.DATA_DIR)
    file_path_csv = xlsx_to_csv(file_path_xlsx)

    print(f"Data downloaded to {file_path_csv}")


if __name__ == "__main__":
    main()
