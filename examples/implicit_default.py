#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# implicit_default.py

#
# Compatible Python >= 3.6.*
# Do not use the code in this file
#

from abd import ABD


# this is a decorator
class Default(ABD):
    """Decorator that accepts options
    The options should represent the keyword and default arguments for
      the decorated/wrapped function.

    The priority is as follows:
        given > decorator > default parameter

    It is not recommended to overwrite a default parameter
      with a decorator.
    Explicit is better than implicit.

    Example usage:
    >>> @Default(a=1, b=2)
    ... def func(a, b=3):
    ...     return a, b
    ...
    >>> func()
    (1, 2)
    >>> func('a')
    ('a', 2)
    >>> func(b='b')
    (1, 'b')
    """
    def invoke(self, *args, **kwargs) -> object:
        """Gets called when the decorated function is called"""
        # get the parameters
        params = self.decorated_object.__code__.co_varnames
        # get the decorator options
        _, deco_kwargs = self.decorator_options
        kwargs = {**deco_kwargs, **kwargs}  # overwrite given defaults
        kwargs = {**kwargs, **dict(zip(params, args))}  # args have priority
        return self.decorated_object(**kwargs)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
