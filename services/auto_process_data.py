import os

import pandas as pd

import config
from services.clean_data import clean_data, wide_to_long
from services.download_data import download_data_sheet, xlsx_to_csv
from services.generate_models import split_data, make_forecast
from services.tools import ensure_directory_exists_and_writable


def auto_process_data(data_download_url: str = None) -> None:
    """
    Combined script to download/read data, clean it and generate models.

    :param data_download_url: Rosstat data sheet url. Default is at config.py.
        If this parameter is None, the script will try to load data from the data dir.
    """

    # Get data either from web or from disk
    if data_download_url is not None:
        file_path_xlsx = download_data_sheet(data_download_url, config.DATA_DIR)
        file_path_csv = xlsx_to_csv(file_path_xlsx)

        print(f"Data downloaded to {file_path_csv}")  # logger.info
    else:
        file_path_csv = config.DATA_FILE_PATH

    # Clean and process the data
    df = clean_data(file_path_csv)
    df_long = wide_to_long(df)

    # file_path = os.path.join(config.DATA_DIR, f"train_data_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.csv")
    file_path = os.path.join(config.DATA_FILE_PATH)
    df_long.to_csv(file_path)

    print(f"Data cleaned and saved to {file_path}")  # logger.info

    df = pd.read_csv(
        file_path, index_col=0, dtype={"Price": float}, parse_dates=["Date"]
    )
    dev_data, test_data = split_data(df, 0.15)
    products = dev_data["Product"].unique()

    # Prepare directory
    ensure_directory_exists_and_writable(config.MODELS_DIR)

    for product in products:
        print(f"Creating model for product {product}")  # logger.info
        make_forecast(
            product,
            dev_data,
            test_data,
            use_train_test_split=True,
            save_model=True,
            show_plot=False,
        )
