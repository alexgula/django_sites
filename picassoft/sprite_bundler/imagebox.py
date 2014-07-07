# coding=utf-8
import os
import Image
from .box import Box


class ImageBox(Box):
    """A Box representing an image."""

    def __init__(self, filepath):
        image = Image.open(filepath)
        width, height = image.size
        super(ImageBox, self).__init__(width, height)
        self.image = image

        self.filepath = filepath
        self.filename, self.fileext = os.path.splitext(os.path.basename(filepath))

        # Sprite with hover support has to include 2 images of equal size, stacked one above another:
        # without hover on top and with hover on bottom. File name has to end with ".hover".
        self.hover = self.filename.endswith('.hover')
        if self.hover:
            self.filename = os.path.splitext(self.filename)[0]

    def __repr__(self):
        return '<ImageBox: filepath={} image={}>'.format(self.filepath, self.image)
