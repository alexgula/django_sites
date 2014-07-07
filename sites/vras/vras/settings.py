# coding: utf-8
# Django settings for vras project.
import os
from settings_defaults import * # DO NOT delete, there are default settings!

SITE_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
WWW_ROOT = os.path.join(SITE_ROOT, 'wwwroot')

DEBUG = True
TEMPLATE_DEBUG = DEBUG
USE_DEBUG_TOOLBAR = True

ALLOWED_HOST = 'vras.com.ua'
ALLOWED_SUBDOMAIN = 'vras.picassoft.com.ua'
ALLOWED_HOSTS = [
    'localhost',
    '.{}'.format(ALLOWED_HOST),  # Allow domain and subdomains
    '.{}.'.format(ALLOWED_HOST),  # Also allow FQDN and subdomains
    '.{}'.format(ALLOWED_SUBDOMAIN),  # Allow domain and subdomains
    '.{}.'.format(ALLOWED_SUBDOMAIN),  # Also allow FQDN and subdomains
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'vras',                      # Or path to database file if using sqlite3.
        'USER': 'postgres',                      # Not used with sqlite3.
        'PASSWORD': 'c',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Kiev'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'uk'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(WWW_ROOT, 'media')
DEFAULT_FILE_STORAGE = 'picassoft.files.storage.HashedFileSystemStorage'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(WWW_ROOT, 'static')
STATIC_SOURCE = os.path.join(SITE_ROOT, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    STATIC_SOURCE,
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '!_d@x7ir*$b#y+e&i93%eg@o&8my!##6qj=o--*k*c1+f6u&80'

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
    'mediatools.context_processors.thumbnail_settings',
)

MIDDLEWARE_CLASSES = (
#    'django.middleware.cache.UpdateCacheMiddleware',
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
#    'django.middleware.cache.FetchFromCacheMiddleware',
)

ROOT_URLCONF = 'vras.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'vras.wsgi.application'

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
    'sorl.thumbnail',
    'paging',
    'modeltranslation',
    'rosetta',
    'feincms',
    'mptt',

    'picassoft.utils',

    'common',
    'content',
    'catalog',
    'feedback',

    'taghelpers',
    'mediatools',
    'navigation',
    'switchlang',
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
    ('en', _("English")),
)

# Translated text settings
LOCALE_PATHS = os.path.join(SITE_ROOT, 'locale'),

# Model translation settings
MODELTRANSLATION_TRANSLATION_REGISTRY = 'common.translations'

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

#Thumbnail settings
THUMBNAIL_DEBUG = DEBUG

THUMBNAIL_STORAGE = 'django.core.files.storage.FileSystemStorage' # Set explicitly to override default storage

THUMBNAIL_SETTINGS = {
    'FULLSCREEN': ('1200', {'upscale': False}), # (geometry, options)
    'PAGE_IMAGE': ('WIDTHxHEIGHT', {'crop': 'center'}),
    'ICON_SIZE': '1070x250',
    'PREVIEW_IMG': '220',
}

# EMAIL settings
EMAIL_FILE_PATH = os.path.join(SITE_ROOT, 'mailbox')

FEEDBACK_RECIPIENTS = (
    'info@vras.com.ua',
    'info@picassoft.com.ua',
)
FEEDBACK_SENDER = 'info@vras.com.ua'
