import os

from flask import Blueprint, render_template, redirect, url_for, flash, send_file

import config
from services.tools import check_models_availability

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """ Main page. """
    is_model_available: bool = check_models_availability()
    if is_model_available:
        flash("Models are ready", "success")
    return render_template("index.html", models_available=is_model_available)


@main_bp.route("/plot")
def plot():
    """ Plot display page. """
    if check_models_availability():
        return render_template("plot.html")
    flash("Models unavailable", "error")
    return redirect(url_for("main.index"))


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
