# coding=utf-8
import os, glob, shutil, subprocess, re
from .box import Box, arrange
from .conf.bundler_settings import SPRITE_COMPRESSOR_PATH

CSS_REGEXP = re.compile(r'[^a-zA-Z\-_]')
CSS_BLOCK_TMPLATE = '''
.{0} {{
{1}
}}
'''

def format_size(size, unit='px'):
    if size == 0:
        return '0'
    else:
        return '{}{}'.format(size, unit)

def clear_css_name(name):
    name = name.replace(' ', '-').replace('.', '-')
    return CSS_REGEXP.sub('', name)

def make_css(name, props):
    # We try to format it nicely here in case the user actually looks at it.
    # If he wants it small, he'll bundle it up in his CssBundle.
    propstr = '\n'.join('     {}: {};'.format(name, value) for name, value in props)
    return CSS_BLOCK_TMPLATE.format(name, propstr)


class SpriteBundler(object):

    """Bundle for PNG sprites.

    In addition to generating a PNG sprite, it also generates CSS rules so that
    the user can easily place their sprites.  We build sprite bundles before CSS
    bundles so that the user can bundle the generated CSS with the rest of their
    CSS.
    """

    def __init__(self, format, source, url, sprite_file, css_file):
        self.format = format
        self.source = source
        self.url = url
        self.sprite_file = sprite_file
        self.css_file = css_file

    def make(self):
        import Image # If this fails, you need the Python Imaging Library.
        boxes = [ImageBox(Image.open(path), path) for path in glob.iglob(self.source)]
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
        sprite.save(self.sprite_file, 'PNG')
        self.optimize_output()
        self.generate_css(areas)

    def optimize_output(self):
        """Optimize the PNG with pngcrush."""
        sprite_path = self.sprite_file
        tmp_path = sprite_path + '.tmp'
        args = [SPRITE_COMPRESSOR_PATH, '-rem', 'alla', sprite_path, tmp_path]
        proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        proc.wait()
        if proc.returncode != 0:
            raise Exception('pngcrush returned error code: {}\nOutput was:\n\n{}'.format(
                proc.returncode, proc.stdout.read()))
        shutil.move(tmp_path, sprite_path)

    def generate_css(self, areas):
        """Generate the background offset CSS rules."""
        with open(self.css_file, 'w') as css:
            css.write("/* Generated classes for django-sprite-bundler. Don't edit! */\n")
            for area in areas:
                for box in area.boxes():
                    props = [
                        ('display', 'block'),
                        ('width', format_size(box.width)),
                        ('height', format_size(box.height)),
                        ('background', 'url("{}") {} {}'.format(
                            self.url, format_size(-box.x), format_size(-box.y))),
                    ]
                    filename, fileext = os.path.splitext(os.path.basename(box.filename))
                    filename = clear_css_name(filename)
                    fileext = clear_css_name(fileext[1:])
                    cssname = self.format.format(name=filename, ext=fileext)
                    css.write(make_css(cssname, props))


class ImageBox(Box):

    """A Box representing an image.

    We hand these off to the bin packing algorithm.  After the boxes have been
    arranged, we can place the associated image in the sprite.
    """

    def __init__(self, image, filename):
        width, height = image.size
        super(ImageBox, self).__init__(width, height)
        self.image = image
        self.filename = filename

    def __repr__(self):
        return '<ImageBox: filename={} image={}>'.format(self.filename, self.image)
