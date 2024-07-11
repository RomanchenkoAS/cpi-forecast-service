import os

from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, send_file
from werkzeug.exceptions import HTTPException

import config
from cache import cache
from services.process_data.auto_process_data import handle_model_upload, \
    handle_model_creation_with_url
from services.tools import check_models_availability, delete_files_in_directory

main_bp = Blueprint("main", __name__)


@main_bp.route("/plot")
def plot():
    if check_models_availability():
        return render_template("plot.html")
    flash("Models unavailable", "error")
    return redirect(url_for("main.index"))


@main_bp.route("/")
def index():
    is_model_available: bool = check_models_availability()
    if is_model_available:
        flash("Models are ready", "success")
    return render_template("index.html", models_available=is_model_available)


@main_bp.route("/download_sample", methods=["GET"])
def download_sample_data():
    """
        Return to user sample data file.
    """
    file_path = os.path.join(config.STATIC_DIR, 'data_sample.csv')

    if not os.path.isfile(file_path):
        return "File not found", 404

    # Send the file to the user
    return send_file(file_path, as_attachment=True, download_name='data_sample.csv')


@main_bp.route("/check_models")
def check_models_availability_endpoint():
    is_model_available: bool = check_models_availability()
    return jsonify({"success": is_model_available}), 200


@main_bp.route("/models", methods=["GET", "POST"])
def create_models():
    """Endpoint to create models either by uploading a CSV file or using a custom URL."""
    if request.method == "POST":
        return handle_model_upload(request.files)
    elif request.method == "GET":
        return handle_model_creation_with_url(request.args.get("url", config.ROSSTAT_CPI_DATA_URL))
    else:
        raise HTTPException("Unsupported request method")


@main_bp.route("/erase")
def erase_models():
    """Endpoint to erase all models and clear the cache."""
    try:
        delete_files_in_directory(config.DATA_DIR)
        delete_files_in_directory(config.MODELS_DIR)
        cache.clear()
        flash("Models successfully deleted.", "info")
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400
