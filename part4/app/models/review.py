from .basemodel import BaseModel
from app import db

class Review(BaseModel):
    __tablename__ = "reviews"

    text = db.Column(db.Text, nullable = False)
    rating = db.Column(db.Integer, nullable = False)
    
    def __init__(self, text, user_id, place_id, rating):
        super().__init__()
        self.text = text
        self.user_id = user_id
        self.place_id = place_id
        self.rating = rating  # Ajout du champ rating

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "user_id": self.user_id,
            "place_id": self.place_id,
            "rating": self.rating,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
