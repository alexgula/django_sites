# coding=utf-8
# Django settings for all projects.

ADMINS = [
    ('Oleksandr Gula', 'sysreports@picassoft.com.ua'),
]

MANAGERS = ADMINS

INTERNAL_IPS = ('127.0.0.1', '95.158.36.13', '213.108.72.234', )

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s',
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s %(module)s %(message)s',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        # Old Django does not contain this
        #'require_debug_true': {
        #    '()': 'django.utils.log.RequireDebugTrue',
        #},
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            #'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
        },
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'py.warnings': {
            'handlers': ['console'],
        },
    },
}

THUMBNAIL_ENGINE = 'sorl.thumbnail.engines.convert_engine.Engine'
THUMBNAIL_CONVERT = 'D:\Programs\ImageMagick\convert'
THUMBNAIL_IDENTIFY = 'D:\Programs\ImageMagick\identify'

ROSETTA_WSGI_AUTO_RELOAD = True

SOUTH_TESTS_MIGRATE = False

#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
