# coding=utf-8
import os
import datetime


def for_date(timestamp):
    zerodate = datetime.datetime(2009, 5, 8)
    dayseconds = timestamp.hour * 3600 + timestamp.minute * 60 + timestamp.second
    return (timestamp - zerodate).days * 100000 + dayseconds


def for_file(path):
    mtime = os.path.getmtime(path)
    timestamp = datetime.datetime.fromtimestamp(mtime)
    return for_date(timestamp)
