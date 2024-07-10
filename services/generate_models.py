import os
import pickle
import warnings
from datetime import datetime
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error
from statsmodels.stats.stattools import medcouple
from statsmodels.tsa.holtwinters import ExponentialSmoothing

import config
from services.tools import slugify


def split_data(
        df: pd.DataFrame, split_coefficient: float = 0.15
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Split data into dev and test sets.
    Be careful, split may not very accurate because of data sampling.

    :param df: Input dataframe
    :param split_coefficient: Part of data that goes into dev part in %. Must be between 0 and 1.
    """

    e = 0.001
    if split_coefficient < e or split_coefficient > 1 - e:
        raise ValueError("Test coefficient must be between 0 and 1.")

    # Calculate the date to split the data
    total_days = (df["Date"].max() - df["Date"].min()).days
    split_date = df["Date"].min() + pd.DateOffset(
        days=int(total_days * (1 - split_coefficient))
    )

    # Split the data into development and testing sets based on the date
    dev_data = df[df["Date"] <= split_date]
    test_data = df[df["Date"] > split_date]

    # Verify the split
    print("Development data size:", len(dev_data))  # logger.info
    print("Testing data size:", len(test_data))  # logger.info

    return dev_data, test_data


def make_forecast(
        product_name: str,
        train_data: pd.DataFrame,
        test_data: pd.DataFrame,
        use_train_test_split: bool = True,
        save_model: bool = False,
        show_plot: bool = False,
) -> dict[str, Any]:
    """
    Create 6 months forecast models on provided data.

    :param product_name: Name of the product in "Product" column.
    :param train_data: Training data dataframe.
    :param test_data: Test data dataframe.
    :param use_train_test_split: Whether to use train and test splits or use whole dataset.
    :param save_model: Save trained model to .pkl.
    :param show_plot: Display forecast plot.
    :return: Dictionary with model and metadata.
    """

    # Filter out the specific warnings
    warnings.filterwarnings("ignore", message="No supported index is available.")
    warnings.filterwarnings(
        "ignore", message="An unsupported index was provided and will be"
    )

    test_mae = train_mae = None

    product_train_data = train_data[train_data["Product"] == product_name]
    product_test_data = test_data[test_data["Product"] == product_name]

    # Sort the data by date
    product_train_data = product_train_data.sort_values(by="Date")
    product_test_data = product_test_data.sort_values(by="Date")

    if use_train_test_split:
        # Use only training data for model fitting
        model = ExponentialSmoothing(
            product_train_data["Price"],
            trend="add",
            seasonal="add",
            seasonal_periods=12,
        )
        model_fit = model.fit()

        # In-sample forecast (on training data)
        in_sample_forecast = model_fit.fittedvalues

        # Out-of-sample forecast (on test data)
        out_of_sample_forecast = model_fit.forecast(steps=len(product_test_data))

        # Calculate evaluation metrics
        train_mae = mean_absolute_error(product_train_data["Price"], in_sample_forecast)
        test_mae = mean_absolute_error(
            product_test_data["Price"], out_of_sample_forecast
        )

        # print(f"Model {product_name} | Train MAE: {train_mae}")  # logger.info
        # print(f"Model {product_name} | Test MAE: {test_mae}")  # logger.info

        if show_plot:
            plt.figure(figsize=(14, 7))
            plt.plot(
                product_train_data["Date"],
                product_train_data["Price"],
                label="Training Data",
                marker="o",
            )
            plt.plot(
                product_test_data["Date"],
                product_test_data["Price"],
                label="Test Data",
                marker="o",
            )
            plt.plot(
                product_train_data["Date"],
                in_sample_forecast,
                label="In-sample Forecast",
                linestyle="--",
            )
            plt.plot(
                product_test_data["Date"],
                out_of_sample_forecast,
                label="Out-of-sample Forecast",
                linestyle="--",
            )
    else:
        # Use all data for model fitting
        combined_data = pd.concat([product_train_data, product_test_data]).sort_values(
            by="Date"
        )
        model = ExponentialSmoothing(
            combined_data["Price"], trend="add", seasonal="add", seasonal_periods=12
        )
        model_fit = model.fit()

        # In-sample forecast
        in_sample_forecast = model_fit.fittedvalues

        # Calculate evaluation metrics
        train_mae = mean_absolute_error(combined_data["Price"], in_sample_forecast)
        # print(f"Model {product_name} | In-sample MAE: {train_mae}")  # logger.info

        if show_plot:
            plt.figure(figsize=(14, 7))
            plt.plot(
                combined_data["Date"],
                combined_data["Price"],
                label="Historical Data",
                marker="o",
            )
            plt.plot(
                combined_data["Date"],
                in_sample_forecast,
                label="In-sample Forecast",
                linestyle="--",
            )

    # Forecast for the next 28 weeks
    forecast_horizon = 28
    last_date = (
        product_test_data["Date"].max()
        if use_train_test_split
        else combined_data["Date"].max()
    )
    forecast_dates = pd.date_range(
        start=last_date + pd.Timedelta(days=7), periods=forecast_horizon, freq="W"
    )
    forecast = model_fit.forecast(steps=forecast_horizon)

    # Calculate prediction intervals
    alpha = 0.05  # 95% confidence interval
    mean_squared_error = np.mean(model_fit.resid ** 2)
    standard_error = np.sqrt(mean_squared_error * (1 + np.arange(1, forecast_horizon + 1)))
    critical_value = 1.96  # Approximation for 95% CI (can use 1.645 for 90% CI)
    lower_ci = forecast - critical_value * standard_error
    upper_ci = forecast + critical_value * standard_error

    # Calculate average confidence interval width for forecast
    avg_ci_width_forecast = np.mean(upper_ci - lower_ci)
    max_ci_width_forecast = np.max(upper_ci - lower_ci)

    # Calculate in-sample confidence intervals
    residuals = model_fit.resid
    scale = np.median(np.abs(residuals - np.median(residuals)))
    mc = medcouple(residuals)
    z = 1.96  # for 95% confidence interval

    lower_in_sample_ci = in_sample_forecast - z * scale * np.exp(-mc * (residuals < 0))
    upper_in_sample_ci = in_sample_forecast + z * scale * np.exp(mc * (residuals > 0))

    # Calculate average confidence interval width for in-sample forecast
    avg_ci_width_in_sample = np.mean(upper_in_sample_ci - lower_in_sample_ci)
    max_ci_width_in_sample = np.max(upper_in_sample_ci - lower_in_sample_ci)

    if show_plot:
        # Plot future forecast
        print(f"Plotting for {product_name}")  # logger.info

        plt.plot(
            forecast_dates,
            forecast,
            label="Next 28 Weeks Forecast",
            linestyle="--",
            marker="o",
        )

        plt.legend()
        plt.title(f"Historical Data and Forecast for {product_name}")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    model_metadata = {
        "model": model_fit,
        "url": f"/forecast/{slugify(product_name)}",
        "product_name": product_name,
        "train_mae": train_mae if train_mae else None,
        "test_mae": test_mae if test_mae else None,
        "date_created": datetime.now(),
        # "forecast": forecast.tolist(),
        # "forecast_dates": [date.strftime('%Y-%m-%d') for date in forecast_dates],
        "avg_forecast_ci_width": float(avg_ci_width_forecast),
        "max_forecast_ci_width": float(max_ci_width_forecast),
        # "in_sample_forecast": in_sample_forecast.tolist(),
        # "in_sample_dates": [date.strftime('%Y-%m-%d') for date in in_sample_dates],
        "avg_in_sample_ci_width": float(avg_ci_width_in_sample),
        "max_in_sample_ci_width": float(max_ci_width_in_sample),
    }

    # Save the model
    if save_model:
        model_filename = f"{slugify(product_name)}.pkl"
        model_path = os.path.join(config.MODELS_DIR, model_filename)
        with open(model_path, "wb") as f:
            pickle.dump(model_metadata, f)

    return model_metadata


def main():
    file_name = os.path.join(config.DATA_DIR, "train_data.csv")
    df = pd.read_csv(
        file_name, index_col=0, dtype={"Price": float}, parse_dates=["Date"]
    )
    dev_data, test_data = split_data(df, 0.15)
    products = dev_data["Product"].unique()

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


if __name__ == "__main__":
    main()
