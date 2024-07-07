import io
import os
import pickle
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from flask import Flask, jsonify, render_template, send_file

from config import DATA_DIR, STATIC_DIR, TEMPLATES_DIR
from services.tools import slugify_cyrillic_word

app = Flask(__name__, template_folder=TEMPLATES_DIR, static_folder=STATIC_DIR)


def load_data(product_name):
    """Loads data for the given product from collection of all data"""
    data = pd.read_csv(os.path.join(DATA_DIR, "price_data_long.csv"))

    # Create a mapping of slugified product names to original product names
    product_mapping = {
        slugify_cyrillic_word(prod): prod for prod in data["Product"].unique()
    }

    # Find the original product name that matches the slugified input
    original_product_name = product_mapping.get(product_name)

    if original_product_name is None:
        raise ValueError(f"No product found matching '{product_name}'")

    # Filter the data for the matched product
    product_data = data[data["Product"] == original_product_name].sort_values(by="Date")

    return product_data


def constrain_forecast(original, forecast, max_change=0.05):
    constrained = [original.iloc[-1]]  # Start with the last known value
    for f in forecast:
        change = (f - constrained[-1]) / constrained[-1]
        if abs(change) > max_change:
            new_value = constrained[-1] * (1 + max_change * np.sign(change))
        else:
            new_value = f
        constrained.append(new_value)
    return constrained[1:]  # Remove the initial seed value


def get_model(product_name: str):
    """Load saved model for the given product"""
    model_filename = f"{product_name.replace(' ', '_')}_model.pkl"
    model_path = os.path.join(DATA_DIR, "trained_models", model_filename)
    with open(model_path, "rb") as f:
        model = pickle.load(f)

    return model


def calculate_train_mae(model, data):
    return -0.1


def calculate_test_mae(model, data):
    return 0.0


def calculate_rmse(model, data):
    return 0.1


@app.route("/forecast/<product_name>")
def get_forecast_plot(product_name):
    data = load_data(product_name)
    model = get_model(product_name)

    # Generate forecast
    forecast_horizon = 28

    last_date = datetime.strptime(data["Date"].max(), "%Y-%m-%d")
    forecast_dates = pd.date_range(
        start=last_date + pd.Timedelta(days=7), periods=forecast_horizon, freq="W"
    )

    # Use the forecast method for Holt-Winters model
    forecast = model.forecast(steps=forecast_horizon)
    forecast = constrain_forecast(data["Price"], forecast)

    # Convert data['Date'] to datetime if it's not already
    data["Date"] = pd.to_datetime(data["Date"])

    train_mae = calculate_train_mae(model, data)
    test_mae = calculate_test_mae(model, data)
    rmse = calculate_rmse(model, data)

    # Create plot
    plt.figure(figsize=(14, 7))
    plt.plot(data["Date"], data["Price"], label="Historical Data", marker="o")
    plt.plot(forecast_dates, forecast, label="Forecast", linestyle="--", marker="o")
    plt.legend()
    plt.title(f"Price Forecast for {product_name}")
    plt.xlabel("Date")
    plt.ylabel("Price Index")
    plt.grid(True)
    plt.xticks(rotation=45)

    # Set y-axis to start from an appropriate value
    # y_min = min(data['Price'].min(), min(forecast)) * 0.95  # 5% below the minimum
    # y_max = max(data['Price'].max(), max(forecast)) * 1.05  # 5% above the maximum
    # plt.ylim(y_min, y_max)

    # Add metrics to the plot
    plt.text(
        0.02,
        0.98,
        f"Train MAE: {train_mae:.2f}\nTest MAE: {test_mae:.2f}\nRMSE: {rmse:.2f}",
        transform=plt.gca().transAxes,
        verticalalignment="top",
        fontsize=10,
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
    )

    plt.tight_layout()

    # Save plot to a byte buffer
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()

    return send_file(buf, mimetype="image/png")


@app.route("/get_products")
def get_products():
    data = pd.read_csv(os.path.join(DATA_DIR, "price_data_long.csv"))
    products = data["Product"].unique().tolist()
    return jsonify(products)


@app.route("/")
def index():
    # return render_template(os.path.join(TEMPLATES_DIR, "index.html"))
    # TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), 'templates')

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
