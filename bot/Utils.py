import functools
import time
from datetime import datetime


def timeit(func):
    @functools.wraps(func)
    def newfunc(*args_, **kwargs):
        start_time = time.time()
        res = func(*args_, **kwargs)
        elapsed_time = time.time() - start_time
        print('function [{}] finished in {} msec'.format(
            func.__name__, int(elapsed_time * 1000)))
        return res
    return newfunc


def ut2dt(time):
    return datetime.fromtimestamp(time / 1000)