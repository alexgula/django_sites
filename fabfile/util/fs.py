# coding=utf-8
import os

from fabric.api import sudo, run, env
from fabric.contrib.files import exists


def chown(name, path):
    sudo('chown -R {name}:{name} {path}'.format(name=name, path=path))


def mkdir(path):
    sudo('mkdir -p {}'.format(path))


def rm(path):
    sudo('rm -f -r -I {}'.format(path))


def link(link_target, link_name):
    sudo('ln -s {target} {name}'.format(target=link_target, name=link_name))


def copy(source_path, target_path):
    sudo('cp -r {source} {target}'.format(source=source_path, target=target_path))


def scp(subdomain, path):
    _scp(env.user_scp, subdomain + '.picassoft.com.ua', path)


def ensure_local_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def prepare_local_dir(dir_path, ext):
    """Prepare directory for filling.

    If directory is not present, create it. If it exists, clear it by removing all files with the given extension."""
    ensure_local_dir(dir_path)
    for root, dirs, files in os.walk(dir_path):
        for file_name in files:
            if file_name.endswith(ext):
                os.remove(os.path.join(root, file_name))


def list_local_files(dir_path, ext):
    if os.path.exists(dir_path):
        for root, dirs, files in os.walk(dir_path):
            for file_name in files:
                file_name, file_ext = os.path.splitext(file_name)
                if file_ext == ext:
                    yield file_name


def first_existing(*args):
    for context, file_name in args:
        if exists(file_name):
            yield context, file_name
            break


def _scp(user, address, path):
    run('scp {user}@{address}:{path} {path}'.format(user=user, address=address, path=path))
