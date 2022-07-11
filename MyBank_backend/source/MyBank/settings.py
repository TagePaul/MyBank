import os
import redis
from datetime import timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-i9rso#_jl5#%n^pq_qj#+l)rauc!6dos^mk3_=m!ez$w-+67*t'

DEBUG = True

# Настройка разрешения по заголовку Origin (домен)
# В Ответе должен быть заголвоок Access-Control-Allow-Origin: https://mysite.com
ALLOWED_HOSTS = ['*'] #####

# [CORS] Расширенная Настройка разрешения по заголовку Origin (домен/протокол/порт)
# установка приложения $ pip install django-cors-headers
# https://pypi.org/project/django-cors-headers/
# Принцип работы CORS:
    # Браузер отправляет запрос на сервер с заголовков Origin: (домен/протокол/порт)
    # В разрешающем ответе должен быть заголвоок Access-Control-Allow-Origin: https://mysite.com
    # Так-же подедерживаются непростые методы и заголовки запроса.
    # Браузер отправляет предзапрос с заголовками Origin:
    #                                             Access-Control-Request-Method: [Методы]
    #                                             Access-Control-Request-Headers [Заголовки]
    # Сервер отвечает с заголовком Access-Control-Allow-Methods: [разрешенные методы]
    #                              Access-Control-Allow-Headers: [Разрешенные заголовки]
    #                              Access-Control-Max-Age: [время кеширования]
    # Если все хорошо, браузер отправляет основной запрос с заголовков Origin: (домен/протокол/порт)
    # Если работа с таким доменом/протоколом/методом/заголовками разрешена
    # Сервер выдает полный ответ с заголовком Access-Control-Allow-Origin https://mysite.com
CORS_ALLOW_ALL_ORIGINS = True # Можно все
# CORS_ALLOWED_ORIGINS = []
# CORS_ALLOW_METHODS = [
#     "DELETE",
#     "GET",
#     "OPTIONS",
#     "PATCH",
#     "POST",
#     "PUT",
# ]
# CORS_ALLOW_HEADERS = []
CSRF_TRUSTED_ORIGINS = []

HOST_NAME = os.environ.get('HOST_NAME','http://localhost:8000')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'user.apps.UserConfig',
    'transaction.apps.TransactionConfig',
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    "corsheaders",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware', # dell
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware', # dell
    'django.contrib.messages.middleware.MessageMiddleware',  # dell
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
       ),
    }

SIMPLE_JWT = {
     'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
     'REFRESH_TOKEN_LIFETIME': timedelta(days=6),
     'ROTATE_REFRESH_TOKENS': True,
     'BLACKLIST_AFTER_ROTATION': True,
     'UPDATE_LAST_LOGIN': False,

     'ALGORITHM': 'HS256',
     'SIGNING_KEY': SECRET_KEY,
     'VERIFYING_KEY': None,
     'AUDIENCE': None,
     'ISSUER': None,
     'JWK_URL': None,
     'LEEWAY': 0,

     'AUTH_HEADER_TYPES': ('Token',),
     'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
     'USER_ID_FIELD': 'id',
     'USER_ID_CLAIM': 'user_id',
     'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

     'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
     'TOKEN_TYPE_CLAIM': 'token_type',

     'JTI_CLAIM': 'jti',

     'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
     'SLIDING_TOKEN_LIFETIME': timedelta(minutes=2),
     'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=7),
   }

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'tagepaul1416@gmail.com'
EMAIL_HOST_PASSWORD = 'cxfusyhrmgwalgjc'
EMAIL_PORT = 587


ROOT_URLCONF = 'MyBank.urls'

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

WSGI_APPLICATION = 'MyBank.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('SQL_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.environ.get('SQL_DATABASE', 'test_work_area2'),
        'USER': os.environ.get('SQL_USER', 'backend_twa1'),
        'PASSWORD': os.environ.get('SQL_PASSWORD', '100101102'),
        'HOST': os.environ.get('SQL_HOST', 'localhost'),
        'PORT': os.environ.get('SQL_PORT', '5432')
    }
}

REDIS_SETTINGS = {
    'host': os.environ.get('REDIS_HOST', 'localhost'),
    'port': os.environ.get('REDIS_PORT', 6379),
    'db': os.environ.get('REDIS_DB', 0)
}

CELERY_BROKER_URL = 'redis://redis:6379'
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
# CELERY_ACCEPT_CONTENT = 'application/json'
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
