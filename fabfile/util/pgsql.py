# coding=utf-8
from fabric.api import env, require, local


def backup(database=None):
    """Backup remote database."""
    require('hosts', 'site_tasks', 'local_pgsql_backup_dir', 'pgsql_username', 'pgsql_port')

    if database is None:
        databases = env.site_tasks['backup']
    else:
        databases = [database]

    for database in databases:
        local('pg_dump.exe --host {host} --port {port} --username "{username}" --no-password --format custom --blobs --clean --file "{backup_path}\{database}.backup" "{database}"'.format(
            backup_path=env.local_pgsql_backup_dir,
            host=env.hosts[0],
            username=env.pgsql_username,
            port=env.pgsql_port,
            database=database
        ))
