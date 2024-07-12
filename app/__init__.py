import os
from flask import Flask
from extensions import db
from flask_cors import CORS
from config import Config
from flask_swagger_ui import get_swaggerui_blueprint
from app.routes.routes import bp as api_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config) 

    db.init_app(app)

    CORS(app)

    SWAGGER_URL = "/swagger"
    API_URL = "/static/swagger.json"
    SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
        SWAGGER_URL, API_URL, config={"app_name": "Black Woman History API"}
    )
    app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
    app.register_blueprint(api_bp, url_prefix='/api')

    app.config["SQLALCHEMY_ECHO"] = True
    app.config["SQLALCHEMY_RECORD_QUERIES"] = True
    return app
