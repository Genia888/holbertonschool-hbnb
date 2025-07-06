from app import create_app, init_db
from app.models import User
from app.extensions import db

app = create_app()
with app.app_context():
    init_db()

with app.app_context():
    session = db.session
    user = User(first_name="John", last_name="Doe", email="john@doe.com", is_admin=True)
    user.set_password("abc123")
    session.add(user)
    session.commit()

    found = session.query(User).filter_by(email="john@doe.com").first()
    print("User found:", found.first_name, found.last_name, found.email)
