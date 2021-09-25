import os
from datetime import timedelta
from pathlib import Path

from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv

load_dotenv()

ENV = os.environ

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = ENV['SECRET_KEY']

DEBUG = int(ENV.get('DJANGO_DEVELOPMENT', False))

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '*', 'web:8000']

CORS_ORIGIN_ALLOW_ALL = True
CORS_URLS_REGEX = r'^/api/.*$'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_apscheduler',
    'rest_framework',
    'django_filters',
    'corsheaders',
    'drf_yasg',
    'api',
    'account',
    'admin_honeypot',
    'martor',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

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

WSGI_APPLICATION = 'project.wsgi.application'


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# User model

AUTH_USER_MODEL = 'account.CustomUser'


# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': ('django.contrib.auth.password_validation.'
                 'UserAttributeSimilarityValidator'),
    },
    {
        'NAME': ('django.contrib.auth.password_validation.'
                 'MinimumLengthValidator'),
    },
    {
        'NAME': ('django.contrib.auth.password_validation.'
                 'CommonPasswordValidator'),
    },
    {
        'NAME': ('django.contrib.auth.password_validation.'
                 'NumericPasswordValidator'),
    },
]


# Internationalization

LANGUAGE_CODE = ENV.get('LANGUAGE_CODE', default='ru-Ru')

TIME_ZONE = ENV.get('TIME_ZONE', default='UTC')

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Rest framework

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
        'djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer',
    ),

    'DEFAULT_PARSER_CLASSES': (
        'djangorestframework_camel_case.parser.CamelCaseFormParser',
        'djangorestframework_camel_case.parser.CamelCaseMultiPartParser',
        'djangorestframework_camel_case.parser.CamelCaseJSONParser',
    ),

    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),

    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
    ],

    'DEFAULT_PAGINATION_CLASS': (
        'rest_framework.pagination.PageNumberPagination'
    ),

    'PAGE_SIZE': 10,
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),
}

MAX_TAGS_COUNT = 4
MAX_IMAGE_UPLOAD_SIZE_MB = 10
MAX_IMAGE_UPLOAD_SIZE = MAX_IMAGE_UPLOAD_SIZE_MB * 1024 * 1024
IMAGE_EXTENSIONS = ('jpg', 'jpeg', 'gif', 'png', 'bmp')

IMAGE_FIELD_HELP_TEXT = _(
    f'Поддерживаемые форматы {", ".join(IMAGE_EXTENSIONS)}. Размер до {MAX_IMAGE_UPLOAD_SIZE_MB} Мб.' # noqa(501)
)


ADMIN_HONEYPOT_EMAIL_ADMINS = False


# Mail Backend

MAIL_API = ENV.get('MAIL_API')
MAIL_API_KEY = ENV.get('MAIL_API_KEY')
FROM_MAIL = ENV.get('FROM_MAIL')


# Scheduler

APSCHEDULER_DATETIME_FORMAT = 'd.m.Y H:i:s'


# Martor settings

MARTOR_THEME = 'bootstrap'

MARTOR_ENABLE_CONFIGS = {
    'emoji': 'true',
    'imgur': 'false',
    'mention': 'false',
    'jquery': 'true',
    'living': 'false',
    'spellcheck': 'false',
    'hljs': 'true',
}

MARTOR_TOOLBAR_BUTTONS = [
    'bold', 'italic', 'horizontal', 'heading', 'pre-code',
    'blockquote', 'unordered-list', 'ordered-list',
    'link', 'image-link', 'emoji',
    'direct-mention', 'toggle-maximize', 'help'
]
