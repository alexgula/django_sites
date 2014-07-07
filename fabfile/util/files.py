# coding=utf-8
from fabric.api import env, sudo, cd, put, get
from . import path, fs


def pack(name):
    with cd(path.account(name)):
        sudo('tar cfz {}.tar.gz .'.format(path.backup('sites', name)))


def unpack(name):
    with cd(path.account(name)):
        base_name = path.backup('sites', name)
        for options, file_name in fs.first_existing(
            ('xfz', '{}.tgz'.format(base_name)),
            ('xfz', '{}.tar.gz'.format(base_name)),
            ('xfz', '{}.gz'.format(base_name)),
            ('xf', '{}.tar'.format(base_name)),
        ):
            sudo('tar {} {}'.format(options, file_name))


def own(name):
    """Restore account and home directory owner."""
    fs.chown(name, path.account(name))
    fs.chown(name, path.home(name))


def put(*args):
    put(path.backup_local(*args), path.backup('sites', *args))


def get(*args):
    get(path.backup('sites', *args), path.backup_local(*args))


def scp(server_from, name):
    fs.scp(server_from, path.tar(path.backup('sites', name)))
