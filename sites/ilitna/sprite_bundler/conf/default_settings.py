# coding=utf-8
"""
These are the default settings for media_bunder.

You can copy, paste, and modify these values into your own settings.py file.
"""
import os
from django.conf import settings


SPRITE_SPACING = 2

SPRITE_BUNDLES = [
    {
        'format': 'sprite-{name}-{ext}',
        'source': os.path.join(settings.STATIC_SOURCE, 'sprites', '*.*'),
        'url': settings.STATIC_URL + 'img/sprites.png',
        'sprite_file': os.path.join(settings.STATIC_SOURCE, 'img', 'sprites.png'),
        'css_file': os.path.join(settings.STATIC_SOURCE, 'css', 'sprites.css'),
    },
]

SPRITE_COMPRESSOR_PATH = 'pngcrush'
