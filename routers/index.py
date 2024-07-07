import io
import os
import pickle

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from flask import Flask, send_file

app = Flask(__name__)

from config import DATA_DIR
from services.tools import slugify_cyrillic_word


def load_data(product_name):
    data = pd.read_csv(os.path.join(DATA_DIR, "price_data_long.csv"))

    # Create a mapping of slugified product names to original product names
    product_mapping = {slugify_cyrillic_word(prod): prod for prod in data['Product'].unique()}

    # Find the original product name that matches the slugified input
    original_product_name = product_mapping.get(product_name)

    if original_product_name is None:
        raise ValueError(f"No product found matching '{product_name}'")

    # Filter the data for the matched product
    product_data = data[data['Product'] == original_product_name].sort_values(by='Date')

    return product_data


def constrain_forecast(original, forecast, max_change=0.05):
    constrained = [original[-1]]  # Start with the last known value
    for f in forecast:
        change = (f - constrained[-1]) / constrained[-1]
        if abs(change) > max_change:
            new_value = constrained[-1] * (1 + max_change * np.sign(change))
        else:
            new_value = f
        constrained.append(new_value)
    return constrained[1:]  # Remove the initial seed value


@app.route('/forecast/<product_name>')
def forecast(product_name):
    # Load the data
    data = load_data(product_name)

    # Load the model
    model_filename = f"{product_name.replace(' ', '_')}_model.pkl"
    model_path = os.path.join(DATA_DIR, "trained_models", model_filename)
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    print(data)

    # Generate forecast
    forecast_horizon = 28
    last_date = data['Date'].max()
    print(f"last_date = {last_date}")
    forecast_dates = pd.date_range(start=last_date + pd.Timedelta(days=7), periods=forecast_horizon, freq='W')
    forecast = model.get_forecast(steps=forecast_horizon).predicted_mean
    forecast = constrain_forecast(data['Price'], forecast)

    # Create plot
    plt.figure(figsize=(14, 7))
    plt.plot(data['Date'], data['Price'], label='Historical Data', marker='o')
    plt.plot(forecast_dates, forecast, label='Forecast', linestyle='--', marker='o')
    plt.legend()
    plt.title(f'Price Forecast for {product_name}')
    plt.xlabel('Date')
    plt.ylabel('Price Index')
    plt.grid(True)
    plt.xticks(rotation=45)

    # Set y-axis to start from an appropriate value
    y_min = min(data['Price'].min(), min(forecast)) * 0.95  # 5% below the minimum
    y_max = max(data['Price'].max(), max(forecast)) * 1.05  # 5% above the maximum
    plt.ylim(y_min, y_max)

    plt.tight_layout()

    # Save plot to a byte buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    return send_file(buf, mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True)
