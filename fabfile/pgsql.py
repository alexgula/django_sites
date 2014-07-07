# coding=utf-8
from fabric.api import task, require
from .util import pgsql

@task
def backup(database=None):
    """Backup remote database."""
    require('hosts', 'site_tasks', 'local_pgsql_backup_dir', 'pgsql_username', 'pgsql_port')
    pgsql.backup(database)