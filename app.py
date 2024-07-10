from flask import Flask

from config import STATIC_DIR, TEMPLATES_DIR
from endpoints.forecast import forecast_bp
from endpoints.main import main_bp
from endpoints.products import products_bp

app = Flask(__name__, template_folder=TEMPLATES_DIR, static_folder=STATIC_DIR)
app.secret_key = "INSECURE_aefbd38c8b3641cb82f823ece1ee4b6b"
app.register_blueprint(forecast_bp)
app.register_blueprint(products_bp)
app.register_blueprint(main_bp)

if __name__ == "__main__":
    app.run(debug=True)
