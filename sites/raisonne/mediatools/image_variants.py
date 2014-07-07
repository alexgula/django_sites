import os
from picassoft.utils.filelock import FileLock

# Generic functions

def urlpath_builder(base_url, base_path, *args):
    url = u'/'.join([base_url]+list(args))
    output_path = os.path.join(*([base_path]+list(args)))
    return (url, output_path)

def create_path(orig_path, output_path, creator, lock_timeout=10, **kwargs):
    overwrite = kwargs.get('overwrite', False)
    if os.path.exists(output_path) and overwrite:
        os.remove(output_path)
    if not os.path.exists(output_path):
        output_dir = os.path.dirname(output_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        with FileLock(output_path, timeout=lock_timeout):
            creator(orig_path, output_path, **kwargs)

def load_variant(orig_url, orig_path, resolver, creator, **kwargs):
    """Get image variant url and path.

    Gets original image url and path.
    Builds variant image with kwargs parameters if necessary.
    """
    output_url, output_path = resolver(orig_url, orig_path, **kwargs)
    create_path(orig_path, output_path, creator, **kwargs)
    return output_url, output_path

def load_field_variant(field, resolver, creator, **kwargs):
    if field.name:
        output_url, output_path = load_variant(field.url, field.path, resolver, creator, **kwargs)
        return output_url
    else:
        return ''

# DeepZoom functions

def default_dzi_resolver(url, path, **kwargs):
    base_url = os.path.dirname(os.path.dirname(url))
    base_path = os.path.dirname(os.path.dirname(path))
    dzi_dir_name = u'dzi'
    dir_name = os.path.splitext(os.path.basename(path))[0]
    file_name = 'dzc_output.xml'

    return urlpath_builder(base_url, base_path, dzi_dir_name, dir_name, file_name)

def create_dzi(path, output_path, **kwargs):
    from .deepzoom import ImageCreator
    creator = ImageCreator(tile_size=256, tile_overlap=1, tile_format="jpg", image_quality=0.8, resize_filter="bicubic")
    creator.create(path, output_path)

# Thumbnail functions

def default_thumbnail_resolver(url, path, **kwargs):
    size = kwargs['size']
    base_url = os.path.dirname(os.path.dirname(url))
    base_path = os.path.dirname(os.path.dirname(path))
    dir_name = u'thumbnail_{0}'.format(size)
    file_name = os.path.basename(path)

    return urlpath_builder(base_url, base_path, dir_name, file_name)

def create_thumbnail(path, output_path, **kwargs):
    import Image
    size = kwargs['size']
    fill = kwargs.get('fill', False)
    offset_h = kwargs.get('offset_h', 0)
    offset_v = kwargs.get('offset_v', 0)

    try:
        im = Image.open(path).convert("RGB")
        if fill:
            x1, y1, x2, y2 = im.getbbox()
            width, height = x2 - x1, y2 - y1

            if width > height:
                cx1 = x1 + (width - height) / 2
                cx2 = x1 + (width + height) / 2
                if offset_h > 0:
                    offset = (width - cx2) * offset_h / 100
                elif offset_h < 0:
                    offset = cx1 * offset_h / 100
                else:
                    offset = 0
                cx1 += offset
                cx2 += offset
                cy1 = y1
                cy2 = y2
            else:
                cx1 = x1
                cx2 = x2
                cy1 = y1 + (height - width) / 2
                cy2 = y1 + (height + width) / 2
                if offset_v > 0:
                    offset = (height - cy2) * offset_v / 100
                elif offset_v < 0:
                    offset = cy1 * offset_v / 100
                else:
                    offset = 0
                cy1 += offset
                cy2 += offset
            im = im.crop((cx1, cy1, cx2, cy2))
        im.thumbnail((size,size), Image.ANTIALIAS)
        im.save(output_path)
    except IOError:
        pass # TODO: Log error!

# Sugar functions

def load_field_dzi(field, resolver=default_dzi_resolver, **kwargs):
    return load_field_variant(field, resolver, create_dzi, **kwargs)

def load_field_thumbnail(field, resolver=default_thumbnail_resolver, **kwargs):
    return load_field_variant(field, resolver, create_thumbnail, **kwargs)
