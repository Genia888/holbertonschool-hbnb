from app import create_app
from app.extensions import db
from app.models import User, Place, Review, Amenity

app = create_app()
with app.app_context():
    db.create_all()
    session = db.session

    if not session.query(User).filter_by(email="john@doe.com").first():
        user = User(
            first_name="John",
            last_name="Doe",
            email="john@doe.com",
            password="$2b$12$2UIQci65wc4.jHNkPtqYX.lQLLiVC.TS3cYkGSQhLIE43.l.A1HdS",
            is_admin=True
        )
        session.add(user)

    place = Place(name="Cabin in the woods", description="Nature and peace", city="Annecy", address="Pine Tree Road")
    review = Review(text="Amazing experience surrounded by nature.")
    amenity = Amenity(name="Jacuzzi")

    session.add_all([place, review, amenity])
    session.commit()

    print("✅ Data successfully inserted.")
