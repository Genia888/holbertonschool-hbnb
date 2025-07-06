from flask import Flask
from app.extensions import db
from app.api.v1 import api_v1
from app.base_model import Base

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dev.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    app.register_blueprint(api_v1, url_prefix="/api/v1")
    return app
