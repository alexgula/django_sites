# coding=utf-8
from fabric.api import env, require, run, cd
from . import path, fs


def create(dbname, username, password):
    """Create database and user for it."""
    dbname = _prepare_dbname(dbname, username)
    _run_ddl(
        "CREATE DATABASE IF NOT EXISTS {db} DEFAULT CHARACTER SET utf8;"
        "GRANT ALL ON {db}.* TO {user}@localhost IDENTIFIED BY '{pwd}';",
        db=dbname, user=username, pwd=password)


def drop(dbname, username):
    dbname = _prepare_dbname(dbname, username)
    """Create database and user for it."""
    _run_ddl(
        "DROP DATABASE IF EXISTS {db};",
        db=dbname)


def backup(dbname, username, password):
    """Create MySQL database backup."""
    dbname = _prepare_dbname(dbname, username)
    with cd(path.backup('mysql')):
        run('mysqldump --opt --user={user} --password={pwd} {db} | gzip > {db}.sql.gz'.format(
            db=dbname, user=username, pwd=password))


def restore(dbname, username, password):
    """Restore MySQL database from backup."""
    dbname = _prepare_dbname(dbname, username)
    with cd(path.backup('mysql')):
        for command, file_name in fs.first_existing(
            ('gunzip <', '{}.sql.gz'.format(dbname)),
            ('cat', '{}.sql'.format(dbname)),
        ):
            run('{cmd} {file} | mysql --user={user} --password={pwd} {db}'.format(
                cmd=command, file=file_name, user=username, pwd=password, db=dbname))


def scp(server_from, dbname, username):
    dbname = _prepare_dbname(dbname, username)
    fs.scp(server_from, path.sql(path.backup('mysql', dbname)))


def _run_ddl(statement, *args, **kwargs):
    """Run DDL statement as dbadmin."""
    require('mysql_admin', 'mysql_password')
    s = statement.format(*args, **kwargs)
    run('echo "{s}" | mysql --batch --user={user} --password={pwd}'.format(
        s=s, user=env.mysql_admin, pwd=env.mysql_password))


def _prepare_dbname(dbname, username):
    return username if dbname == username or dbname == "" or dbname is None else '{}_{}'.format(username, dbname)
