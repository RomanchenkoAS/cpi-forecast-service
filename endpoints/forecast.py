from datetime import datetime

import pandas as pd
from flask import Blueprint, send_file, jsonify

from services.forecast import (
    calculate_rmse,
    constrain_forecast,
    create_forecast_plot,
    get_model_dict,
    load_data,
)
from services.tools import slugify

forecast_bp = Blueprint("forecast", __name__)


@forecast_bp.route("/forecast/<product_name>")
def get_forecast_plot(product_name):
    """
    Return plot as an image.
    """
    data = load_data(product_name)
    model_dict = get_model_dict(product_name)

    model = model_dict["model"]

    forecast_horizon = 28
    last_date = datetime.strptime(data["Date"].max(), "%Y-%m-%d")
    forecast_dates = pd.date_range(
        start=last_date + pd.Timedelta(days=7), periods=forecast_horizon, freq="W"
    )
    forecast = model.forecast(steps=forecast_horizon)
    forecast = constrain_forecast(data["Price"], forecast)

    data["Date"] = pd.to_datetime(data["Date"])

    train_mae = model_dict["train_mae"]
    test_mae = model_dict["test_mae"]
    rmse = calculate_rmse(model, data)
    plot_title = model_dict["product_name"]

    buf = create_forecast_plot(
        data, forecast_dates, forecast, plot_title, train_mae, test_mae, rmse
    )

    return send_file(buf, mimetype="image/png")


@forecast_bp.route("/get_metadata/<product_name>")
def get_metadata(product_name):
    model_dict = get_model_dict(product_name)
    metadata = {
        "url": f"/forecast/{slugify(product_name)}",
        "product_name": model_dict["product_name"],
        "train_mae": model_dict["train_mae"],
        "test_mae": model_dict["test_mae"],
        "date_created": model_dict["date_created"].isoformat(),
    }
    return jsonify(metadata)
