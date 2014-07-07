# coding=utf-8
from functools import wraps

def coroutine(fun):
    @wraps(fun)
    def wrapper(*args, **kwargs):
        c = fun(*args, **kwargs)
        c.next()
        return c
    return wrapper

def multiranges(num, times, target):
    for t in xrange(times):
        for i in xrange(num):
            target.send(i)

@coroutine
def filter(test, target):
    while True:
        val = (yield)
        if test(val):
            target.send(val)

@coroutine
def multicast(*targets):
    while True:
        val = (yield)
        for target in targets:
            target.send(val)

@coroutine
def receive_print(pattern="{0}"):
    while True:
        val = (yield)
        print(pattern.format(val))

if __name__ == '__main__':
    def simple_test(test_val):
        return lambda val: val == test_val

    rp = receive_print()
    f1 = filter(simple_test(2), rp)
    f2 = filter(simple_test(4), rp)
    pipe = multicast(f1, f2)
    multiranges(5, 3, pipe)
