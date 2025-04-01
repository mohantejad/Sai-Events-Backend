from datetime import timedelta
import os
from dotenv import load_dotenv
from pathlib import Path
import dj_database_url

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
DEBUG = os.getenv("DEBUG", "False") == "True"
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS').split(' ')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'djoser',
    'corsheaders',
    'django_extensions',

    'users.apps.UsersConfig',
    'events.apps.EventsConfig'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'main.wsgi.application'

if DEBUG:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "sai_events_db",
            "USER": "postgres",
            "PASSWORD": "realestate_db_password",
            "HOST": "localhost",
            "PORT": "5432",
        }
    }
else:
    DATABASE_URL = os.getenv("DATABASE_PUBLIC_URL")
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600
        )
    }


AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'
FILE_UPLOAD_PERMISSIONS = 0o640
if not DEBUG:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'users.authentication.CustomJWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),

}

DOMAIN = os.getenv('DOMAIN')
SITE_NAME = os.getenv('SITE_NAME')

EMAIL_BACKEND = 'django_ses.SESBackend'
DEFAULT_FROM_EMAIL = os.getenv('AWS_SES_FROM_EMAIL')
AWS_SES_ACCESS_KEY_ID = os.getenv('AWS_SES_ACCESS_KEY_ID')
AWS_SES_SECRET_ACCESS_KEY = os.getenv('AWS_SES_SECRET_ACCESS_KEY')
AWS_SES_REGION_NAME = os.getenv('AWS_SES_REGION')
AWS_SES_REGION_ENDPOINT = f'email.{AWS_SES_REGION_NAME}.amazonaws.com'
USE_SES_V2 = True

DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': 'reset-password/{uid}/{token}',
    'USERNAME_RESET_CONFIRM_URL': 'reset-username/{uid}/{token}',
    'EMAIL_FRONTEND_DOMAIN': 'fancigadgets',
    'EMAIL_FRONTEND_SITE_NAME': 'Fanci Gadgets',
    'SEND_ACTIVATION_EMAIL': True,
    'SEND_CONFIRMATION_EMAIL': True,
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION': True,
    'USERNAME_CHANGED_EMAIL_CONFIRMATION': True,
    'ACTIVATION_URL': 'activate-account/{uid}/{token}',
    'USER_CREATE_PASSWORD_RETYPE': True,
    'SET_USERNAME_RETYPE': True,
    'SET_PASSWORD_RETYPE': True,
    'PASSWORD_RESET_CONFIRM_RETYPE': True,
    'USERNAME_RESET_CONFIRM_RETYPE': True,
    'PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND': True,
    'USERNAME_RESET_SHOW_EMAIL_NOT_FOUND': True,
    'TOKEN_MODEL': None,
    # 'SOCIAL_AUTH_ALLOWED_REDIRECT_URIS': os.getenv('REDIRECT_URLS').split(','),
    'SERIALIZERS': {
        'current_user': 'users.serializers.CurrentUserSerializer',
        'user_create': 'users.serializers.UserCreateSerializer',
        'user': 'users.serializers.UserSerializer',
    },
    'EMAIL': {
        'activation': 'users.emails.ActivationEmail',
        'confirmation': 'users.emails.ConfirmationEmail',
    },
}

AUTH_COOKIE = 'access'
AUTH_COOKIE_ACCESS_MAX_AGE = 60 * 60 * 24
AUTH_COOKIE_REFRESH_MAX_AGE = 60 * 60 * 24 * 5
AUTH_COOKIE_SECURE = os.getenv('AUTH_COOKIE_SECURE')
AUTH_COOKIE_HTTP_ONLY = True
AUTH_COOKIE_PATH = '/'
AUTH_COOKIE_SAME_SITE = 'None'
CORS_ALLOW_CREDENTIALS = True
CSRF_COOKIE_SECURE = True

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('JWT',),
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=3),
}

CSRF_TRUSTED_ORIGINS = [
    'https://event-manager-backend-production-c3c4.up.railway.app',
]

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'https://event-manager-backend-production-c3c4.up.railway.app',
]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'users.User'
