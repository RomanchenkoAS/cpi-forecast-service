from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from werkzeug.exceptions import HTTPException

import config
from services.auto_process_data import auto_process_data

main_bp = Blueprint("main", __name__)


@main_bp.route("/plot")
def plot():
    return render_template("plot.html")


@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.route("/upload")
def upload():
    # Endpoint to upload CSV file, then redirect to /models
    raise NotImplementedError()


@main_bp.route("/models", methods=["GET", "POST"])
def create_models():
    if request.method == "POST":
        raise NotImplementedError("POST method not implemented")
    elif request.method == "GET":
        url = request.args.get("url", config.ROSSTAT_CPI_DATA_URL)
        try:
            auto_process_data(data_download_url=url)
            return redirect(url_for("main.plot"))
        except Exception as e:
            return jsonify({"success": False, "error": str(e)})

    else:
        # Handle other request methods
        raise HTTPException("Unsupported request method")
