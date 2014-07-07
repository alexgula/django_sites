# coding: utf-8
# Django settings for hermanmiller project.
import os
from settings_defaults import * # DO NOT delete, there are default settings!

SITE_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
WWW_ROOT = os.path.join(SITE_ROOT, 'wwwroot')

DEBUG = True
TEMPLATE_DEBUG = DEBUG
USE_DEBUG_TOOLBAR = True

ALLOWED_HOST = 'herman-miller.com.ua'
ALLOWED_SUBDOMAIN = 'hermanmiller.picassoft.com.ua'
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
        'NAME': 'hermanmiller',                      # Or path to database file if using sqlite3.
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
SECRET_KEY = 'u12k&hqz8+agf%q3ob5fg6e2-4t#4s+do9$d_#!63=6r9$ou3)'

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
    'mediatools.context_processors.settings',
    'constance.context_processors.config',
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

ROOT_URLCONF = 'hermanmiller.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'hermanmiller.wsgi.application'

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
    #'django_extensions',
    'south',
    'sorl.thumbnail',
    'paging',
    #'modeltranslation',
    'feincms',
    'mptt',
    'haystack',
    'constance',
    'constance.backends.database',

    'picassoft.utils',
    'picassoft.sprite_bundler',

    'search',
    'navigation',
    'catalog',
    'content',
    'shop',
    'slideshow',
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
)

LOCALE_PATHS = os.path.join(SITE_ROOT, 'locale'),

# Model translation settings
TRANSLATION_REGISTRY = 'hermanmiller.translations'

# Sprite bundles settings
SPRITE_BUNDLES = [
    {
        'format': "sprite-{name}",
        'source': os.path.join(SITE_ROOT, 'sprites', '*.*'),
        'url': "../img/sprites.png",
        'sprite_file': os.path.join(STATIC_SOURCE, 'img', 'sprites.png'),
        'css_file': os.path.join(STATIC_SOURCE, 'css', 'sprites.css'),
    }
]

#Thumbnail settings
THUMBNAIL_DEBUG = DEBUG

THUMBNAIL_STORAGE = 'django.core.files.storage.FileSystemStorage' # Set explicitly to override default storage

THUMBNAIL_SETTINGS = {
    'FULLSCREEN_SIZE': '870',
    'ICON_SIZE': '250x250',
    'ONE_COLUMN_ICON_SIZE': '270',
    'CONTENT_PICTURE': '250x187',
    'CONTENT_PICTURE_NEWS': '270x202',
}

THUMBNAIL_PADDING = True

#Search settings
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.xapian_backend.XapianEngine',
        'PATH': os.path.join(SITE_ROOT, 'index', 'xapian'),
        'INCLUDE_SPELLING': True,
    },
}

#Constance setings
CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
CONSTANCE_DATABASE_CACHE_BACKEND = 'default'

CONSTANCE_CONFIG = {
    'CURRENCY_RATE_EUR': (12.5, _("Currency rate UAH to EUR (per 1 EUR).")),
    'INVOICE_SUPPLIER': ("", _("Invoice supplier. New lines are taken into account.")),
    'LIQPAY_PUBLIC_KEY': ('i1887235161', _("LiqPay public key.")),
    'LIQPAY_PRIVATE_KEY': ('1LjptrUnv71ecOv1W62MOWK8QgVYd82ObadL48Iw', _("LiqPay private key.")),
}

#Session settings
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

#Email settings
EMAIL_FILE_PATH = os.path.join(SITE_ROOT, 'mailbox')

ORDER_RECIPIENTS = (
    'sales@picassoft.com.ua',
    'a.butsan@picassoft.com.ua',
)

ORDER_SENDER = 'sales@hermanmiller.com.ua'

#Auth settings
LOGIN_URL = 'registration:login'
LOGIN_REDIRECT_URL = 'home'
