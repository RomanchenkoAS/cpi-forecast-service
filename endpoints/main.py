from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from werkzeug.exceptions import HTTPException

import config

main_bp = Blueprint("main", __name__)


@main_bp.route("/plot")
def plot():
    print("IN PLOT")
    return render_template("plot.html")


@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.route("/upload")
def upload():
    # Endpoint to upload CSV file, then redirect to /models
    raise NotImplementedError()


def check_models_availability():
    pass


@main_bp.route("/check_models")
def check_models_availability_endpoint():
    # Check if models are available 
    if check_models_availability():
        return jsonify({"success": True}), 200
    return jsonify({"success": False}), 200


@main_bp.route("/models", methods=["GET", "POST"])
def create_models():
    if request.method == "POST":
        raise NotImplementedError("POST method not implemented")
    elif request.method == "GET":
        # This feature is not implemented on front-end yet.
        download_url = request.args.get("url", config.ROSSTAT_CPI_DATA_URL)
        try:
            # auto_process_data(data_download_url=download_url)
            return jsonify({"success": True}), 200
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    else:
        # Handle other request methods
        raise HTTPException("Unsupported request method")
