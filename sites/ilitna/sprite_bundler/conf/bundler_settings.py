# coding=utf-8
"""
media_bundler specific settings with the defaults filled in.

If the user has overridden a setting in their settings module, we'll use that
value, but otherwise we'll fall back on the value from
media_bundler.default_settings.  All bundler- specific settings checks should
go through this module, but to check global Django settings, use the normal
django.conf.settings module.
"""
from django.conf import settings
from . import default_settings

SPRITE_SPACING = getattr(settings, 'SPRITE_SPACING', default_settings.SPRITE_SPACING)
SPRITE_BUNDLES = getattr(settings, 'SPRITE_BUNDLES', default_settings.SPRITE_BUNDLES)
SPRITE_COMPRESSOR_PATH = getattr(settings, 'SPRITE_COMPRESSOR_PATH', default_settings.SPRITE_COMPRESSOR_PATH)
