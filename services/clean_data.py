import os

import pandas as pd

import config
from services.tools import print_full_df


def clean_data(file_name: str) -> pd.DataFrame:
    """
    Read csv, convert to DF and clean NaN's
    """
    if not os.path.isfile(file_name):
        raise RuntimeError(f"The file '{file_name}' does not exist.")

    # Read csv and coerce invalid values to NaN
    df = pd.read_csv(file_name, na_values=['...', '…'])

    # Clear NaN rows
    df.dropna(inplace=True)

    # print_full_df(df)
    return df


def wide_to_long(df: pd.DataFrame) -> pd.DataFrame:
    """
    Combine all dates from multiple columns into one
    """
    product_names = df.iloc[:, 0]
    price_data = df.iloc[:, 1:]

    # Convert the price data to a long format
    price_data_long = pd.melt(df, id_vars=['Наименование'], var_name='Date', value_name='Price')
    price_data_long.columns = ['Product', 'Date', 'Price']
    # Convert Date column to datetime format
    price_data_long['Date'] = pd.to_datetime(price_data_long['Date'], format='%Y-%m-%d')

    # Convert Price column to numeric, forcing errors to NaN
    price_data_long['Price'] = pd.to_numeric(price_data_long['Price'], errors='coerce')

    # Drop rows with NaN values in Price column
    price_data_long = price_data_long.dropna(subset=['Price'])

    return price_data_long


def main():
    file_name = os.path.join(config.DATA_DIR, 'data.csv')
    df = clean_data(file_name)
    df_long = wide_to_long(df)
    df_long.to_csv(os.path.join(config.DATA_DIR, 'train_data.csv'))


if __name__ == "__main__":
    main()
