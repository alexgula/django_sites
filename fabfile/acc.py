# coding=utf-8
from fabric.api import task, env, sudo, settings

from .util import path, fs, mysql, files, series


@task
def user(name):
    """Create user and all appropriate directories remotedly."""
    sudo('useradd --create-home --user-group {name}'.format(name=name))
    fs.mkdir(path.account(name))
    fs.link(path.account(name), path.home(name, 'sites'))
    fs.mkdir(path.home(name, '.ssh'))
    fs.copy(path.home(env.user, '.ssh', 'authorized_keys'), path.home(name, '.ssh', 'authorized_keys'))
    files.own(name)


@task
def own(name):
    files.own(name)


@task
def create(name, password):
    user(name)
    mysql.create(name, name, password)


@task
def create_all():
    series.apply_to_all(user, mysql.create)


@task
def drop(name):
    with settings(warn_only=True):
        sudo('userdel -r {name}'.format(name=name))
        #fs.rm(path.account(name))
        mysql.drop(name, name)

@task
def backup_files(name):
    files.pack(name)


@task
def backup_mysql(database, name, password):
    mysql.backup(database, name, password)


@task
def backup(name, password):
    backup_files(name)
    backup_mysql(name, name, password)


@task
def restore_files(name):
    """Create user and restore files from backup."""
    files.unpack(name)
    files.own(name)


@task
def restore_mysql(database, name, password):
    """Create database and restore it from backup."""
    mysql.create(database, name, password)
    mysql.restore(database, name, password)


@task
def restore(name, password):
    """Create user and database and restore from backup."""
    restore_files(name)
    restore_mysql(name, name, password)


@task
def move_local_files(name):
    files.put(path.tar(name))
    restore_files(name)


@task
def move_local_mysql(database, name, password):
    files.put(path.sql(name))
    restore_mysql(database, name, password)


@task
def move_local(name, password):
    move_local_files(name)
    move_local_mysql(name, name, password)


@task
def move_remote_files(server_from, name):
    files.scp(server_from, name)
    restore_files(name)


@task
def move_remote_mysql(server_from, name, password):
    mysql.scp(server_from, name, name)
    mysql.restore(name, name, password)


@task
def move_remote_mysql_all(server_from):
    for username, password, dbnames in series.list_all():
        for dbname in dbnames:
            mysql.scp(server_from, dbname, username)
            mysql.drop(dbname, username)
            mysql.create(dbname, username, password)
            mysql.restore(dbname, username, password)


@task
def move_remote(server_from, name, password):
    move_remote_files(server_from, name)
    move_remote_mysql(server_from, name, name, password)
