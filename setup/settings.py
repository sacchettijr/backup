# Django 4.0.3.
import os
from pathlib import Path
from django.contrib.messages import constants as messages_constants

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-&mho4j!!-hy!x4r#7^*g5x@3g!d3gao7dz)%=iv++=pj6j0ge+'
DEBUG = True
ALLOWED_HOSTS = []
INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	# DJANGO REST FRAMEWORK
	'rest_framework',
	'rest_framework.authtoken',
	'django_filters',
	'guardian',
	# BIBLIOTECAS
	'debug_toolbar',
	'widget_tweaks',
	# APP
	'core',
]

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'setup.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': ['templates'],
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

WSGI_APPLICATION = 'setup.wsgi.application'

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': BASE_DIR / 'db.sqlite3',
	}
}

AUTH_PASSWORD_VALIDATORS = [
	{'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
	{'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
	{'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
	{'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

REST_FRAMEWORK = {
	'DEFAULT_PERMISSION_CLASSES': [
		'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
	],
	'DEFAULT_AUTHENTICATION_CLASSES': [
		'rest_framework.authentication.BasicAuthentication',
		'rest_framework.authentication.SessionAuthentication',
	]
}

AUTHENTICATION_BACKENDS = (
	'django.contrib.auth.backends.ModelBackend',  # default
	'guardian.backends.ObjectPermissionBackend',
)

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Manaus'
USE_I18N = True
USE_TZ = False
HTML_MINIFY = True
AUTH_USER_MODEL = 'core.Usuario'
LOGIN_REDIRECT_URL = 'index'
LOGOUT_REDIRECT_URL = 'index'

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MESSAGE_TAGS = {
	messages_constants.SUCCESS: 'success',
	messages_constants.WARNING: 'warning',
	messages_constants.ERROR: 'danger',
	messages_constants.INFO: 'info',
	messages_constants.DEBUG: 'debug',
}

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



INTERNAL_IPS = [
	'127.0.0.1',
]
