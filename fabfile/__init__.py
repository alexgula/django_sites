# coding=utf-8
import os
import yaml
from fabric.api import env, task, require
from .util import path
from .models import config
from . import acc, dj, mysql, pgsql, srv

# Fabric
env.always_use_pty = True

# Local paths
env.root_path = os.path.abspath(os.path.dirname(__file__))

ROOT_PATH = os.path.dirname(env.root_path)

env.local_etc_dir = os.path.join(ROOT_PATH, 'conf', 'etc')
env.local_config_dir = os.path.join(ROOT_PATH, 'conf', 'accounts')
env.local_template_dir = os.path.join(ROOT_PATH, 'conf', 'service_templates')
env.local_pgsql_backup_dir = os.path.join(ROOT_PATH, 'db', 'backups')

# Mercurial
env.tag = 'tip'  # 'production'

# Django
env.settings = 'settings_prod'

# Load config from file into environment
with open(path.env_config()) as f:
    env.update(yaml.load(f))

@task
def d():
    """Set local paths, keys for example, to drive D."""
    set_local('D')


@task
def e():
    """Set local paths, keys for example, to drive E."""
    set_local('E')


@task
def on(server):
    """Set the target to operate."""
    set_target(server)


@task
def py(server='hps1'):
    """Set the target to Django."""
    set_target(server)
    env.user = 'django'
    env.django_user = '{user}@{hosts[0]}'.format(**env)
    env.remote_django_sync = 'ssh://{}/{}'.format(env.django_user, path.account('django'))


def set_local(drive):
    """Set the local paths."""
    env.local_drive = drive


def set_target(server):
    """Set the target."""

    server_convig = env.servers[server]

    env.key_filename = r'{}:\Picassoft\Hosting\keys\{}.openssl.key'.format(env.local_drive, server_convig['key'])
    env.putty_key_filename = r'{}:\Picassoft\Hosting\keys\{}.ppk'.format(env.local_drive, server_convig['key'])
    env.hg_config = 'ui.ssh="TortoisePlink.exe -ssh -2 -i {}"'.format(env.putty_key_filename)

    # Connection
    env.hosts = ['{}.picassoft.com.ua'.format(server)]
    env.user = server_convig.get('user', 'ubuntu')

    # SCP connection
    env.user_scp = 'root'

    # Remote paths
    env.remote_web_dir = '/web'

    # Remote MySQL
    env.mysql_admin = server_convig.get('mysql_admin', 'root')
    env.mysql_password = server_convig.get('mysql_password', 'numelore0010')

    # Remote PostgreSQL
    env.pgsql_username = server_convig.get('pgsql_username', 'postgres')
    env.pgsql_port = server_convig.get('pgsql_port', 5432)

    # Services classes
    env.service_handlers = config.init_services(server_convig.get('name'), env.services)
