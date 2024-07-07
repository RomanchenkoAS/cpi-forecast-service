from flask import Flask

from config import STATIC_DIR, TEMPLATES_DIR


def create_app():
    app = Flask(__name__, template_folder=TEMPLATES_DIR, static_folder=STATIC_DIR)

    from endpoints.forecast import forecast_bp
    from endpoints.main import main_bp
    from endpoints.products import products_bp

    app.register_blueprint(forecast_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(main_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
