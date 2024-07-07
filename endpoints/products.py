import os

import pandas as pd
from flask import Blueprint, jsonify

from config import DATA_DIR
from services.tools import slugify_cyrillic_word

products_bp = Blueprint("products", __name__)


@products_bp.route("/get_products")
def get_products():
    data = pd.read_csv(os.path.join(DATA_DIR, "price_data_long.csv"))
    products = data["Product"].unique()
    product_pairs = [(prod, slugify_cyrillic_word(prod)) for prod in products]
    return jsonify(product_pairs)
