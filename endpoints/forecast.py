import io
import os
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
from flask import Blueprint, jsonify, send_file

from services.forecast import (
    calculate_rmse,
    calculate_test_mae,
    calculate_train_mae,
    constrain_forecast,
    create_forecast_plot,
    get_model,
    load_data,
)
from services.tools import slugify

forecast_bp = Blueprint("forecast", __name__)


@forecast_bp.route("/forecast/<product_name>")
def get_forecast_plot(product_name):
    data = load_data(product_name)
    model = get_model(product_name)

    forecast_horizon = 28
    last_date = datetime.strptime(data["Date"].max(), "%Y-%m-%d")
    forecast_dates = pd.date_range(
        start=last_date + pd.Timedelta(days=7), periods=forecast_horizon, freq="W"
    )
    forecast = model.forecast(steps=forecast_horizon)
    forecast = constrain_forecast(data["Price"], forecast)

    data["Date"] = pd.to_datetime(data["Date"])

    train_mae = calculate_train_mae(model, data)
    test_mae = calculate_test_mae(model, data)
    rmse = calculate_rmse(model, data)

    buf = create_forecast_plot(
        data, forecast_dates, forecast, product_name, train_mae, test_mae, rmse
    )

    return send_file(buf, mimetype="image/png")
