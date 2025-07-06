from app.extensions import db
from .base_model import BaseModel

class User(BaseModel, db.Model):
    __tablename__ = 'users'
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class Place(BaseModel, db.Model):
    __tablename__ = 'places'
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=True)
    city = db.Column(db.String(128), nullable=False)
    address = db.Column(db.String(256), nullable=False)

class Review(BaseModel, db.Model):
    __tablename__ = 'reviews'
    text = db.Column(db.Text, nullable=False)

class Amenity(BaseModel, db.Model):
    __tablename__ = 'amenities'
    name = db.Column(db.String(128), nullable=False)
