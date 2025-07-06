from app.models.user import User
from app.repositories.user_repository_interface import UserRepositoryInterface
from app import db

class SQLAlchemyUserRepository(UserRepositoryInterface):
    def get_by_id(self, user_id):
        return User.query.get(user_id)

    def get_by_email(self, email):
        return User.query.filter_by(email=email).first()

    def create(self, user_data):
        user = User(**user_data)
        db.session.add(user)
        db.session.commit()
        return user

    def update(self, user_id, updates):
        user = self.get_by_id(user_id)
        if not user:
            return None
        for key, value in updates.items():
            setattr(user, key, value)
        db.session.commit()
        return user

    def delete(self, user_id):
        user = self.get_by_id(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
