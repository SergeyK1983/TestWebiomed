import os
from pathlib import Path
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(dotenv_path=os.path.join(BASE_DIR, '.env'))

SECRET_KEY = os.getenv('SECRET_KEY', )

DEBUG = False

if DEBUG:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']
else:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

if DEBUG:
    CSRF_TRUSTED_ORIGINS = ['http://*', 'https://*']
else:
    CSRF_TRUSTED_ORIGINS = ['http://*', 'https://*']

SITE_ID = 1

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.sites',
    'django.contrib.flatpages',

    'corsheaders',
    'drf_yasg',
    'rest_framework',

    'checks.apps.ChecksConfig',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],

    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],

    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],

    'DATETIME_FORMAT': "%d.%m.%Y %H:%M:%S",
}

CORS_ORIGIN_ALLOW_ALL = True  # added to solve CORS
CORS_ALLOW_HEADERS = ('content-disposition', 'accept-encoding',
                      'content-type', 'accept', 'origin', 'Authorization',
                      'access-control-allow-methods', 'access-control-allow-origin',
                      'access-control-allow-credentials', 'attribution-reporting',
                      )

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
]

ROOT_URLCONF = 'producer.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'producer.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('HOST'),
        'PORT': os.getenv('PORT', '5432')
    }
}

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


# Internationalization
LANGUAGE_CODE = 'ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = '/var/www/producer/static'

MEDIA_URL = '/media/'
if DEBUG:
    MEDIA_ROOT = BASE_DIR / 'media'
else:
    MEDIA_ROOT = '/var/www/producer/media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Логирование
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'general_log_info': {
            'format': '{asctime} - {levelname} - {module} - {message}',
            'style': '{',
        },
        'error_log': {
            'format': '{asctime} - {levelname} - {pathname} - {exc_info} - {message}',
            'style': '{',
        },
        'security_log': {
            'format': '{asctime} - {levelname} - {module} - {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',  # фильтр, который пропускает записи только в случае, когда DEBUG = True
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',  # фильтр, который пропускает записи только в случае, когда DEBUG = False
        },
    },
    # Обработчики
    'handlers': {
        'file_general.log': {
            'level': 'INFO',
            'filters': ['require_debug_false'],
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'general.log',
            'formatter': 'general_log_info',
        },
        'file_errors.log': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'errors.log',
            'formatter': 'error_log',
        },
        'file_security.log': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'security.log',
            'formatter': 'security_log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file_general.log'],
            # 'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['file_errors.log'],
            'level': "ERROR",
            'propagate': False,
        },
        'django.server': {
            'handlers': ['file_errors.log'],
            'propagate': True,
        },
        'django.template': {
            'handlers': ['file_errors.log'],
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['file_errors.log'],
            'propagate': False,
        },
        'django.security': {
            'handlers': ['file_security.log'],
            'propagate': False,
        },
    },
}
