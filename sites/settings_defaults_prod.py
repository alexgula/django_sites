# coding=utf-8
# Django production settings for all projects.

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#SEND_BROKEN_LINK_EMAILS = True

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
        #'django.template.loaders.eggs.Loader',
    )),
)

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

THUMBNAIL_CONVERT = 'convert'
THUMBNAIL_IDENTIFY = 'identify'
