from flask import Blueprint, render_template, request, jsonify
from werkzeug.exceptions import HTTPException

main_bp = Blueprint("main", __name__)


@main_bp.route("/plot")
def plot():
    return render_template("plot.html")


@main_bp.route("/models", methods=["GET", "POST"])
def create_models():
    if request.method == "POST":
        raise NotImplementedError("POST method not implemented")
    elif request.method == "GET":
        return jsonify({"message": "Not implemented yet 123"})
    else:
        # Handle other request methods
        raise HTTPException("Unsupported request method")
