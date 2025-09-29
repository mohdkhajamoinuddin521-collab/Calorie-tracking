import os
import dj_database_url
from .settings import *  # import base settings
from .settings import BASE_DIR

# ------------------------------------------------------------------------------
# SECURITY & DEBUG
# ------------------------------------------------------------------------------
DEBUG = False   # ✅ Keep False in production
SECRET_KEY = os.environ.get("SECRET_KEY")

# ------------------------------------------------------------------------------
# HOSTS & ORIGINS
# ------------------------------------------------------------------------------
ALLOWED_HOSTS = [
    os.environ.get("RENDER_EXTERNAL_HOSTNAME"),   # backend render service
    "calorie-tracking-frontend.onrender.com",     # frontend render site
]

CSRF_TRUSTED_ORIGINS = [
    f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}",
    "https://calorie-tracking-frontend.onrender.com",
]

# Allow CORS for React frontend
CORS_ALLOWED_ORIGINS = [
    "https://calorie-tracking-frontend.onrender.com",
]

# ------------------------------------------------------------------------------
# MIDDLEWARE
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    # 👇 CORS should be high in the list, before CommonMiddleware
    "corsheaders.middleware.CorsMiddleware",

    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ------------------------------------------------------------------------------
# STATIC FILES
# ------------------------------------------------------------------------------
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

# ------------------------------------------------------------------------------
# DATABASE
# ------------------------------------------------------------------------------
DATABASES = {
    "default": dj_database_url.config(
        default=os.environ["DATABASE_URL"],
        conn_max_age=600,
        ssl_require=True,   # ✅ enforce SSL for Render Postgres
    )
}
