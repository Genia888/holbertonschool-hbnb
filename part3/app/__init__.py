from flask_jwt_extended import JWTManager
import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_jwt_extended import JWTManager
from flask_jwt_extended import JWTManager
from flask_jwt_extended import JWTManager
from flask_jwt_extended import JWTManager
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from app.extensions import db, bcrypt
from flask_restx import Api
from app.api.v1.users import api as users_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.amenities import api as amenities_ns

db = SQLAlchemy()

def create_app(config_name="default"):

    from config import config # Importe le dictionnaire
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'dev-secret')
    from app.extensions import jwt
    jwt.init_app(app)
    app.config.from_object(config[config_name])

    db.init_app(app)
    bcrypt.init_app(app)
    
    api = Api(app, version='1.0', title='HBnB API',
              description='HBnB Application API')

    # Register the users namespace
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    
    return app
