import uuid
from datetime import datetime
from app import db
from app.extensions import db

class BaseModel(db.Model):
    __abstract__ = True
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """Mets à jour la modif date(upadate_at) quand l'obj est changé"""
        self.updated_at = datetime.now()

    def update(self, data):
        """Mets à jours les attributs de l'obj à l'aide d'un dico"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()  # Mets à jour la date de modif
