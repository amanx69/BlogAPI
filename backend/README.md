# 📝 Blog API

A fully-featured RESTful Blog API built with **Django REST Framework**, secured with **JWT Authentication**, and powered by **Celery** for asynchronous background tasks like email verification.

---

## 🚀 Features

- 🔐 JWT-based Authentication (Register, Login, Logout, Token Refresh)
- ✉️ Email Verification via Celery background tasks
- 📝 Full CRUD for Blog Posts
- 💬 Comments on Posts
- 🏷️ Categories & Tags
- 👤 User Profile Management
- 🔒 Permission-based Access Control
- 🌐 CORS Support

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Framework | Django 4.x + Django REST Framework |
| Auth | JWT (`djangorestframework-simplejwt`) |
| Task Queue | Celery |
| Message Broker | Redis |
| Database | PostgreSQL |
| Email | SMTP / Django Email Backend |
| Environment | python-decouple / dotenv |


## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/amanx69/BlogAPI.git
cd BlogAPI
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
touch .env # in linux
```

Edit `.env` with your configuration:

```env
# Django
SECRET_KEY=your-secret-key



# JWT
ACCESS_TOKEN_LIFETIME_MINUTES=60
REFRESH_TOKEN_LIFETIME_DAYS=7

# Redis (Celery Broker)
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Email
email_b=django.core.mail.backends.smtp.EmailBackend
email_h=smtp.gmail.com
email_port=587
EMAIL_USE_TLS=True
email_host=your-email@gmail.com
email_pass=your-app-password
DEFAULT_FROM_EMAIL=Blog API <your-email@gmail.com>


```

### 5. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a superuser

```bash
python manage.py createsuperuser
```

### 7. Start Redis (required for Celery)


#  Redis is installed locally
redis-server
```

### 8. Start the Celery worker

```bash
celery -A config worker --loglevel=info
```

### 9. Run the development server

```bash
python manage.py runserver
```

---

## 🔑 Authentication Flow

```
POST /api/auth/signup/        → Triggers Celery task to send verification email
GET  /api/auth/verify-email/<uid><token>    → Verifies token from email link
POST /api/auth/login/           → Returns access + refresh JWT tokens
POST /api/auth/token/refresh/   → Refresh access token
POST /api/auth/Logout/          → Blacklist refresh token
```


## 👤 Author

**Aman**
- GitHub: [@amanx69](https://github.com/amanx69)
- Email: anujaman56gmail.com