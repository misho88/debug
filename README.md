# debug
print-like function for debugging

# usage

Use `debug()` like print, but it will also tell you where it was called from.

```
>>> from debug import debug
>>> debug('xxx')
<stdin>[1]: xxx
>>> def f(): debug('in f')
...
>>> f()
<stdin>[1]: f(): in f
>>> def g(): f()
...
>>> g()
<stdin>[1]: g(): f(): in f
```

It tries to get the names of lambdas, too:

```
>>> def h(): λ = lambda: debug('in λ'); λ()
...
>>> h()
<stdin>[1]: h(): <λ>(): in λ
```

# TO DO:

- handle nested functions better
- handle class methods better
