from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime, Boolean
from app.extensions import bcrypt
import uuid

class BaseModel:
    id = Column(String(60), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

Base = declarative_base(cls=BaseModel)

class User(Base):
    __tablename__ = 'users'
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False, unique=True)
    _password = Column("password", String(128), nullable=False)
    is_admin = Column(Boolean, default=False)

    def set_password(self, plaintext_password):
        self._password = bcrypt.generate_password_hash(plaintext_password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self._password, password)
PLACES = []
