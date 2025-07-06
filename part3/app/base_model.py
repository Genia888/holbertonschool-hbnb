from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String
import uuid

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    id = Column(String(60), primary_key=True, default=lambda: str(uuid.uuid4()))
