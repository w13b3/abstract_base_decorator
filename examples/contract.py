#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# contract.py

#
# Compatible Python >= 3.8.*
# Do not use the code in this file
#

import typing
from typing import get_origin, get_type_hints, get_args

import inspect
from inspect import Signature
from functools import lru_cache

from abd import ABD

# placeholder to indicate the not annotated (keyword) arguments
_EMPTY: object = Signature.empty


# this is a decorator
class Contract(ABD):
    """Decorator that assures the received types
    are of the defined annotations.
    It checks -input- (keyword) arguments and the -output- return value.
    It doesn't check the value types within container datatypes.

    Example usage:
    >>> from typing import Union
    >>> @Contract
    ... def func(a: str, b: int, c: Union[set, dict]) -> list:
    ...     if b > 2:
    ...         return [a, b, c]  # -> list
    ...     else:
    ...         return (c, b, a)  # -> tuple (not as annotated)
    ...
    >>> func('union dict', 10, {1: 2})  # input and output are as annotated
    ['union dict', 10, {1: 2}]
    >>> func('union set', 10, {1, 2})  # input and output are as annotated
    ['union set', 10, {1, 2}]
    >>> func('b', 1, {3, 4})  # output tuple, not list; expect TypeError
    Traceback (most recent call last):
        ...
    TypeError: return type: ({3, 4}, 1, 'b'), is not of type: <class 'list'>
    >>> func(1, 2, 3)  # input types are not correct; expect TypeError
    Traceback (most recent call last):
        ...
    TypeError: func(a: str) received: 1 (int)
    """
    _func_annotations: dict = {}
    _return_annotation: type = None

    @property
    def annotations(self) -> dict:
        """Return a dict of the function it's parameters sans empty ones"""
        anno = {**self._func_annotations, 'return': self._return_annotation}
        return {k: v for k, v in anno.items() if v is not _EMPTY}

    def __init__(self, *args, incoming: bool = True,
                 outgoing: bool = True, **kwargs) -> None:
        """Decorator init.
        incoming: Option to check incoming value(s). Default True.
        outgoing: Option to check outgoing value(s). Default True.
        """
        kwargs.update({'incoming': incoming, 'outgoing': outgoing})
        super(Contract, self).__init__(*args, **kwargs)

    @lru_cache
    def _store_annotations(self, func: callable = None) -> None:
        """Store the annotations of the decorated function"""
        func = func or self.decorated_object
        hints: dict = get_type_hints(func)
        signature: Signature = inspect.signature(func)
        self._return_annotation: type = hints.pop('return', _EMPTY)
        # get the best possible annotations
        _dict: dict = {}
        for param, anno in signature.parameters.items():
            # annotation = most accurate --or-> given --or-> default
            _dict[param] = hints.get(param) or anno.annotation or _EMPTY
        self._func_annotations = _dict  # store the annotations

    def _check_instance(self, val, type_) -> bool:
        """Check if the given value is an instance of the given type"""
        return isinstance(val, self._unpack_types(type_))

    def _unpack_types(self, type_) -> tuple:
        """Unpacking typing.Union to return a tuple of type origins
        or return a tuple of the single type
        """
        type_args = (type_,)
        if (org := get_origin(type_)) and type(org).__name__ in dir(typing):
            type_args = get_args(type_)  # get the arguments of the Union
        type_args = (t for t in type_args)  # fix to accept single type
        return tuple(get_origin(t) or t for t in type_args)  # base types

    def __check_arguments(self, *args) -> None:
        """Check the type of arguments against the annotations"""
        err = "{0}({1}: {2}) received: {3} ({4})"
        for arg, (name, anno) in zip(args, self._func_annotations.items()):
            if anno is not _EMPTY:
                if not self._check_instance(arg, anno):
                    func, type_ = self.__name__, type(arg).__name__
                    e = err.format(func, name, anno.__name__, arg, type_)
                    raise TypeError(e)

    def __check_keyword_arguments(self, **kwargs) -> None:
        """Check the type of the keyword-values against the annotations"""
        err = "{0}({1}: {2}) received: {3} ({4})"
        for key, val in kwargs.items():
            if (anno := self._func_annotations.get(key, _EMPTY)) is not _EMPTY:
                if not self._check_instance(val, anno):
                    func, type_ = self.__name__, type(val).__name__
                    e = err.format(func, key, anno.__name__, val, type_)
                    raise TypeError(e)

    def __check_return_value(self, ret_val: object) -> None:
        """Check the type of the return value against the return annotation"""
        err = "return type: {0}, is not of type: {1}"
        if not self._check_instance(ret_val, self._return_annotation):
            e = err.format(ret_val, self._return_annotation)
            raise TypeError(e)

    def invoke(self, *args: object, **kwargs: object) -> object:
        """Gets called when the decorated function is called"""
        # store annotations of the decorated function
        self._store_annotations(self.decorated_object)
        # get options
        deco_args, deco_kwargs = self.decorator_options
        if deco_kwargs.get('incoming'):  # set by init
            # check the incoming values on their types
            self.__check_arguments(*args)
            self.__check_keyword_arguments(**kwargs)
        # call the decorated function
        result = self.decorated_object(*args, **kwargs)
        if self._return_annotation is not _EMPTY \
                and deco_kwargs.get('outgoing'):  # set by init
            # check the result of the function on it's type
            self.__check_return_value(result)
        return result


if __name__ == '__main__':
    import doctest
    doctest.testmod()
