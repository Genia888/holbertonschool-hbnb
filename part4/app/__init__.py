from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from app.extensions import db, bcrypt
from flask_restx import Api
from app.api.v1.users import api as users_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.amenities import api as amenities_ns
from flask_jwt_extended import JWTManager
from app.api.v1.auth import api as auth_ns
from flask_cors import CORS


jwt = JWTManager()


def create_app(config_name="default"):

    from config import config # Importe le dictionnaire
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    CORS(app)

    @app.route('/')
    def create_index():
        return render_template('index.html')
    
    @app.route('/index.html')
    def create_index2():
        return render_template('index.html')
    
    @app.route('/login.html')
    def create_login():
        return render_template('login.html')
    
    @app.route('/place.html')
    def create_place():
        return render_template('place.html')

    
    api = Api(app, version='1.0', title='HBnB API',
              description='HBnB Application API')

    # Register the users namespace
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')
    
    return app
