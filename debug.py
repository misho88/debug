'''print-like function for debugging

>>> from debug import debug
>>> debug('here')
<stdin>[1]: here
>>> def doit(): debug('in doit')
...
>>> doit()
<stdin>[1]: doit(): in doit
'''

__all__ = 'debug',

from sys import stderr
from os.path import relpath, abspath, sep, commonpath, curdir
from inspect import currentframe
from types import FrameType


def get_function_name(frame):
    if hasattr(frame.f_code, 'co_qualname'):
        return frame.f_code.co_qualname

    try:
        from executing import Source
    except (ModuleNotFoundError, ImportError):
        return frame.f_code.co_name

    name = Source.executing(frame).code_qualname()
    assert name.endswith(frame.f_code.co_name)
    assert name.rfind('.') + 1 == len(name) - len(frame.f_code.co_name)
    return name


def get_lambda_name(frame):
    parent = frame.f_back
    if parent is None:
        return frame.f_code.co_name

    qualname = get_function_name(frame)

    for mapping in parent.f_locals, parent.f_globals, parent.f_builtins:
        for name, attr in mapping.items():
            if getattr(attr, '__code__', None) is frame.f_code:
                return f'{qualname[:-len(frame.f_code.co_name)]}<{name}>'

    return qualname


def stack_functions(frame, max_depth=1024):
    functions = []
    depth = 0
    while depth < max_depth and frame and frame.f_code.co_name != '<module>':
        func = frame.f_code.co_name
        if func == '<lambda>':
            func = get_lambda_name(frame)
        else:
            func = get_function_name(frame)

        functions.append(func)
        frame = frame.f_back
        depth += 1
    return functions


def context(frame, max_depth=1024):
    path = abspath(frame.f_code.co_filename)
    if commonpath((path, abspath(curdir))) != sep:
        path = relpath(frame.f_code.co_filename)
    line = frame.f_lineno
    funcs = stack_functions(frame, max_depth=max_depth)
    return path, line, funcs


def debug(*args, caller=1, max_depth=1024, sep=': ', file=stderr, **kwargs):
    '''like print, but for debugging

    args: passed to print()
    caller: how many stack frames to go back to reach the caller being debugged
            or the calling frame directly
            default is 1; use 2 or inspect.currentframe() when wrapping debug()
    max_depth: how many stack frames back to go; e.g., 1: only the calling
               function, 2: calling function and its parent, 0: nothing
    sep: like print(), but the default is ': '
    file: file print(), but the default is stderr
    **kwargs: passed to print() (e.g., end='\n' and flush=False)

    Examples:

    Basic:
    >>> debug('msg', 'detail')
    <stdin>[1]: msg: detail
    >>> def func(): debug('msg', 'detail')
    ...
    >>> func()
    <stdin>[1]: func(): msg: detail

    Work out names of lambdas:
    >>> lamb = lambda: debug('msg', 'detail')
    >>> lamb()
    <stdin>[1]: <lamb>(): msg: detail

    Go through the stack:
    >>> f = lambda: debug('xxx')
    >>> g = lambda: f()
    >>> g()
    <stdin>[1]: <g>(): <f>(): xxx

    Customizing via wrapper:
    >>> def debug_xxx(*args, caller=1, **kwargs): debug('xxx', *args, caller=caller + 1, **kwargs)
    ...
    >>> f = lambda: debug_xxx('msg', 'detail')
    >>> f()
    <stdin>[1]: <f>(): xxx: msg: detail

    Customizing via partial:
    >>> from functools import partial
    >>> debug_xxx = partial(debug, 'xxx')
    >>> f = lambda: debug_xxx('msg', 'detail')
    >>> f()
    <stdin>[1]: <f>(): xxx: msg: detail
    '''
    if isinstance(caller, FrameType):
        frame = caller
    else:
        frame = currentframe()
        for _ in range(caller):
            if frame is None:
                break
            frame = frame.f_back
        if frame is None:
            return print(*args, sep=sep, file=file, **kwargs)

    path, line, funcs = context(frame, max_depth=max_depth)
    print(
        f'{path}[{line}]',
        *(f'{f}()' for f in funcs[::-1]),
        *args,
        sep=sep,
        file=file,
        **kwargs,
    )
    return None if len(args) == 0 else args[0] if len(args) == 1 else args
