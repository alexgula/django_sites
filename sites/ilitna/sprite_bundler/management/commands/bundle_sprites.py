# coding=utf-8
"""
A Django management command to bundle our media.

This command should be integrated into any build or deploy process used with
the project.
"""
from django.core.management.base import NoArgsCommand

from ...conf import bundler_settings
from ... import bundler


class Command(NoArgsCommand):
    """Bundles your media as specified in settings.py."""

    def handle_noargs(self, **options):
        for bundle in bundler_settings.SPRITE_BUNDLES:
            bundler.SpriteBundler(**bundle).make()
