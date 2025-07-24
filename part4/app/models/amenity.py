from .basemodel import BaseModel
from app.extensions import db

class Amenity(BaseModel):
    __tablename__ = "amenities"

    name = db.Column(db.String(255), nullable =False)
    
    def __init__(self, name):
        super().__init__()

        if not isinstance(name, str) or not name.strip():
            raise ValueError ("The amenities name must be a string available")
        
        self.name = name.strip()


    def __str__(self):
        # Retourne une représentation claire de l'amenity
        return f"[Amenity] ({self.id}) {self.name}"
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
