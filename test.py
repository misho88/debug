#!/usr/bin/env python3

from debug import debug
from functools import partial


def inner():
    debug('in inner')


def outer():
    inner()

debug('not in a function')
inner()
outer()

λ = lambda: debug('in a lambda')
λ()


def debug_wrapper(*args, **kwargs):
    return debug('wrapped', *args, caller=2, **kwargs)


def inner_wrapper():
    debug_wrapper('inner_wrapper')


inner_wrapper()

partial(inner)()
