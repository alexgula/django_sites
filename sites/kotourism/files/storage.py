# coding=utf-8
import errno

import hashlib
import os
from django.conf import settings
from django.core.files.move import file_move_safe
from django.core.files import locks
from django.core.files.storage import FileSystemStorage


class HashedFileSystemStorage(FileSystemStorage):
    def __init__(self,  hash_dirs=None, *args, **kwargs):
        super(HashedFileSystemStorage, self).__init__(*args, **kwargs)

        if not hash_dirs:
            hash_dirs = getattr(settings, 'HASHED_STORAGE_DIRS', [2, 2])
        self.hash_dirs = hash_dirs

    def _split_name(self, name):
        parts = []
        start = 0
        for part_len in self.hash_dirs:
            parts.append(name[start:start + part_len])
            start += part_len
        if start < len(name):
            parts.append(name)
        return os.path.join(*parts)

    def _save(self, name, content):
        # Prepare file name from the file content hash
        dir_name, file_full_name = os.path.split(name)
        file_name, file_ext = os.path.splitext(file_full_name)
        content_hash = hashlib.sha1()
        for chunk in content.chunks():
            content_hash.update(chunk)
        hash_name = self._split_name(content_hash.hexdigest())
            # + str(content.size) Can add size if anytime stuck into collisions.
        name = os.path.join(dir_name, hash_name + file_ext.lower())

        full_path = self.path(name)

        # Create any intermediate directories that do not exist.
        # Note that there is a race between os.path.exists and os.makedirs:
        # if os.makedirs fails with EEXIST, the directory was created
        # concurrently, and we can continue normally. Refs #16082.
        directory = os.path.dirname(full_path)
        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
            except OSError, e:
                if e.errno != errno.EEXIST:
                    raise
        if not os.path.isdir(directory):
            raise IOError("%s exists and is not a directory." % directory)

        # There's a potential race condition: it's possible that two threads
        # might return the same name. In this case we just continue normally.
        # NOTE! This differs considerably from the default file storage behaviour.
        try:
            # This file has a file path that we can move.
            if hasattr(content, 'temporary_file_path'):
                file_move_safe(content.temporary_file_path(), full_path)
                content.close()

            # This is a normal uploadedfile that we can stream.
            else:
                # This fun binary flag incantation makes os.open throw an
                # OSError if the file already exists before we open it.
                fd = os.open(full_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, 'O_BINARY', 0))
                try:
                    locks.lock(fd, locks.LOCK_EX)
                    for chunk in content.chunks():
                        os.write(fd, chunk)
                finally:
                    locks.unlock(fd)
                    os.close(fd)
        except OSError, e:
            if e.errno != errno.EEXIST:
                raise

        if settings.FILE_UPLOAD_PERMISSIONS is not None:
            os.chmod(full_path, settings.FILE_UPLOAD_PERMISSIONS)

        return name

    def get_available_name(self, name):
        return name
