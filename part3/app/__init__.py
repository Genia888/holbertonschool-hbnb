from flask import Flask
from flask_jwt_extended import JWTManager
from .api.v1 import api_v1

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dev.db'
    app.config["JWT_SECRET_KEY"] = "your-secret-key"
    JWTManager(app)
    app.register_blueprint(api_v1)
    db.init_app(app)
    return app

from app.models import Base
from app.extensions import db

def init_db():
    with db.engine.begin() as conn:
        Base.metadata.create_all(conn)
