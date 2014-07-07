# coding=utf-8
import os
from fabric.api import env, require


def account(name, *args):
    require('remote_web_dir')
    return remote_path_join(env.remote_web_dir, 'sites', name, *args)


def django_site(*args):
    require('remote_web_dir')
    return account('django', 'sites', *args)


def home(name, *args):
    if name == 'root':
        return remote_path_join('/root', *args)
    return remote_path_join('/home', name, *args)


def backup_local(*args):
    return os.path.join(r'W:\.backups', *args)


def backup(*args):
    require('remote_web_dir')
    return remote_path_join(env.remote_web_dir, 'backups', *args)


def env_config():
    require('root_path')
    return os.path.join(env.root_path, 'config.yaml')


def account_config(name):
    require('local_config_dir')
    return os.path.join(env.local_config_dir, name + '.yaml')


def etc_local(*args):
    require('local_etc_dir')
    return os.path.join(env.local_etc_dir, *args)


def etc(*args):
    return remote_path_join('/etc', *args)


def remote_path_join(*args):
    """Join path elements for remote host. Assuming it is Unix-like."""
    return '/'.join([arg for arg in args if arg])


def tar(name):
    return name + '.tar.gz'


def sql(name):
    return name + '.sql.gz'