from app.persistence.repository import InMemoryRepository, SQLAlchemyRepository
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review
from app.repositories.user_repository import UserRepository
from app.repositories.place_repository import PlaceRepository
from app.repositories.amenity_repository import AmenityRepository
from app.repositories.review_repository import ReviewRepository

class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()

    # ----- USER -----
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    # ----- PLACE -----
    def create_place(self, place_data):
        place = Place(
            title=place_data['title'],
            description=place_data.get('description', ''),
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner=place_data.get('owner_id')
        )

        for amenity_id in place_data.get('amenities', []):
            amenity = self.amenity_repo.get(amenity_id)
            if amenity:
                place.add_amenity(amenity)
            else:
                raise ValueError(f"Amenity with id {amenity_id} does not exist")

        self.place_repo.add(place)
        return place.to_dict()

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return [place.to_dict() for place in self.place_repo.get_all()]

    def update_place(self, place_id, place_data):
        place = self.get_place(place_id)
        if not place:
            return None

        for key in ['title', 'description', 'price', 'latitude', 'longitude']:
            if key in place_data:
                setattr(place, key, place_data[key])

        if 'amenities' in place_data:
            place.amenities = []
            for amenity_id in place_data['amenities']:
                amenity = self.amenity_repo.get(amenity_id)
                if amenity:
                    place.add_amenity(amenity)

        return place

    # ----- AMENITY -----
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None
        if 'name' in amenity_data:
            amenity.name = amenity_data['name']
        return amenity

    # ----- REVIEW -----
    def create_review(self, review_data, user_id, rating, place_id):
        user = self.get_user(user_id)
        if not user:
            raise ValueError("User not found.")

        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place not found.")

        review = Review(
            text=review_data["text"],
            user_id=user.id,
            place_id=place.id,
            rating=rating
        )
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError("Review not found")
        return review

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place not found")
        return [review for review in self.review_repo.get_all() if review.place_id == place_id]

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError("Review not found")

        for key, value in review_data.items():
            if hasattr(review, key):
                setattr(review, key, value)

        self.review_repo.update(review_id, review.__dict__)
        return review

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError("Review not found")
        self.review_repo.delete(review_id)
        return {'message': 'Review deleted successfully'}

# Instance globale
facade = HBnBFacade()
