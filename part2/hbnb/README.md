# C#26 🌭️ - Part 2 - HBnB Team Project -

## 📅 Overview

This project is part of the HBnB web application and focuses on building the **Business Logic** and **Presentation (API)** layers of the app. In Part 2, we define the project structure, implement core entity classes, and set up a RESTful API using **Flask** and **Flask-RESTx**.

---

## ✅ Objectives

* Create a modular project architecture
* Implement core business logic for **Users**, **Places**, **Reviews**, and **Amenities**
* Set up a Flask-based RESTful API with `flask-restx`
* Build a **facade layer** to connect the API and business logic

---

## 🚀 Table of Contents

1. [Project Structure](#project-structure)
2. [Key Concepts](#key-concepts)
3. [Quick Start](#quick-start)
4. [Architecture](#architecture)
5. [Endpoints](#endpoints)
6. [Example Flows](#example-flows)
7. [Useful Scripts](#useful-scripts)
8. [Roadmap](#roadmap)
9. [Team](#team)

---

## 📂 Project Structure

```bash
hbnb/
├── app/
│   ├── __init__.py               # Initializes the app package
│   ├── api/                      # 🌐 Presentation Layer (REST API)
│   │   ├── __init__.py           # Initializes the API module
│   │   └── v1/                   # Version 1 of the REST API
│   │       ├── __init__.py       # Init v1
│   │       ├── users.py          # REST endpoints for /users
│   │       ├── places.py         # REST endpoints for /places
│   │       ├── reviews.py        # REST endpoints for /reviews
│   │       └── amenities.py      # REST endpoints for /amenities
│   ├── models/                   # 📂 Model Layer – entity representations
│   │   ├── __init__.py
│   │   ├── user.py               # User class (name, email...)
│   │   ├── place.py              # Place class (description, city...)
│   │   ├── review.py             # Review class (rating, text...)
│   │   ├── amenity.py            # Amenity class (wifi, TV...)
│   │   └── basemodel.py          # Base class: UUID + timestamps
│   ├── services/                 # 🧠 Business Logic Layer
│   │   ├── __init__.py
│   │   └── facade.py             # Central logic via Facade Pattern
│   └── persistence/              # 📀 Persistence Layer – temporary storage
│       ├── __init__.py
│       └── repository.py         # Simulates DB with in-memory storage
├── run.py                        # Launches the Flask API + Swagger
├── config.py                     # Global settings (CORS, DEBUG...)
├── requirements.txt              # Required Python modules
├── tree.py                       # Displays project tree structure
├── README.md                     # This file
```

---

## 🧠 Key Concepts

* **Modularity**: Clean separation between API, logic, models, and persistence
* **Flask & Flask-RESTx**: Simple framework with Swagger auto-doc
* **RESTful API**: CRUD through HTTP routes
* **Facade Pattern**: Aggregates logic behind a single service
* **In-memory Persistence**: Simulates a real DB
* **Versioned API**: `/api/v1/` prefix for endpoints

---

## ⚡️ Quick Start

```bash
# Clone the repo
git clone https://github.com/ddoudou7/holbertonschool-hbnb.git
cd holbertonschool-hbnb/part2/hbnb

# Optional: virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the API
python run.py

# Docs at:
http://localhost:5000/
```

---

## 🏗️ Architecture

* **API Layer** → `/app/api/v1/`
* **Business Layer** → `/app/services/facade.py`
* **Model Layer** → `/app/models/`
* **Persistence** → `/app/persistence/repository.py`

---

## 🌐 Endpoints

| Method | Endpoint             | Description    |
| ------ | -------------------- | -------------- |
| GET    | `/api/v1/users`      | List users     |
| POST   | `/api/v1/users`      | Create user    |
| GET    | `/api/v1/users/<id>` | Get user by ID |
| PUT    | `/api/v1/users/<id>` | Update user    |
| DELETE | `/api/v1/users/<id>` | Delete user    |

> (Same for `/places`, `/reviews`, `/amenities`)

---

## 🔄 Example Flows

### ➕ Create a User

```bash
curl -X POST http://localhost:5000/api/v1/users \
     -H "Content-Type: application/json" \
     -d '{"name": "Alice", "email": "alice@mail.com"}'
```

### 📥 Get Places

```bash
curl http://localhost:5000/api/v1/places
```

### ❌ Delete Review

```bash
curl -X DELETE http://localhost:5000/api/v1/reviews/<id>
```

---

## 🛠️ Useful Scripts

| Command           | Description            |
| ----------------- | ---------------------- |
| `python tree.py`  | Show project structure |
| `python run.py`   | Run API locally        |
| `pip install ...` | Install dependencies   |

---

## 🗺️ Roadmap

### ✅ Completed

* Modular architecture (Model/Service/API)
* Full CRUD endpoints
* Facade logic layer
* REST API with Swagger

### 🚀 Next Steps

* Input validation
* OpenAPI/Swagger full doc

---

## 🤝 Team

* Mr Phillips
* Sofian
* Evgeni
