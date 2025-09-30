import os
import dj_database_url
from .settings import *
from .settings import BASE_DIR 

DEBUG = False  # better for Render

SECRET_KEY = os.environ.get('SECRET_KEY')

ALLOWED_HOSTS = [
    "calorie-tracker-app.onrender.com",
    "calorie-tracking-frontend.onrender.com",
]

CSRF_TRUSTED_ORIGINS = [
    "https://calorie-tracker-app.onrender.com",
    "https://calorie-tracking-frontend.onrender.com",
]

# ---- CORS ----
CORS_ALLOW_ALL_ORIGINS = True  # test only
# Later replace with:
# CORS_ALLOWED_ORIGINS = ["https://calorie-tracking-frontend.onrender.com"]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ['DATABASE_URL'],
        conn_max_age=600
    )
}
