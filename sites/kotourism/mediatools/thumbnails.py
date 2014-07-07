# coding=utf-8

try:
    from PIL import Image, ImageOps, ImageEnhance
except ImportError:
    import Image, ImageOps, ImageEnhance

import os

from .variants import get_variant, urlpath_builder

def resolve_thumbnail(url, path, **kwargs):
    """Default thumbnail file name and url resolver.

    Gets parent directory of the directory of the file and creates new directory.
    """
    thumb_dir = kwargs.get('name', u'thumbnail')
    (width, height) = kwargs['size']
    base_url = os.path.dirname(os.path.dirname(url))
    base_path = os.path.dirname(os.path.dirname(path))
    if width == height:
        dir_name = u'{}_{}'.format(thumb_dir, width)
    else:
        dir_name = u'{}_{}x{}'.format(thumb_dir, width, height)
    file_name = os.path.basename(path)

    return urlpath_builder(base_url, base_path, u'thumbnail', dir_name, file_name)

def create_thumbnail(source_path, output_path, **kwargs):
    """Default thumbnail creator.

    Creates thumbnail file at output path from the image at source path.
    Additional arguments:
    - size: tuple (width, height) of the resulting image;
    - fill: boolean, if True, fit image in size, possibly cropping at bigger sides,
      else resize image to size, possibly with blank areas at smaller sides;
    - offset: tuple, with the following elements:
        - absolute: boolean, if True, offset is set in pixels, else it's set in percent;
        - horisontal offset: [0;width] if absolute, [0.0;1.0] otherwise;
        - vertical offset: [0;height] if absolute, [0.0;1.0] otherwise;
    - contrast: float, histogram pixel count cut percentage, 0 is none, 1 is every single pixel,
      if None autocontrast is not used;
    - sharpen: float, sharpnes amount, 1 is none, 2 is moderate sharpen, 0.5 is blur.
    """
    import Image

    im = Image.open(source_path).convert("RGB")

    image_width, image_height = im.size
    thumb_size = kwargs['size']
    fill = kwargs.get('fill', True)
    offset_absolute, offset_h, offset_v = kwargs.get('offset', (False, None, None)) # offsets can be None
    if offset_h is None:
        offset_h = 0.5
    if offset_v is None:
        offset_v = 0.5
    if offset_absolute:
        offset_h = 1.0 * offset_h / image_width
        offset_v = 1.0 * offset_v / image_height

    crop_width, crop_height = kwargs.get('crop_size', (None, None))
    if crop_width is None:
        crop_width = image_width
    if crop_height is None:
        crop_height = image_height
    crop_size = (crop_width, crop_height)

    contrast = kwargs.get('contrast', None)
    sharpen = kwargs.get('sharpen', 1.6)

    im.thumbnail(crop_size, Image.ANTIALIAS)
    if fill:
        im = ImageOps.fit(im, thumb_size, Image.ANTIALIAS, centering=(offset_h, offset_v))
    else:
        im.thumbnail(thumb_size, Image.ANTIALIAS)

    if contrast is not None:
        im = ImageOps.autocontrast(im, contrast)
    if sharpen is not None:
        sharpener = ImageEnhance.Sharpness(im)
        im = sharpener.enhance(sharpen)

    im.save(output_path)

def get_thumbnail(field, resolver=resolve_thumbnail, creator=create_thumbnail, **kwargs):
    output_url, output_path = get_variant(field, resolver, creator, **kwargs)
    return dict(url=output_url)
