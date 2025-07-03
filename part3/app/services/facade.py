from werkzeug.security import generate_password_hash, check_password_hash
from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.engine.db_storage import storage
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # ----- USER -----
    def create_user(self, user_data):
        user_data["password"] = generate_password_hash(user_data["password"])
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def authenticate_user(self, email, password):
        user = self.get_user_by_email(email)
        if not user or not check_password_hash(user.password, password):
            return None
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    # ----- PLACE -----
    # (le reste de tes méthodes existantes…)

# instance globale
dalton = HBnBFacade()

# instance globale
dalton = HBnBFacade()
facade = dalton
