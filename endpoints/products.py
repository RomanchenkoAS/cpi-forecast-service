import pandas as pd
from flask import Blueprint, jsonify

import config
from services.tools import slugify

products_bp = Blueprint("products", __name__)


@products_bp.route("/get_products")
def get_products():
    data = pd.read_csv(config.DATA_FILE_PATH)
    products = data["Product"].unique()
    product_pairs = [(prod, slugify(prod)) for prod in products]
    return jsonify(product_pairs)
