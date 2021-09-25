from datetime import timedelta
from os import environ
from pathlib import Path

from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv

load_dotenv()

ENV = environ

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = ENV['SECRET_KEY']

DEBUG = int(ENV.get('DJANGO_DEVELOPMENT', False))

ADMINS = [('BBBS_team', ENV.get('EMAIL_HOST_USER')), ]

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
    'rest_framework',
    'django_filters',
    'corsheaders',
    'drf_yasg',
    'afisha',
    'api',
    'account',
    'common',
    'admin_honeypot',
    'martor',
    'phonenumber_field',
    'django_cron',
]

CRON_CLASSES = [
    'api.cron.EventCanceled',
    'api.cron.EventReminder',
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
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': ENV['POSTGRES_DB'],
        'USER': ENV.get('POSTGRES_USER', 'user'),
        'PASSWORD': ENV.get('POSTGRES_PASSWORD', 'password'),
        'HOST': ENV.get('DB_HOST', 'db'),
        'PORT': ENV.get('DB_PORT', 5432),
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

PHONENUMBER_DEFAULT_REGION = 'RU'

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


# Main page

MAIN_ARTICLES_LENGTH = int(ENV.get('MAIN_ARTICLES_LENGTH', 2))
MAIN_QUESTION_LENGTH = int(ENV.get('MAIN_QUESTION_LENGTH', 10))
MAIN_MOVIES_LENGTH = int(ENV.get('MAIN_MOVIES_LENGTH', 7))


MAX_TAGS_COUNT = 4

DJANGORESIZED_DEFAULT_SIZE = [1920, 1080]
DJANGORESIZED_DEFAULT_QUALITY = 100
DJANGORESIZED_DEFAULT_FORCE_FORMAT = 'JPEG'
DJANGORESIZED_DEFAULT_FORMAT_EXTENSIONS = {'JPEG': '.jpg'}
MAX_IMAGE_UPLOAD_SIZE_MB = 10
MAX_IMAGE_UPLOAD_SIZE = MAX_IMAGE_UPLOAD_SIZE_MB * 1024 * 1024
IMAGE_EXTENSIONS = ('jpg', 'jpeg', 'gif', 'png', 'bmp')

IMAGE_FIELD_HELP_TEXT = _(
    f'Поддерживаемые форматы {", ".join(IMAGE_EXTENSIONS)}. Размер до {MAX_IMAGE_UPLOAD_SIZE_MB} Мб.' # noqa E501
)


ADMIN_HONEYPOT_EMAIL_ADMINS = False


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
    'bold', 'italic', 'horizontal', 'heading', 'blockquote',
    'unordered-list', 'link', 'emoji', 'toggle-maximize', 'help',
]

# Mail

EMAIL_SUBJECT_PREFIX = 'BBBS: '
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = ENV.get('EMAIL_HOST')
EMAIL_HOST_USER = ENV.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = ENV.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT = int(ENV.get('EMAIL_PORT', default=587))
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

SERVER_EMAIL = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

EMAIL_SEND_TIMEOUT = int(ENV.get('EMAIL_SEND_TIMEOUT', 10))

USER_CREATION_SUBJECT = ENV.get('USER_CREATION_SUBJECT', _('Регистрация на сайте BBBS'))
USER_CREATION_MESSAGE = ENV.get('USER_CREATION_MESSAGE', _('Вас зарегестрировали на сайте BBBS. Используйте логин %s и пароль %s для входа на сайт.'))

USER_PASSWORD_CHANGE_SUBJECT = ENV.get('USER_PASSWORD_CHANGE_SUBJECT', _('Изменение пароля для сайта BBBS'))
USER_PASSWORD_CHANGE_MESSAGE = ENV.get('USER_PASSWORD_CHANGE_MESSAGE', _('Ваш пароль для BBBS был изменён. Используйте новый пароль %s для входа на сайт.'))

SEND_DIARY_TO_CURATOR_SUBJECT = ENV.get('SEND_DIARY_TO_CURATOR_SUBJECT', _('%s: запись в дневнике от %s'))
