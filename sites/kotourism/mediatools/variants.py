# coding=utf-8

import os
from picassoft.utils.filelock import FileLock

def create_variant(orig_path, output_path, creator, lock_timeout=10, **kwargs):
    """Create file at the output path from the file at the original path using creator function.

    If output file is exists and is older than original file, then skip creation.
    To avoid multiple writes output file is locked with timeout.
    """
    if os.path.exists(output_path):
        if os.path.getmtime(orig_path) > os.path.getmtime(output_path):
            os.remove(output_path)
    if not os.path.exists(output_path):
        output_dir = os.path.dirname(output_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        with FileLock(output_path, timeout=lock_timeout):
            creator(orig_path, output_path, **kwargs)

def get_variant(field, resolver, creator, **kwargs):
    """Get image variant url and path.

    Gets original image url and path.
    Builds variant image with kwargs parameters if necessary.
    """
    orig_url, orig_path = field.url, field.file.name
    output_url, output_path = resolver(orig_url, orig_path, **kwargs)
    create_variant(orig_path, output_path, creator, **kwargs)
    return output_url, output_path

def urlpath_builder(base_url, base_path, *args):
    url = u'/'.join([base_url]+list(args))
    output_path = os.path.join(*([base_path]+list(args)))
    return url, output_path
