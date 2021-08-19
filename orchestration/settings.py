"""
Django settings for orchestration project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from os import environ
from dotenv import load_dotenv

from corsheaders.defaults import default_headers

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Environment Variable Setup
load_dotenv()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-#lb@63a1u&0-j5v+h+q7w+11&--45ab4_(pz388b$2y8ln6s!7"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# CORS
CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_HEADERS = list(default_headers) + [
    "sentry-trace",
]

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    "strategy",
    "authentication",
    "orchestrator",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    # django rest framework
    "rest_framework",
    "rest_framework.authtoken",
    "rest_auth",
    # django celery
    "django_celery_results",
    # for social login
    "allauth",
    "allauth.account",
    "rest_auth.registration",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "corsheaders",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    # 'django.middleware.csrf.CsrfViewMiddleware',
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "orchestration.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "orchestration.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": environ["DATABASE_NAME"],
        "USER": environ["DATABASE_USER"],
        "PASSWORD": environ["DATABASE_PASSWORD"],
        "HOST": environ["DATABASE_HOST"],
        "PORT": environ["DATABASE_PORT"],
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SITE_ID = 1

ROOT_URLCONF = "orchestration.urls"
WSGI_APPLICATION = "orchestration.wsgi.application"

# Celery

# Make this a shared result backend
CELERY_RESULT_BACKEND = f'db+postgresql://{environ["DATABASE_USER"]}:{environ["DATABASE_PASSWORD"]}@{environ["DATABASE_HOST"]}:{environ["DATABASE_PORT"]}/{environ["CELERY_BACKEND_DATABASE_NAME"]}'
CELERY_CACHE_BACKEND = 'django-cache'
CELERY_BROKER_URL = environ["RABBIT_MQ_URL"]

CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'