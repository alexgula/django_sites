# coding=utf-8
import os
import re


def list_all():
    fabric_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    with open(os.path.join(fabric_path, 'acc.list')) as f:
        for line in f.readlines():
            params = re.split(r'\s+', line.strip())
            username = params[0]
            if len(params) == 1:
                yield username, "", []
            else:
                password = params[1]
                dbnames = params[2:] if len(params) > 2 else [username]
                yield username, password, dbnames


def apply_to_all(user_func=None, db_func=None):
    for username, password, dbnames in list_all():
        if user_func is not None:
            user_func(username)
        if db_func is not None:
            for dbname in dbnames:
                db_func(dbname, username, password)
