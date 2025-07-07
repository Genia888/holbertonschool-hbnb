from app.models.user import User
from app import db
from app.repositories.sqlalchemy_repository import SQLAlchemyRepository
from app.extensions import db

class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(User)

    def get_user_by_email(self, email):
        return self.model.query.filter_by(email=email).first()