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

def outer_lambda():
    iλ = lambda: debug('in lambda')
    iλ()

outer_lambda()


def outer():
    def inner():
        debug('here')
    return inner

outer()()


class C:
    def func():
        debug('func')
    def meth(self):
        debug('meth')


C.func()
C().meth()
