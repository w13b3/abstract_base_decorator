#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# logio.py

#
# Compatible Python >= 3.6.*
# Do not use the code in this file
#

import logging
import functools  # wraps
import itertools  # count

from abd import ABD


# this is a class decorator
class LogIO(ABD):
    """Decorator for classes
    logs all the input & output of class methods
    Example usage:
    >>> import io, logging
    >>> stream = io.StringIO()
    >>> logging.basicConfig(level=logging.DEBUG, stream=stream)
    >>> @LogIO(level=logging.INFO)
    ... class Recursive:
    ...     def func(self, num: int, count: int = 0):
    ...         if num == 0:
    ...             return num
    ...         else:  # recursive
    ...             self.func(num - 1, count + 1)
    ...
    >>> _ = Recursive().func(2)  # catch the return value
    >>> print(stream.getvalue())
    INFO:root:0 input: func(2 )
    INFO:root:1 input: func(1, 1 )
    INFO:root:2 input: func(0, 2 )
    INFO:root:2 output func: 0
    INFO:root:1 output func: None
    INFO:root:0 output func: None
    """
    # count to keep track of the input/output in the log
    _c = itertools.count()

    def _log(self, func, *opt, **options) -> callable:
        """Wrapper for the to log InputOutput"""
        # get the option: level, default DEBUG
        loglvl = options.get('level', logging.DEBUG)

        @functools.wraps(func)
        def innerfunc(*args, **kwargs) -> object:
            nonlocal self  # get `self`
            # create a log text
            count = next(self._c)
            func_name = func.__name__
            _args = ', '.join(repr(a) for a in args)
            _kwargs = ', '.join(f'{k}: {v!r}' for k, v in kwargs.items())
            log = f'{count} input: {func_name}({_args} {_kwargs})'
            logging.log(loglvl, log)  # log the input
            res = func(*args, **kwargs)  # call the wrapped function
            log = f'{count} output {func_name}: {res!r:100}'
            logging.log(loglvl, log)  # log the output
            return res  # return result of the wrapped function
        return innerfunc

    def invoke(self, *args, **kwargs) -> object:
        """Gets called when the decorated function is called"""
        # get the decorator options
        deco_args, deco_kwargs = self.decorator_options
        # initialize the class
        class_instance = self.decorated_object(*args, **kwargs)
        # loop over all the methods except the private and magic ones
        cdir = (c for c in dir(class_instance)
                if not c.startswith('__')
                and callable(getattr(class_instance, c)))
        for func in cdir:
            # get the method attribute
            method = getattr(class_instance, func)
            # wrap the log method
            wrap = self._log(method, **deco_kwargs)  # level=10
            # apply the wrapped method onto the class
            setattr(class_instance, func, wrap)
        return class_instance


if __name__ == '__main__':
    import doctest
    flags = doctest.NORMALIZE_WHITESPACE | doctest.DONT_ACCEPT_BLANKLINE
    doctest.testmod(optionflags=flags)
