# 📚 Library DRF Backend

A REST API for a library management system built with **Django REST Framework**.

🔗 **Repository:** https://github.com/HamsterKate/library-drf-backend

---

## 🛠️ Technologies

<p>
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Django-6.x-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/Django_REST_Framework-API-A30000?style=for-the-badge&logo=django&logoColor=white" alt="Django REST Framework">
  <img src="https://img.shields.io/badge/PostgreSQL-17-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/JWT-Authentication-black?style=for-the-badge" alt="JWT">
  <img src="https://img.shields.io/badge/OpenAPI-Swagger-85EA2D?style=for-the-badge&logo=swagger&logoColor=black" alt="Swagger">
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
├── .env
├── .env.sample
├── .gitignore
├── manage.py
├── requirements.txt
└── README.md
```

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/HamsterKate/library-drf-backend.git
cd library-drf-backend
```

### 2. Create a virtual environment

#### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root based on `.env.sample`.

> 🔐 Never commit `.env` or any secret values to the repository.

### 5. Apply migrations

```bash
python manage.py migrate
```

### 6. Create a superuser

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

The API will be available at:

```text
http://127.0.0.1:8000/
```

---

## 🗄️ Database

🐘 The project uses **PostgreSQL** as the database.

Before running the project, make sure PostgreSQL is installed and running and that the database credentials in `.env` are configured correctly.

---

## 📚 API Documentation

Interactive API documentation is available through **Swagger UI**:

👉 http://127.0.0.1:8000/api/docs/

OpenAPI schema:

👉 http://127.0.0.1:8000/api/schema/

Alternative documentation with **ReDoc**:

👉 http://127.0.0.1:8000/api/docs/redoc/

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

Run all tests with:

```bash
python manage.py test
```

You can also run tests for a specific application:

```bash
python manage.py test tests.test_books
python manage.py test tests.test_users
python manage.py test tests.test_borrowings
python manage.py test tests.test_payments
```


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
