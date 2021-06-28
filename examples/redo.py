#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# redo.py

#
# Compatible Python >= 3.6.*
# Do not use the code in this file
#

from collections import deque

from abd import ABD


# this is a decorator
class Redo(ABD):
    """Decorator that keeps track of the inputs
    gives the options: `redo_last` and `redo_first`
      to the decorated function

    Example usage:
    >>> @Redo
    ... def func(num: int) -> int:
    ...     print(num, end='')
    ...     return num
    ...
    >>> for i in range(10):
    ...     _ = func(i)  # discard result
    ...
    0123456789
    >>> _ = func.redo_last(10)  # discard result list
    9876543210
    >>> _ = func.redo_first(5)  # discard result list
    01234
    >>> result = func.redo_last(3)
    987
    >>> result  # check last results
    [9, 8, 7]
    """
    _memory: deque = None  # saves

    def __init__(self, *args, maxlen: int = 100, **kwargs) -> None:
        """keyword argument maxlen indicates the max length of memory"""
        self._memory = deque(maxlen=maxlen)
        super(Redo, self).__init__(*args, **kwargs)

    def __redo(self, _memory) -> list:
        return [self.decorated_object(*args, **kwargs)
                for args, kwargs in _memory]

    def redo_last(self, num: int = 1) -> list:
        """redo the last `num` amount of times"""
        num = abs(num)
        if not num <= 0:
            redo = [m for m, _ in zip(reversed(self._memory), range(num))]
            return self.__redo(redo)

    def redo_first(self, num: int = 1) -> list:
        """redo the first `num` amount of times"""
        num = abs(num)
        if not num <= 0:
            redo = [m for m, _ in zip(self._memory, range(num))]
            return self.__redo(redo)

    def invoke(self, *args, **kwargs) -> object:
        """Is called when the decorated function is called"""
        # save the given (keyword) arguments
        self._memory.append((args, kwargs))
        # call and return the result of the decorated function
        return self.decorated_object(*args, **kwargs)


if __name__ == '__main__':
    @Redo
    def func(num):
        print(num, end='')
        return num

    for i in range(10):
        func(i)

    print()  # newline
    res = func.redo_last(10)

    print()  # newline
    print(res)  # print list of results from func
