# coding=utf-8
from time import time


def timed_iterator(iterator):
    start = time()
    for value in iterator:
        stop = time()
        yield stop - start, value
        start = time()
