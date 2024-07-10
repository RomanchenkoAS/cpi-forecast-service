import os

from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, send_file
from werkzeug.exceptions import HTTPException

import config
from services.auto_process_data import auto_process_data
from services.tools import check_models_availability

main_bp = Blueprint("main", __name__)


@main_bp.route("/plot")
def plot():
    if check_models_availability():
        return render_template("plot.html")
    else:
        flash("Models unavailable", "error")
        return redirect(url_for("main.index"))


@main_bp.route("/")
def index():
    models_available = check_models_availability()
    if models_available:
        flash("Models are ready", "success")
    return render_template("index.html", models_available=models_available)


@main_bp.route("/download-sample", methods=["GET"])
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
    if check_models_availability():
        return jsonify({"success": True}), 200
    return jsonify({"success": False}), 200


@main_bp.route("/models", methods=["GET", "POST"])
def create_models():
    if request.method == "POST":
        # Endpoint to upload CSV file manually
        if 'file' not in request.files:
            return jsonify({"success": False, "error": "No file provided"}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({"success": False, "error": "No file provided"}), 400

        if file and file.filename.endswith('.csv'):
            file.save(config.DATA_FILE_PATH)
            auto_process_data()
            return jsonify({"success": True}), 200
        else:
            return jsonify({"success": False, "error": "Invalid file type. Only CSV files are allowed."}), 400

    elif request.method == "GET":
        # Custom URL from user: this feature is not implemented on front-end.
        download_url = request.args.get("url", config.ROSSTAT_CPI_DATA_URL)
        try:
            auto_process_data(data_download_url=download_url)
            return jsonify({"success": True}), 200
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    else:
        raise HTTPException("Unsupported request method")


@main_bp.route("/erase")
def erase_models():
    try:
        # Delete all contents in config.DATA_DIR
        for filename in os.listdir(config.DATA_DIR):
            file_path = os.path.join(config.DATA_DIR, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                os.rmdir(file_path)

        # Delete all contents in config.MODELS_DIR
        for filename in os.listdir(config.MODELS_DIR):
            file_path = os.path.join(config.MODELS_DIR, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                os.rmdir(file_path)

        flash("Models successfully deleted.", "info")
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400
