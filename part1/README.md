# C#26 :school: <img src="https://cdn.prod.website-files.com/6105315644a26f77912a1ada/63eea844ae4e3022154e2878_Holberton-p-800.png" width="150" /> - HBnB Team Project - 

## 📌 Objective

The goal of this task is to create a **high-level package diagram** that illustrates the **three-layer architecture** of the HBnB Evolution application. The diagram provides a conceptual overview of how the main components of the system are organized and how they communicate with each other using the **Facade Pattern**.

---

## 🧱 Layered Architecture Overview

The HBnB Evolution system follows a classic **3-layer architecture**:

### 1. Presentation Layer (API / Services)
- This layer handles the interaction between the user and the application. It includes all the services and APIs that are exposed to the users.

### 2. Business Logic Layer (Models)
- This layer contains the core business logic and the models that represent the entities in the system.
- Includes model managers for:
  - `User`
  - `Place`
  - `Review`
  - `Amenity`
- Exposes a **Facade** interface to decouple upper and lower layers.

### 3. Persistence Layer
- This layer is responsible for data storage and retrieval, interacting directly with the database..

#!/usr/bin/python3
"""
Saves a Python object to a file using JSON format.
"""

import json


def save_to_json_file(my_obj, filename):
    """
    Writes an object to a file in JSON format.
    """
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(my_obj, f)

---

## 🔁 Communication Flow

- **Presentation → Business Logic:**  
  The **Facade Pattern** is used to expose a simplified, unified interface from the Business Logic Layer to the Presentation Layer.

- **Business Logic → Persistence:**  
  Business logic components access data through well-defined **Repository** or **DAO** interfaces, abstracting the database layer.

---

## 📊 Diagram

The high-level package structure is represented below using **UML syntax (Mermaid.js)**:

```mermaid
classDiagram
class Presentation {
  <<Interface>>
  +Services
  +API endpoints
}
class BusinessLogic {
  <<Core Models>>
  +User
  +Place
  +Review
  +Amenity
}
class Persistence {
    <<DataStorage>>
  +Database
  +Repository
  +data_save()
  +data_fetch()
}

Presentation --> BusinessLogic : Facade Pattern
BusinessLogic --> Persistence : Database Access
