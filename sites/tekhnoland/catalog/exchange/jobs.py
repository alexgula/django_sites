# coding=utf-8
from contextlib import contextmanager
import redis
from django.conf import settings

STATUS_STARTING = 'starting'
STATUS_STARTED = 'started'
STATUS_PENDING = 'pending'
STATUS_ERROR = 'error'
STATUS_FINISHED = 'finished'


def _connect():
    return redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


def _job_key(key):
    return '{}_{}'.format(settings.EXCHANGE1C_REDIS_CURRENT_KEY, key)


def queue(key):
    if get_status(key) is None:
        set_status(key, STATUS_PENDING)
        return _connect().lpush(settings.EXCHANGE1C_REDIS_QUEUE, key)
    return None


def get():
    key = _connect().rpop(settings.EXCHANGE1C_REDIS_QUEUE)
    if key is None:
        return True, None
    key_status = get_status(key)
    if key_status is None:
        return False, None
    if key_status == STATUS_PENDING:
        set_status(key, STATUS_STARTING)
        return False, key
    return True, None


@contextmanager
def run(key):
    set_status(key, STATUS_STARTED)
    try:
        yield
        set_status(key, STATUS_FINISHED)
    except Exception:
        set_status(key, STATUS_ERROR)
        raise


def set_status(key, status):
    result = _connect().set(_job_key(key), status)
    _connect().expire(_job_key(key), 24 * 60 * 60)
    return result


def get_status(key):
    return _connect().get(_job_key(key))


def del_status(key):
    return _connect().delete(_job_key(key))
