import os
from config.env import env, BASE_DIR

env.read_env(os.path.join(BASE_DIR, ".env"))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY", default='=ug_ucl@yi6^mrcjyz%(u0%&g2adt#bz3@yos%#@*t#t!ypx=a')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", default=True)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*'])


# Application definition
LOCAL_APPS = [
    'blog_version2.core.apps.CoreConfig',
    'blog_version2.common.apps.CommonConfig',
    'blog_version2.users.apps.UsersConfig',
    'blog_version2.authentication.apps.AuthenticationConfig',
    'blog_version2.home.apps.HomeConfig',
    
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'django_filters',
    'django_celery_results',
    'django_celery_beat',
    'corsheaders',
    'drf_spectacular',
    'django_extensions',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # http://whitenoise.evans.io/en/stable/django.html#using-whitenoise-in-development
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    *THIRD_PARTY_APPS,
    *LOCAL_APPS,
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': env.db('DATABASE_URL', default='psql://parham:paripari85@127.0.0.1:5432/blog_version2'),
}
DATABASES['default']['ATOMIC_REQUESTS'] = True

if os.environ.get('GITHUB_WORKFLOW'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'github_actions',
            'USER': 'parham',
            'PASSWORD': 'paripari85',
            'HOST': '127.0.0.1',
            'PORT': '5432',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
    
    {'NAME': 'blog_version2.users.validators.NumberValidator'},
    {'NAME': 'blog_version2.users.validators.LetterValidator'},
    {'NAME': 'blog_version2.users.validators.SpecialCharValidator'},
]

AUTH_USER_MODEL = 'users.BaseUser'

# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'EXCEPTION_HANDLER': 'blog_version2.api.exception_handlers.drf_default_with_modifications_exception_handler',
    # 'EXCEPTION_HANDLER': 'blog_version2.api.exception_handlers.hacksoft_proposed_exception_handler',
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': []
}


# Redis
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': env("REDIS_LOCATION", default="redis://localhost:6379"),
    }
}
# Cache time to live is 15 minutes.
CACHE_TTL = 60 * 15


APP_DOMAIN = env("APP_DOMAIN", default="http://localhost:8000")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

{'NAME': 'blog_version2.users.validators.NumberValidator'},
{'NAME': 'blog_version2.users.validators.LetterValidator'},
{'NAME': 'blog_version2.users.validators.SpecialCharValidator'},

CSRF_SESSION_KEY = "yourrandomsecretkey"
WTF_CSRF_ENABLED = True
WTF_CSRF_SECRET_KEY = "yourrandomsecretkey"
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0", "*"]


from config.settings.cors import *  # noqa
from config.settings.jwt import *  # noqa
from config.settings.sessions import *  # noqa
from config.settings.celery import *  # noqa
from config.settings.swagger import *  # noqa
#from config.settings.sentry import *  # noqa
#from config.settings.email_sending import *  # noqa