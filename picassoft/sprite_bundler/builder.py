# coding=utf-8
import glob
import shutil
import subprocess

import Image

from .css import generate_css
from .box import arrange
from .imagebox import ImageBox
from .settings import SPRITE_COMPRESSOR_PATH


def _optimize_image(file_path):
    """Optimize the PNG with pngcrush."""
    tmp_path = file_path + '.tmp'

    if SPRITE_COMPRESSOR_PATH is None:
        return

    args = [SPRITE_COMPRESSOR_PATH, '-rem', 'alla', file_path, tmp_path]
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    proc.wait()
    if proc.returncode != 0:
        raise Exception('pngcrush returned error code: {}\nOutput was:\n\n{}'.format(
            proc.returncode, proc.stdout.read()))
    shutil.move(tmp_path, file_path)


def _write_css(css_file, *args, **kwargs):
    """Generate the background offset CSS rules."""
    with open(css_file, 'w') as css:
        css.write("/* Generated classes! Don't edit! */\n")
        css.writelines(generate_css(*args, **kwargs))


def make(format, source, url, sprite_file, css_file):
    """Make PNG sprites.

    In addition to generating a PNG sprite, generates CSS rules so that
    the user can easily place their sprites.
    """
    boxes = [ImageBox(path) for path in glob.iglob(source)]
    areas, height = arrange(boxes)
    if not areas:
        return
    width = areas[0].width
    sprite = Image.new('RGBA', (width, height))
    for area in areas:
        for box in area.boxes():
            # Convert to RGBA to properly build bands. If not convert, even if image's mode is RGBA,
            # mask is applied incorrectly (applies not only to alpha channel but also to color channels).
            sprite.paste(box.image.convert('RGBA'), (box.x, box.y))
    sprite.save(sprite_file, 'PNG')
    _optimize_image(sprite_file)
    _write_css(css_file, url, format, areas)
    return sprite_file
