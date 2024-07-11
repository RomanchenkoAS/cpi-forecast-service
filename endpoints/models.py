from flask import Blueprint, flash, jsonify, request
from werkzeug.exceptions import HTTPException

import config
from cache import cache
from services.process_data.auto_process_data import (
    handle_model_creation_with_url,
    handle_model_upload,
)
from services.tools import check_models_availability, delete_files_in_directory

models_bp = Blueprint("models", __name__)


@models_bp.route("/check_models")
def check_models_availability_endpoint():
    is_model_available: bool = check_models_availability()
    return jsonify({"success": is_model_available}), 200


@models_bp.route("/models", methods=["GET", "POST"])
def create_models():
    """Endpoint to create models either by uploading a CSV file or using a custom URL."""
    if request.method == "POST":
        return handle_model_upload(request.files)
    elif request.method == "GET":
        return handle_model_creation_with_url(
            request.args.get("url", config.ROSSTAT_CPI_DATA_URL)
        )
    else:
        raise HTTPException("Unsupported request method")


@models_bp.route("/erase")
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
