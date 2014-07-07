# coding: utf-8
import os
from settings_defaults import *  # DO NOT delete, there are default settings!

SITE_ID = 0

SITE_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
WWW_ROOT = os.path.join(SITE_ROOT, 'wwwroot')

DEBUG = True
TEMPLATE_DEBUG = DEBUG
USE_DEBUG_TOOLBAR = True

ALLOWED_HOST = '{{ project_name }}.picassoft.com.ua'
ALLOWED_HOSTS = [
    'localhost',
    '.{}'.format(ALLOWED_HOST),  # Allow domain and subdomains
    '.{}.'.format(ALLOWED_HOST),  # Also allow FQDN and subdomains
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '{{ project_name }}',                      # Or path to database file if using sqlite3.
        'USER': 'postgres',                      # Not used with sqlite3.
        'PASSWORD': 'c',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

TIME_ZONE = 'Europe/Kiev'
LANGUAGE_CODE = 'uk'
USE_I18N = True
USE_L10N = True
USE_TZ = True

MEDIA_ROOT = os.path.join(WWW_ROOT, 'media')
MEDIA_URL = '/media/'

DEFAULT_FILE_STORAGE = 'picassoft.files.storage.HashedFileSystemStorage'

STATIC_ROOT = os.path.join(WWW_ROOT, 'static')
STATIC_SOURCE = os.path.join(SITE_ROOT, 'static')
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'
STATICFILES_DIRS = (
    STATIC_SOURCE,
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '{{ secret_key }}'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.i18n',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

if USE_DEBUG_TOOLBAR:
    MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )

# After DebugToolbarMiddleware to show SQL queries.
MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + (
    'django.middleware.http.ConditionalGetMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
)

ROOT_URLCONF = '{{ project_name }}.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = '{{ project_name }}.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(SITE_ROOT, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.webdesign',

    'debug_toolbar',
    'django_extensions',
    'south',
    #'media_bundler',
    #'sorl.thumbnail',
    #'paging',
    #'modeltranslation',
    #'rosetta',
    #'feincms',
    #'mptt',
    #'haystack',

    'picassoft.utils',
    'picassoft.sprite_bundler',

)

# Debug Bar settings
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

# Cache settings
CACHE_MIDDLEWARE_KEY_PREFIX = os.path.split(SITE_ROOT)[1]
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Languages settings
_ = lambda s: s
LANGUAGES = (
    ('uk', _("Ukrainian")),
    ('ru', _("Russian")),
)

LOCALE_PATHS = os.path.join(SITE_ROOT, 'locale'),

# Media bundles settings, using only for sprites
MEDIA_BUNDLES_SOURCE = os.path.join(STATIC_SOURCE, 'sprites')
MEDIA_BUNDLES = {
    'type': 'png-sprite',
    'name': 'sprites',
    'path': MEDIA_BUNDLES_SOURCE,
    'url': STATIC_URL + 'images/',
    'css_file': os.path.join(STATIC_SOURCE, 'css', 'sprites.css'),
    'files': [f for f in os.listdir(MEDIA_BUNDLES_SOURCE) if not f.startswith('sprites')],
},

USE_BUNDLES = False

# Thumbnail settings
THUMBNAIL_DEBUG = DEBUG

THUMBNAIL_STORAGE = 'django.core.files.storage.FileSystemStorage'  # Set explicitly to override default storage

THUMBNAIL_SETTINGS = {
    'FULLSCREEN': ('1200', {'upscale': False}),  # (geometry, options)
    'PAGE_IMAGE': ('WIDTHxHEIGHT', {'crop': 'center'}),
}

# Search settings
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.xapian_backend.XapianEngine',
        'PATH': os.path.join(SITE_ROOT, 'index', 'xapian'),
        'INCLUDE_SPELLING': True,
    },
}
