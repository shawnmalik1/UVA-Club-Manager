import os
import dj_database_url
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'your-secret-key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['a11-application-e8dd308d0fa2.herokuapp.com', 'localhost', 'project-a-11.com/', '127.0.0.1']

# Application definition
#daphne and channels were used for live chat
INSTALLED_APPS = [
    #'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'a11_project',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'sslserver',
    'storages',
    #'channels'
]

"""
Channel layers for live chat
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}
"""


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Enable Whitenoise for static file handling
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware'
]

ROOT_URLCONF = 'a11_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'a11_project', 'templates')],
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

"""
WSGI_APPLICATION = 'a11_project.wsgi.application'
if 'DATABASE_URL' in os.environ:
     DATABASES = {
         'default': dj_database_url.config(conn_max_age=600, ssl_require=True)
     }
else:
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.postgresql',
             'NAME': os.environ.get('DB_NAME', 'dtvv82sbr485'),  # Correct environment variable or fallback
             'USER': os.environ.get('DB_USER', 'u993vgclb7atte'),  # Correct user from DATABASE_URL
             'PASSWORD': os.environ.get('DB_PASSWORD', 'p9b88dbc0e6622590ab80d3fd12f14ddb9f1ff3d54e5f446885e7446e52e46991'),  # Correct password
             'HOST': os.environ.get('DB_HOST', 'c5p86clmevrg5s.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com'),  # Extracted from DATABASE_URL
             'PORT': os.environ.get('DB_PORT', '5432'),  # Default PostgreSQL port
         }
     }
"""


WSGI_APPLICATION = 'a11_project.wsgi.application'
#ASGI_APPLICATION = "a11_project.asgi.application" #for live chat
if 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.config(conn_max_age=600, ssl_require=True, default = os.environ.get('DATABASE_URL'))
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

SITE_ID = 2
SOCIALACCOUNT_LOGIN_ON_GET = True
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
            'prompt': 'select_account'
        }
    }
}

# Internationalization
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Remove STATICFILES_DIRS if no custom static files exist
# Commenting it out will prevent the directory-not-found warning
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static'),
# ]

# Simplified static file serving with Whitenoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Heroku-specific settings
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'True') == 'True'
# CSRF_COOKIE_SECURE = True

# CSRF trusted origins to allow requests from the Heroku app
CSRF_TRUSTED_ORIGINS = ['https://a11-application-e8dd308d0fa2.herokuapp.com']

# Amazon S3 settings
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = 'AKIAQ3EGVUROLPU3LZSS'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'project-a11-storage'
AWS_S3_REGION_NAME = 'us-east-2'  # Ohio region
AWS_QUERYSTRING_AUTH = False

# S3 Bucket URL and configuration
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None

# Media files storage
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# AWS S3 Storage
AWS_ACCESS_KEY_ID = 'AKIAQ3EGVUROLPU3LZSS'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'project-a11-storage'
AWS_S3_REGION_NAME = 'us-east-2'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None


# Use Amazon S3 for file storage
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Static and Media file configurations (Optional)
#STATIC_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/static/'
MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

TIME_ZONE = 'America/New_York'  # Use your local timezone
USE_TZ = True  # Keep using timezone-aware datetimes

# Daphne

