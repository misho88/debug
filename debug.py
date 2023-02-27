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
from inspect import currentframe
from pathlib import Path
from types import FrameType


def stack_functions(frame, max_depth=1024):
    functions = []
    depth = 0
    while depth < max_depth and frame and frame.f_code.co_name != '<module>':
        parent = frame.f_back
        func = frame.f_code.co_name
        if func == '<lambda>' and parent is not None:
            for mapping in parent.f_locals, parent.f_globals, parent.f_builtins:
                for name, attr in mapping.items():
                    if getattr(attr, '__code__', None) is frame.f_code:
                        func = f'<{name}>'
                        break
                else:
                    continue
                break
        functions.append(func)
        frame = parent
        depth += 1
    return functions


def context(frame, max_depth=1024):
    path = Path(frame.f_code.co_filename).resolve().relative_to(Path().resolve())
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
    return print(
        f'{path}[{line}]',
        *(f'{f}()' for f in funcs[::-1]),
        *args,
        sep=sep,
        file=file,
        **kwargs,
    )
