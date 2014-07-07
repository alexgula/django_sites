# coding=utf-8
# Django settings for tekhnoland project.
import os
from settings_defaults import *

# calculated paths for django and the site
# used as starting points for various other paths
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
WWW_ROOT = os.path.join(SITE_ROOT, 'wwwroot')

DEBUG = True
TEMPLATE_DEBUG = DEBUG
USE_DEBUG_TOOLBAR = True

ALLOWED_HOST = 'tekhnoland.com'
ALLOWED_HOSTS = [
    'localhost',
    '.{}'.format(ALLOWED_HOST),  # Allow domain and subdomains
    '.{}.'.format(ALLOWED_HOST),  # Also allow FQDN and subdomains
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'tekhnoland',             # Or path to database file if using sqlite3.
        'USER': 'postgres',               # Not used with sqlite3.
        'PASSWORD': 'c',                  # Not used with sqlite3.
        'HOST': 'localhost',                       # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                       # Set to empty string for default. Not used with sqlite3.
    }
}

# Redis settings
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DB = 2
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
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(WWW_ROOT, 'media')

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

# URL prefix for FeinCMS static files.
FEINCMS_ADMIN_MEDIA = '/static/feincms/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
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
SECRET_KEY = ']pwrgjiq3\%^$%Hrtsah%$YnsaAST#$^h45ydgGy'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    #('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
        #'django.template.loaders.eggs.Loader',
    #)),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.debug',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'picassoft.utils.middleware.ForceInactiveUserLogoutMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
)

if USE_DEBUG_TOOLBAR:
    MIDDLEWARE_CLASSES += 'debug_toolbar.middleware.DebugToolbarMiddleware',

ROOT_URLCONF = 'tekhnoland.urls'

TEMPLATE_DIRS = (
    # Put strings here, like '/home/html/django_templates' or 'C:/www/django/templates'.
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
    'django.contrib.admin',
    'django.contrib.markup',
    'django.contrib.staticfiles',
    'django.contrib.webdesign',

    'debug_toolbar',
    'django_extensions',
    'south',
    'paging',
    'media_bundler',
    'django_extensions',

    'tekhnoland.account',
    'tekhnoland.catalog',
    'tekhnoland.exchange1c',
    'tekhnoland.feedback',
    'tekhnoland.navigation',
    'tekhnoland.news',
    'tekhnoland.taghelpers',
    'tekhnoland.polls',
)

# Debug Bar settings
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

# Session settings
SESSION_COOKIE_AGE = 3600
SESSION_SAVE_EVERY_REQUEST = True

# Messages settings
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# Cache settings
CACHE_MIDDLEWARE_KEY_PREFIX = os.path.split(SITE_ROOT)[1]
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

_ = lambda s: s
LANGUAGES = (
    ('ru', _("Russian")),
)

# Profiler settings
USE_PROFILER = False
PROFILER_LOG_BASE = os.path.join(SITE_ROOT, 'profile')

# Test and coverage settings
TEST_RUNNER = 'django_coverage.coverage_runner.CoverageRunner'
COVERAGE_REPORT_HTML_OUTPUT_DIR = os.path.join(SITE_ROOT, 'coverage')
COVERAGE_CODE_EXCLUDES = [
    'def __unicode__\(self\):',
    'def __str__\(self\):',
    'def get_absolute_url\(self\):',
    'from .* import .*', 'import .*',
]
COVERAGE_CUSTOM_REPORTS = False

def list_files_in_path(dirs, ext='.png'):
    return [os.path.join(*(dirs + [f])) for f in os.listdir(os.path.join(STATIC_SOURCE, *dirs)) if f.endswith(ext)]

# Media bundles settings
MEDIA_BUNDLES = (
    {
        'type': 'png-sprite',
        'name': 'sprites',
        'path': STATIC_SOURCE,
        'url': STATIC_URL,
        # Where the generated CSS rules go.
        'css_file': os.path.join(STATIC_SOURCE, 'css', 'sprites.css'),
        'files': list_files_in_path(['sprites']),
    },
)

USE_BUNDLES = False
BUNDLE_VERSION_FILE = None #os.path.join(SITE_ROOT, 'bundle_versions.py')
BUNDLE_VERSIONER = 'mtime'

# EMAIL settings
EMAIL_FILE_PATH = os.path.join(SITE_ROOT, 'mailbox')

FEEDBACK_RECIPIENTS = (
    'info@tekhnoland.com',
    'alexgula@gmail.com',
)
FEEDBACK_SENDER = 'system@tekhnoland.com'

REGISTER_RECIPIENTS = (
    'registration@tekhnoland.com',
    'alexgula@gmail.com',
)
REGISTER_SENDER = 'system@tekhnoland.com'

ORDER_RECIPIENTS = FEEDBACK_RECIPIENTS
ORDER_SENDER = FEEDBACK_SENDER

# Registration settings
REGISTER_EXPIRATION_DAYS = 3

# Login view settings
LOGIN_URL = '/account/login/'
LOGIN_REDIRECT_URL = '/account/'
LOGOUT_URL = '/account/logout/'

AUTH_PROFILE_MODULE = 'account.CustomerProfile'

AUTHENTICATION_BACKENDS = 'tekhnoland.account.auth.CaseInsensitiveModelBackend',

# Exchange 1C settings
EXCHANGE1C_DEBUG_ORDERS = True
EXCHANGE1C_DEBUG_FILES = True
EXCHANGE1C_USER = 'tekhno'
EXCHANGE1C_PASSWORD = '0708'
EXCHANGE1C_UPLOAD_DIR = 'tmp'
EXCHANGE1C_UPLOAD_PATH = os.path.join(SITE_ROOT, EXCHANGE1C_UPLOAD_DIR)
EXCHANGE1C_UPLOAD_RETENTION_DAYS = '10'
EXCHANGE1C_COOKIE_NAME = u"exchangeid"

EXCHANGE1C_REDIS_QUEUE = 'exchange_queue'
EXCHANGE1C_REDIS_CURRENT_KEY = 'exchange_current'

# Order upload settimgs
ORDER_UPLOAD_MAX_SIZE = 1*1024*1024 # 1MB
