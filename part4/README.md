# C#26 :school: <img src="https://cdn.prod.website-files.com/6105315644a26f77912a1ada/63eea844ae4e3022154e2878_Holberton-p-800.png" width="150" /> - Part 4 - HBnB Project -

## Overview
This project is the final part (Part 4) of the HBnB web application, developed as a team project at Holberton School. It is a full-stack web platform for booking and reviewing places, inspired by Airbnb. The project combines a Python/Flask REST API backend with a modern, responsive JavaScript/HTML/CSS frontend.

## Features
- **User Authentication:** Secure login/logout with JWT tokens.
- **Place Listings:** Browse a list of places with images, prices, and details.
- **Place Details:** View detailed information about each place, including description, price, location, amenities, and reviews.
- **Amenities:** Each place displays its available amenities.
- **Reviews:** Authenticated users can add reviews and ratings for places (one review per user per place).
- **Filtering:** Filter places by price.
- **Responsive Design:** The UI is fully responsive and adapts to all screen sizes.
- **Dynamic Frontend:** All data is loaded dynamically via API calls (no page reloads).


## Backend (API)
- The backend is a Flask REST API (see `part3/`).
- Endpoints:
  - `/api/v1/places/` - List all places
  - `/api/v1/places/<id>` - Get details for a place
  - `/api/v1/reviews/places/<place_id>/reviews` - Get/add reviews for a place
  - `/api/v1/auth/login` - User login
  - `/api/v1/auth/me` - Get current user info
- Each place includes: `id`, `title`, `description`, `price`, `latitude`, `longitude`, `image_url`, `amenities` (list of names)
- Reviews include: `user_first_name`, `rating`, `text`

## Frontend
- **index.html:**
  - Displays all places as cards with images, title, and price.
  - Each card links to the details page.
  - Price filter available.
- **place.html:**
  - Shows all details for a selected place.
  - Displays the same image as on the home page.
  - Lists amenities and reviews.
  - Allows logged-in users to add a review if they haven't already.
- **login.html:**
  - User authentication form.
- **add_review.html:**
  - Review form (included in place.html for dynamic display).

## How to Run
1. **Backend:**
   - Go to `part3/` and run the Flask app (`python3 run.py`).
   - Make sure the database is set up (`app.db`).
2. **Frontend:**
   - Open `part4/index.html` in your browser.
   - The frontend will communicate with the backend API at `http://127.0.0.1:5000`.

## Technologies Used
- Python 3, Flask, Flask-RESTx, SQLAlchemy
- HTML5, CSS3, JavaScript (ES6)
- JWT for authentication

## Team & Credits
- Project by Holberton School students, C#26.
- See project contributors in the repository.

## Screenshots
![Home Page](images/house.jpg)

---
For any questions or issues, please contact the project maintainers.