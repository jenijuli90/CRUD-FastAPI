# FastAPI Social Media API 

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)
![CI/CD](https://img.shields.io/badge/CI/CD-GitHub%20Actions-orange)

A RESTful backend API built using **FastAPI, SQLAlchemy ORM, PostgreSQL, Docker, and JWT Authentication**.

This project implements user authentication, post management, and a voting system similar to a social media platform.

---

# Features

## Authentication

- User registration
- User login
- JWT-based authentication
- OAuth2 password flow
- Secure password hashing using Argon2
- Protected API routes
- Token expiration handling

---

## User Management

- Create new users
- Fetch user details
- Email validation
- Duplicate email prevention
- Secure password storage

---

## Post Management

- Create posts
- Retrieve all posts
- Retrieve post by ID
- Update posts
- Delete posts
- Search posts
- Pagination support
- User ownership validation

---

## Voting System

- Users can vote on posts
- Prevent duplicate votes
- Count total votes per post
- Database relationship between users and posts

---

## Error Handling

- Centralized exception handling
- Database rollback on errors
- Proper HTTP status codes
- Custom error handling decorator

---

# Tech Stack

| Technology | Purpose |
|------------|---------|
| FastAPI | Backend API framework |
| SQLAlchemy | Database ORM |
| PostgreSQL | Database |
| Pydantic | Data validation |
| JWT | Authentication |
| OAuth2 | Security protocol |
| Passlib + Argon2 | Password hashing |
| Docker | Containerization |
| Docker Compose | Multi-container setup |
| GitHub Actions | CI/CD automation |
| Uvicorn | ASGI server |
| Python | Programming language |

---

# Project Structure

```
fastapi-social-media-api/

│
├── app/
│   │
│   ├── main.py              # FastAPI application entry point
│   ├── database.py          # Database connection and session
│   ├── models.py            # SQLAlchemy database models
│   ├── schemas.py           # Pydantic request/response models
│   ├── token.py             # JWT token creation and validation
│   ├── utils.py             # Password hashing utilities
│   ├── config.py            # Application configuration
│   │
│   └── routers/
│       │
│       ├── user.py          # User APIs
│       ├── auth.py          # Authentication APIs
│       ├── post.py          # Post CRUD APIs
│       ├── like.py          # Voting APIs
│       └── decorator.py     # Error handling decorator
│
├── Dockerfile               # Docker image configuration
├── docker-compose.yml       # Multi-container configuration
│
├── .github/
│   └── workflows/
│       └── ci.yml           # GitHub Actions CI/CD pipeline
│
├── .env.example             # Environment variable template
├── .gitignore               # Git ignored files
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation

```

---

# Installation and Setup

## 1. Clone Repository

```bash
git clone https://github.com/jenijuli90/CRUD-FastAPI
```

Move into project directory:

```bash
cd fastapi-social-media-api
```

---

# 2. Create Virtual Environment

Create virtual environment:

```bash
python -m venv venv
```

Activate it:

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

---

# 3. Install Dependencies

Install required packages:

```bash
pip install -r requirements.txt
```

---

# Environment Variables Setup

Create a `.env` file in the project root.

Copy the example file:

```bash
cp .env.example .env
```

Update the values according to your local setup.

Example:

```env
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=fastapi_db
DATABASE_USERNAME=postgres
DATABASE_PASSWORD=your_password

SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Never commit the `.env` file to GitHub.

---

# Database Setup

This project uses PostgreSQL.

Create database:

```sql
CREATE DATABASE fastapi_db;
```

Update database credentials in `.env`.

The application automatically creates tables when it starts:

```python
Base.metadata.create_all(bind=engine)
```

---

# Running the Application

Start FastAPI server:

```bash
uvicorn app.main:app --reload
```

Application will run at:

```
http://127.0.0.1:8000
```

---

# Docker Setup

## Build Docker Image

```bash
docker build -t fastapi-social-media-api .
```

---

## Run Docker Container

```bash
docker run -p 8000:8000 fastapi-social-media-api
```

---

## Docker Compose

Start FastAPI and PostgreSQL containers:

```bash
docker-compose up --build
```

Stop containers:

```bash
docker-compose down
```

---

# CI/CD Pipeline

This project uses GitHub Actions for automation.

Workflow:

```
Developer
    |
    |
Git Push
    |
    |
GitHub Actions
    |
    |
Install Dependencies
    |
    |
Run Tests
    |
    |
Build Docker Image
    |
    |
Deploy Application
```

CI/CD process includes:

- Installing dependencies
- Running automated tests
- Building Docker images
- Automated deployment

---

# API Documentation

FastAPI automatically generates interactive documentation.

## Swagger UI

```
http://127.0.0.1:8000/docs
```

## ReDoc

```
http://127.0.0.1:8000/redoc
```

---

# Authentication Flow

## 1. Register User

Endpoint:

```
POST /users/
```

User passwords are hashed using Argon2 before storing in the database.

---

## 2. Login

Endpoint:

```
POST /login
```

Successful login returns a JWT token.

Example:

```json
{
    "access_token": "your_token",
    "token_type": "bearer"
}
```

---

## 3. Access Protected Routes

Send JWT token in request header:

```
Authorization: Bearer <access_token>
```

FastAPI validates the token before allowing access.

---

# API Endpoints

## Users

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/users/` | Create new user |
| GET | `/users/{email}` | Get user details |

---

## Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/login` | User login |

---

## Posts

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/posts/` | Get all posts |
| GET | `/posts/{id}` | Get post by ID |
| POST | `/posts/` | Create post |
| PUT | `/posts/{id}` | Update post |
| DELETE | `/posts/{id}` | Delete post |

---

## Votes

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/vote` | Add or remove vote |

---

# Architecture Overview

```
Client

   |

FastAPI Router

   |

Pydantic Schemas

   |

SQLAlchemy ORM

   |

PostgreSQL Database
```

---

# Security Implementation

Implemented security features:

- JWT Authentication  
- OAuth2 Password Flow  
- Argon2 Password Hashing  
- Environment-based Configuration  
- SQLAlchemy ORM Protection  
- Token Expiration  
- Protected Routes  
- Database Transaction Rollback  

---

# Testing

Run tests:

```bash
pytest
```

---

# Future Improvements

- Refresh token implementation
- Redis caching
- Email verification
- Kubernetes deployment
- Monitoring using Prometheus and Grafana

---

# Author

Jenifer Juliya
