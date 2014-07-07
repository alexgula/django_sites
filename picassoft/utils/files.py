# coding=utf-8
import os, zipfile, errno, datetime

def walk_files(path, ext=None):
    """Find recursively all files with given extension in the path."""
    for root, dirs, files in os.walk(path):
        for file_name in files:
            if not ext or file_name.endswith(ext):
                yield root, file_name

def extract_zip(extract_dir, file_path):
    """Extract file to directory."""
    with zipfile.ZipFile(file_path) as zf:
        zf.extractall(extract_dir)

def safe_make_dirs(dir, mode=0777):
    try:
        os.makedirs(dir, mode)
    except OSError, e:
        if e.errno != errno.EEXIST:
            raise

def list_dirs(path):
    for name in os.listdir(path):
        dir_path = os.path.join(path, name)
        if os.path.isdir(dir_path):
            yield dir_path

def old_dirs(path, age, ref_date=None):
    if ref_date is None:
        ref_date = datetime.datetime.now()

    for dir_path in list_dirs(path):
        yield dir_path, (ref_date - datetime.datetime.fromtimestamp(os.path.getctime(dir_path))) > age
