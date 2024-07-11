from datetime import datetime

import pandas as pd
from flask import Blueprint, send_file, jsonify

from cache import cache
from services.forecast import (
    calculate_rmse,
    constrain_forecast,
    create_forecast_plot,
    get_model_dict,
    load_data,
)

forecast_bp = Blueprint("forecast", __name__)


@forecast_bp.route("/forecast/<product_name>")
@cache.cached(timeout=60 * 60, query_string=True)
def get_forecast_plot(product_name):
    """
    Return plot as an image for the given product name.
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
@cache.cached(timeout=60 * 60, query_string=True)
def get_metadata(product_name):
    """
    Return metadata for a given product.
    """
    try:
        model_dict = get_model_dict(product_name)

        # Prepare dict for sending
        model_dict['date_created'] = model_dict["date_created"].strftime("%Y-%m-%d %H:%M:%S")
        model_dict.pop("model")

        return jsonify(model_dict)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
