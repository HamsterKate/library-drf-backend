# 📚 Library DRF Backend

A REST API for a library management system built with **Django REST Framework**.

🔗 **Repository:** https://github.com/HamsterKate/library-drf-backend

---

## 🛠️ Technologies

<p>
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Django-6.1-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/Django_REST_Framework-API-A30000?style=for-the-badge&logo=django&logoColor=white" alt="Django REST Framework">
  <img src="https://img.shields.io/badge/PostgreSQL-17-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/JWT-Authentication-black?style=for-the-badge" alt="JWT">
  <img src="https://img.shields.io/badge/OpenAPI-Swagger-85EA2D?style=for-the-badge&logo=swagger&logoColor=black" alt="Swagger">
  <img src="https://img.shields.io/badge/Docker-Containerization-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
</p>

---

## ✨ Features

### 📖 Books

* Full CRUD functionality
* All users, including unauthenticated users, can list books
* Only admin users can create, update and delete books

### 👤 Users & Authentication

* User CRUD functionality
* User authentication with email and password
* JWT access and refresh tokens
* Separate permissions for regular and admin users

### 📚 Borrowings

* Borrowing list and detail endpoints
* Create a borrowing with inventory validation
* Automatically decrease book inventory when a book is borrowed
* Automatically assign the current user to the borrowing
* Filtering by active borrowings
* Users can see only their own borrowings
* Admins can see all users' borrowings
* Admin filtering by `user_id`
* Borrowing return functionality
* Prevent returning the same borrowing twice
* Automatically increase book inventory after a return

### 💳 Payments

* Payment model
* Payment list and detail endpoints
* Regular users can see only their own payments
* Admin users can see all payments

---

## 📁 Project Structure

```text
library-drf-backend/
│
├── books/
├── users/
├── borrowings/
├── payments/
├── tests/
│   ├── test_books.py
│   ├── test_users.py
│   ├── test_borrowings.py
│   └── test_payments.py
│
├── library_service/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── .dockerignore
├── .env
├── .env.sample
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── manage.py
├── requirements.txt
└── README.md
```

> `.env` is used for environment variables and must not be committed to the repository.

---

## 🚀 Installation

### 🐳 Option 1: Run with Docker

Make sure **Docker Desktop** is installed and running.

#### 1. Clone the repository

```bash
git clone https://github.com/HamsterKate/library-drf-backend.git
cd library-drf-backend
```

#### 2. Configure environment variables

Create a `.env` file in the project root based on `.env.sample`.

> 🔐 Never commit `.env` or any secret values to the repository.

#### 3. Build and start the containers

```bash
docker compose up --build
```

The application will be available at:

```text
http://localhost:8000/
```

#### 4. Apply migrations

Open a new terminal in the project directory and run:

```bash
docker compose exec web python manage.py migrate
```

#### 5. Create a superuser

```bash
docker compose exec web python manage.py createsuperuser
```

#### 6. Stop the containers

```bash
docker compose down
```

---

### 💻 Option 2: Run locally

#### 1. Clone the repository

```bash
git clone https://github.com/HamsterKate/library-drf-backend.git
cd library-drf-backend
```

#### 2. Create a virtual environment

**Windows**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux / macOS**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### 3. Install dependencies

```bash
pip install -r requirements.txt
```

#### 4. Configure environment variables

Create a `.env` file in the project root based on `.env.sample`.

For local development, configure PostgreSQL with:

```text
DB_HOST=localhost
```

> 🔐 Never commit `.env` or any secret values to the repository.

#### 5. Make sure PostgreSQL is installed and running

The project uses **PostgreSQL 17**.

Make sure PostgreSQL is running and that the database credentials in `.env` are configured correctly.

#### 6. Apply migrations

```bash
python manage.py migrate
```

#### 7. Create a superuser

```bash
python manage.py createsuperuser
```

#### 8. Run the development server

```bash
python manage.py runserver
```

The API will be available at:

```text
http://127.0.0.1:8000/
```

---

## 🐳 Docker

The project includes Docker support for running the Django application together with PostgreSQL.

The Docker setup includes:

* `Dockerfile` for building the Django application image
* `docker-compose.yml` for running Django and PostgreSQL containers
* `.dockerignore` for excluding unnecessary files from the Docker build context
* PostgreSQL data persistence using a Docker volume

The Docker setup consists of:

```text
┌──────────────────────┐
│   Django container   │
│        web           │
│      port 8000       │
└──────────┬───────────┘
           │
           │
┌──────────▼───────────┐
│ PostgreSQL container │
│         db           │
│      port 5432       │
└──────────────────────┘
```

Build and start the application:

```bash
docker compose up --build
```

Apply migrations:

```bash
docker compose exec web python manage.py migrate
```

Run tests inside the Docker container:

```bash
docker compose exec web python manage.py test
```

Stop the containers:

```bash
docker compose down
```

---

## 🗄️ Database

🐘 The project uses **PostgreSQL 17** as the database.

When running with Docker, PostgreSQL runs in a separate Docker container and its data is stored in a Docker volume.

When running locally, PostgreSQL must be installed and running on the host machine.

---

## 📚 API Documentation

Interactive API documentation is available through **Swagger UI**:

👉 http://localhost:8000/api/docs/

OpenAPI schema:

👉 http://localhost:8000/api/schema/

Alternative documentation with **ReDoc**:

👉 http://localhost:8000/api/docs/redoc/

---

## 🔐 Authentication

The API uses **JWT authentication**.

### Obtain tokens

```http
POST /api/token/
```

### Refresh access token

```http
POST /api/token/refresh/
```

Use the access token when making authenticated requests.

---

## 🧪 Tests

The project uses **`TestCase`-based tests** together with Django REST Framework test utilities.

Run all tests locally with:

```bash
python manage.py test
```

Run all tests inside Docker:

```bash
docker compose exec web python manage.py test
```

You can also run tests for a specific application:

```bash
python manage.py test tests.test_books
python manage.py test tests.test_users
python manage.py test tests.test_borrowings
python manage.py test tests.test_payments
```

The project currently contains **53 tests**, all passing successfully.

---

## 📌 Implemented Coding Tasks

This project includes the following implemented tasks from the Coding section:

1. ✅ Books CRUD
2. ✅ Books permissions
3. ✅ Users CRUD & JWT authentication
4. ✅ Borrowing List & Detail
5. ✅ Create Borrowing
6. ✅ Borrowings filtering
7. ✅ Return Borrowing
8. ✅ Payments List & Detail

---

## 👩‍💻 Author

**HamsterKate**

🔗 GitHub: https://github.com/HamsterKate