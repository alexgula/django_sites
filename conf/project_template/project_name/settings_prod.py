# coding: utf-8
from .settings import *

DEBUG = False
USE_DEBUG_TOOLBAR = DEBUG
TEMPLATE_DEBUG = DEBUG
THUMBNAIL_DEBUG = DEBUG

DATABASES['default']['PASSWORD'] = 'demoroga1122'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
        #'django.template.loaders.eggs.Loader',
    )),
)

# Sessions settings
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

# Redis settings
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DB = 10
REDIS_PASSWORD = ''

# Cache settings
CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': '{}:{}'.format(REDIS_HOST, REDIS_PORT),
        'OPTIONS': {
            'DB': REDIS_DB,
            #'PASSWORD': REDIS_PASSWORD,
        },
    },
}

# Thumbnail settings
THUMBNAIL_CONVERT = 'convert'
THUMBNAIL_IDENTIFY = 'identify'

THUMBNAIL_KVSTORE = 'sorl.thumbnail.kvstores.redis_kvstore.KVStore'
THUMBNAIL_REDIS_HOST = REDIS_HOST
THUMBNAIL_REDIS_PORT = REDIS_PORT
THUMBNAIL_REDIS_DB = REDIS_DB
THUMBNAIL_REDIS_PASSWORD = REDIS_PASSWORD
