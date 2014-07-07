import os
import shutil


def auto_rename(file_path, new_name):
    """
    Renames a file, keeping the extension.

    Parameters:
        - file_path: the file path
        - new_name: the new basename of the file (no extension)

    Returns the new file path on success or the original file_path on error.
    """

    if file_path == '':
        return ''

    # Get the new name
    new_path = change_basename(file_path, new_name)

    if new_path != file_path:
        try:
            shutil.move(file_path, new_path)
        except IOError:
            # Error? Restore original name
            new_path = file_path

    return new_path


def change_basename(file_path, new_name):
    # Extract path: 'news/img'
    path = os.path.dirname(file_path)
    # Extract current name: 'name.jpg'
    curr_name = os.path.basename(file_path)
    # Split file name and extension: 'name', '.jpg'
    original, ext = os.path.splitext(curr_name)
    # Return the new path: 'news/img/new_name.jpg'
    return os.path.join(path, new_name + ext).replace('\\', '/')


def add_to_basename(file_path, str):
    # Extract path: 'news/img'
    path = os.path.dirname(file_path)
    # Extract current name: 'name.jpg'
    curr_name = os.path.basename(file_path)
    # Split file name and extension: 'name', '.jpg'
    original, ext = os.path.splitext(curr_name)
    # Return the new path: 'news/img/originalstr.jpg'
    return os.path.join(path, original + str + ext).replace('\\', '/')
