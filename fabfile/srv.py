# coding=utf-8
import os
from fabric.api import env, task, require, sudo, put
from .util import path, fs


@task
def deploy(service_seq, *args):
    upload(service_seq, *args)
    restart(service_seq)


@task
def restart(service_seq):
    """Restart service by name(s). Service names are built of string of first letters of each service."""
    require('services')
    for service_char in service_seq:
        sudo('service {} restart'.format(env.service_handlers[service_char].service_name))


@task
def generate(service_seq, *args):
    """Upload service configuration for the given service name(s) and account list."""
    for result in generate_iter(service_seq, *args):
        print(result)


@task
def upload(service_seq, *args):
    for result in generate_iter(service_seq, *args):
        put_config(*result)


def generate_iter(service_seq, *args):
    for service_code in service_seq:
        for result in env.service_handlers[service_code].generate(*args):
            yield result


def put_config(local_path, remote_path):
    put(local_path, remote_path, mode=0644, use_sudo=True)
    fs.chown('root', remote_path)
