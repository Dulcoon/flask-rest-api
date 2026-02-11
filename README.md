# Flask REST API – User, Product, Order
A simple REST API built with **Flask**, **SQLite**, and **SQLAlchemy** as part of a technical take-home test.

This project implements basic authentication using JWT and provides CRUD functionality for **User**, **Product**, and **Order** resources.  
No frontend interface is included — API only.


---


## Features
- JWT-based authentication (Register & Login)
- CRUD Product API
- Order creation with business logic:
  - stock validation
  - automatic total price calculation
- User-specific order listing
- Input validation with clear error messages
- SQLite database with SQLAlchemy ORM
- Database migration using Flask-Migrate


---


## Tech Stack

- **Python**
- **Flask**
- **Flask-JWT-Extended**
- **Flask-SQLAlchemy**
- **Flask-Migrate**
- **SQLite**
- **Marshmallow (validation concept)**
- **Decimal (financial precision)**


---


## Requirements
- Python 3.10 or newer


---


## Project Structure
```
app/
├── models/        # Database models (User, Product, Order)
├── routes/        # API routes (auth, product, order, user)
├── utils/         # Helper utilities (password hashing)
├── extensions.py  # Flask extensions (db, jwt, migrate)
├── config.py      # App configuration
├── __init__.py    # Application factory
run.py             # Application entry point
```

---


## 🚀 Getting Started (Local Setup)

### 1 Clone Repository
- git clone <repo-url>
- cd flask-rest-api

### 2 Create Virtual Environment
python -m venv venv

activate virtual environment
Windows:
venv\Scripts\activate

macOS / Linux:
source venv/bin/activate

### 3 Install Dependencies
pip install -r requirements.txt

### 4 Databaase Migration
- flask db init
- flask db migrate
- flask db upgrade

### 5 Run Aplication
python run.py

The API will be available at:
http://127.0.0.1:5000


---


## Authentication Flow
Register
POST /auth/register
{
  "email": "user@mail.com",
  "password": "secret123"
}

Login
POST /auth/login
Response:
{
  "access_token": "<JWT_TOKEN>"
}


Use the token for protected endpoints:
Authorization: Bearer <JWT_TOKEN>


---


## API Endpoints Overview
-Auth
| Method | Endpoint       | Description       |
| ------ | -------------- | ------------------|
| POST   | /auth/register | Register new user |
| POST   | /auth/login    | Login & get JWT   |

-User
| Method | Endpoint       | Auth |
| ------ | -------------- | ---- |
| GET    | /users/me      | yes  |

-Product
| Method | Endpoint       | Auth |
| ------ | -------------- | ---- |
| POST   | /products      | yes  |
| GET    | /products      | no   |
| GET    | /products/{id} | no   |
| PUT    | /products/{id} | yes  |
| DELETE | /products/{id} | yes  |

-Order
| Method | Endpoint | Auth |
| ------ | -------- | ---- |
| POST   | /orders  | yes  |
| GET    | /orders  | yes  |


---


## Authorization Rules
- Public endpoints:
  - GET /products
  - GET /products/{id}

- Protected endpoints (JWT required):
  - All user-related endpoints
  - Product create, update, delete
  - All order endpoints


---


## Notes on Price & Quantity ❗
- price is handled using Decimal for better financial precision.
- Price values should be sent as string in JSON.
- quantity must be a positive integer.
- total_price is calculated by the backend and cannot be set by the client.


---


## Deployment Note ❗
This project uses SQLite, which is suitable for local development and testing.  
For serverless platforms (e.g. Vercel), an external database would be required.  
Deployment is optional and not included in this repository.


---


## Author
Michael Valensio  
Developed as part of a backend internship technical assessment at JogjaCodingHouse (CODING COLECTIVE).
