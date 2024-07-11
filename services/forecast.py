import io
import os
import pickle

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import MaxNLocator
from sklearn.metrics import mean_squared_error

import config
from config import MODELS_DIR
from services.tools import slugify


def load_data(product_name: str) -> pd.DataFrame:
    """
    From csv with all data get data for product_name
    """
    data = pd.read_csv(config.DATA_FILE_PATH)
    product_mapping = {slugify(prod): prod for prod in data["Product"].unique()}
    original_product_name = product_mapping.get(product_name)
    if original_product_name is None:
        raise ValueError(f"No product found matching '{product_name}'")
    product_data = data[data["Product"] == original_product_name].sort_values(by="Date")
    return product_data


def constrain_forecast(original, forecast, max_change=0.05) -> list:
    """
    Limit predictions to a certain threshold
    """
    constrained = [original.iloc[-1]]
    for f in forecast:
        change = (f - constrained[-1]) / constrained[-1]
        if abs(change) > max_change:
            new_value = constrained[-1] * (1 + max_change * np.sign(change))
        else:
            new_value = f
        constrained.append(new_value)
    return constrained[1:]


def get_model_dict(product_name: str) -> dict:
    """
    Load model from disk and return it as a dictionary
    """
    model_filename = f"{slugify(product_name)}.pkl"
    model_path = os.path.join(MODELS_DIR, model_filename)
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    return model


def calculate_rmse(model, data) -> float:
    in_sample_forecast = model.fittedvalues
    min_length = min(len(data["Price"]), len(in_sample_forecast))
    return mean_squared_error(
        data["Price"][-min_length:], in_sample_forecast[-min_length:], squared=False
    )


def create_forecast_plot(
    data, forecast_dates, forecast, product_name, train_mae, test_mae, rmse
) -> io.BytesIO:
    plt.figure(figsize=(14, 7))
    plt.plot(data["Date"], data["Price"], label="Historical Data", marker="o")
    plt.plot(forecast_dates, forecast, label="Forecast", linestyle="--", marker="o")
    plt.axhline(y=100, color="g", linestyle="--", label="100%")
    plt.legend()
    plt.title(f"Price Forecast for {product_name}")
    plt.xlabel("Date")
    plt.ylabel("Price Index")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.text(
        0.02,
        0.98,
        f"Train MAE: {train_mae:.2f}\nTest MAE: {test_mae:.2f}\nRMSE: {rmse:.2f}",
        transform=plt.gca().transAxes,
        verticalalignment="top",
        fontsize=15,
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
    )
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()
    return buf
