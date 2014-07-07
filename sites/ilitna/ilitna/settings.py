# coding=utf-8
# Django settings for ilitna project.
import os
from settings_defaults import * # DO NOT delete, there are default settings!

SITE_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
WWW_ROOT = os.path.join(SITE_ROOT, 'wwwroot')

DEBUG = True
TEMPLATE_DEBUG = DEBUG
USE_DEBUG_TOOLBAR = True

ALLOWED_HOST = 'ilitna.info'
ALLOWED_HOSTS = [
    'localhost',
    '.{}'.format(ALLOWED_HOST),  # Allow domain and subdomains
    '.{}.'.format(ALLOWED_HOST),  # Also allow FQDN and subdomains
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'ilitna',                      # Or path to database file if using sqlite3.
        'USER': 'postgres',                      # Not used with sqlite3.
        'PASSWORD': 'c',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Redis settings
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DB = 6
REDIS_PASSWORD = ''

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
LANGUAGE_CODE = 'ru'

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
    'compressor.finders.CompressorFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'i0*^fcaymxj*#s0di05epj5u5(5wgbnnf^e(c&amp;c=td_uu^$h42'

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

ROOT_URLCONF = 'ilitna.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'ilitna.wsgi.application'

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
    'django.contrib.markup',
    'django.contrib.webdesign',

    'debug_toolbar',
    'django_extensions',
    'south',
    'mptt',
    'paging',
    'sorl.thumbnail',
    'compressor',
    'modeltranslation',
    'rosetta',
    'feincms',

    'news',
    'library',
    'page',
    'sprite_bundler',
    'switchlang',
    'navigation',
    'taghelpers',
    #'haystack',
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
    ('ru', _("Russian")),
    #('uk', _("Ukrainian")),
)

# Translated text settings
LOCALE_PATHS = os.path.join(SITE_ROOT, 'locale'),

# Model translation settings
MODELTRANSLATION_TRANSLATION_REGISTRY = 'ilitna.translations'

#Thumbnail settings
THUMBNAIL_DEBUG = DEBUG
THUMBNAIL_STORAGE = 'django.core.files.storage.FileSystemStorage' # Set explicitly to override default storage
THUMBNAIL_SETTINGS = {
    'FULLSCREEN': ('1200', {'upscale': False}), # (geometry, options)
    'PAGE_IMAGE': ('250', {'upscale': False}),
}

#Sprite settings
SPRITE_BUNDLES = [
    {
        'format': '{name}',
        'source': os.path.join(STATIC_SOURCE, 'sprites', '*.*'),
        'url': STATIC_URL + 'img/sprites.png',
        'sprite_file': os.path.join(STATIC_SOURCE, 'img', 'sprites.png'),
        'css_file': os.path.join(STATIC_SOURCE, 'css', 'sprites.css'),
    },
]
SPRITE_COMPRESSOR_PATH = os.path.join(SITE_ROOT, 'bin', 'pngcrush')

#Search settings
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.xapian_backend.XapianEngine',
        'PATH': os.path.join(SITE_ROOT, 'index', 'xapian'),
        'INCLUDE_SPELLING': True,
    },
}

# Compressor settings
COMPRESS_OFFLINE = False
COMPRESS_OUTPUT_DIR = 'cache'
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter',
]
COMPRESS_PRECOMPILERS = [
    ('text/less', os.path.join(SITE_ROOT, 'bin', 'lessc.cmd') + ' {infile}'), # Since {outfile} is omitted, use stdout
]

#Email settings
EMAIL_FILE_PATH = os.path.join(SITE_ROOT, 'mailbox')
