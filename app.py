import os

from dotenv import load_dotenv
from flask import Flask

import config
from cache import init_cache
from endpoints.forecast import forecast_bp
from endpoints.main import main_bp
from endpoints.products import products_bp
from services.tools import ensure_directory_exists_and_writable

load_dotenv()

app = Flask(__name__, template_folder=config.TEMPLATES_DIR, static_folder=config.STATIC_DIR)
app.secret_key = os.getenv("SECRET_KEY")
init_cache(app)
app.register_blueprint(forecast_bp)
app.register_blueprint(products_bp)
app.register_blueprint(main_bp)

if __name__ == "__main__":
    ensure_directory_exists_and_writable(config.DATA_DIR)
    ensure_directory_exists_and_writable(config.MODELS_DIR)
    app.run(debug=os.getenv("DEBUG", False))
