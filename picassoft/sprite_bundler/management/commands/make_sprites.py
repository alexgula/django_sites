# coding=utf-8
from django.core.management.base import NoArgsCommand
from django.conf import settings

from ... import builder
from ... import image_show


class Command(NoArgsCommand):
    """Bundles your sprites as specified in settings.py."""

    def handle_noargs(self, **options):
        for bundle in settings.SPRITE_BUNDLES:
            filename = builder.make(**bundle)
            self.stdout.write("Success: sprite file {}".format(filename))
            image_show.show(filename)
