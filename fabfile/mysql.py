# coding=utf-8
from functools import wraps
from fabric.api import task
from .util import mysql, series


def repeat_name_if_missing(f):
    @wraps(f)
    def wrapper(*args):
        if len(args) == 2:
            return f(args[0], args[0], args[1])
        else:
            return f(*args)
    return wrapper


@task
@repeat_name_if_missing
def create(dbname, username, password):
    """Create database and user for it."""
    mysql.create(dbname, username, password)


@task
def create_all():
    series.apply_to_all(db_func=mysql.create)


@task
@repeat_name_if_missing
def backup(dbname, username, password):
    """Create database and restore it from backup."""
    mysql.backup(dbname, username, password)


@task
def backup_all():
    series.apply_to_all(db_func=mysql.backup)


@task
@repeat_name_if_missing
def restore(dbname, username, password):
    """Create database and restore it from backup."""
    mysql.restore(dbname, username, password)


@task
def restore_all():
    series.apply_to_all(db_func=mysql.restore)


@task
def drop(dbname):
    """Drop database, retaining user."""
    mysql.drop(dbname, dbname)


@task
def drop_all():
    for username, password, dbnames in series.list_all():
        for dbname in dbnames:
            mysql.drop(dbname, username)
