# coding=utf-8
from contextlib import contextmanager
from functools import wraps
import json


@contextmanager
def ignored(*exceptions):
    try:
        yield
    except exceptions:
        pass


