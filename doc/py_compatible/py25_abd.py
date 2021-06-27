#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# py25_abd.py

#
# Python >=2.5.* compatible
# Do not use the code in this file.
#

import functools

__all__ = ['ABD', 'AbstractBaseDecorator', 'BaseDecorator']


class AbstractBaseDecorator(object):
    """Abstract class to make decorators or wrappers.
    To create a decorator or a wrapper:
      Inherit this class and add the `invoke` function to the class.
    The decorators accepts arguments & keyword arguments.
    """
    # class attributes
    _deco_args = ()  # type: tuple
    _deco_kwargs = {}  # type: dict
    _decorated_obj = None  # type: callable

    @property
    def decorated_object(self):
        # type: () -> callable
        """
        Returns the function that is decorated.
        This should be used/called in AbstractBaseDecorator.invoke
          to change the behavior of the decorated function.
        :return: The decorated/wrapped function
        :rtype: callable
        """
        return self._decorated_obj

    @property
    def decorator_options(self):
        # type: () -> (tuple, dict)
        """Return the arguments or keyword arguments
        These are given when the creating a new class instance
        :return: The options; (arguments, keyword arguments)
        :rtype: tuple, dict
        """
        return self._deco_args, self._deco_kwargs

    def __repr__(self):
        # type: () -> str
        """A visual representation that dynamically returns
          <@><class name><(options)>< -> decorated function>
        :return: A string representing the decorator and function
        :rtype: str
        """
        at, func, options = '', '', ''
        class_name = self.__class__.__qualname__
        # join args and kwargs for representation
        args, kwargs = '', ''
        for arg in self._deco_args:
            args = args + '{0}, '.format(repr(arg))
        for key, val in self._deco_kwargs.items():
            kwargs = kwargs + '{0}={1}, '.format(key, repr(val))
        # apply options
        if args or kwargs:
            if args and kwargs:
                args = "{0}, ".format(args)
            else:
                args = args
            options = '({0}{1})'.format(args, kwargs)
        if hasattr(self, '__name__'):
            at, func = '@', ' -> {0}'.format(self.__name__)
        # return dynamic representation
        return '{0}{1}{2}{3}'.format(at, class_name, options, func)

    def __init__(self, *args, **kwargs):
        # type: (*object, **object) -> None
        """Initialization function of the class.
        The 1st argument is considered to be the
          decorated or wrapped function.
        This function is stored and accessible with `decorated_object`
        The given arguments & keyword arguments are saved.
        These are accessible by `decorator_options`
        New options can be set by `set_decorator_options`
        :param args: The first argument is expected to be the callable.
        And is thus separated from the other arguments.
        Is this not the case, all the arguments are respected.
        :param kwargs: key=`value` pair keyword arguments
        """
        # If 1st element is a callable it will be separated
        function, args = self._pop_callable(*args)

        # always point to the original function
        if isinstance(function, type(self)):
            function = function.decorated_object

        # save or overwrite previous options
        if self._decorated_obj is None:
            self.set_decorator_options(*args, **kwargs)

        # set the function as the decorated object
        if callable(function) and self._decorated_obj is None:
            self._decorate(function)

    def __call__(self, *args, **kwargs):
        # type: (*object, **object) -> object or callable
        """This function is invoked
          when the decorated/wrapped function is called.
        Or when an instance of this class gets decorated/wrapped again.
        If the latter is the case,
          the 1st argument is the decorated function.
        Also __init__ will catch the arguments & keyword arguments.
        :param args: All the arguments are passed to `invoke`
        :param kwargs: All the key=value pair keyword arguments
          are passed to `invoke`
        :return: `self` or the result of the decorated/wrapped function
        :rtype: `self` or object
        """
        # If 1st element is a callable it will be separated
        function, args = self._pop_callable(*args)

        # always point to the original function
        if isinstance(function, type(self)):
            function = function._decorated_obj

        # set the function as the decorated object
        if callable(function) and self._decorated_obj is None:
            self._decorate(function)
            return self  # don't invoke

        # call invoke where the function is called
        return self.invoke(*args, **kwargs)

    @staticmethod
    def _pop_callable(*args):
        # type: (*object) -> (callable, tuple) or (None, tuple)
        function = None
        if args and callable(args[0]):
            if len(args) > 1:
                function, args = args[0], args[1:]
            else:
                function, args = args[0], ()
        return function, tuple(args)

    def _decorate(self,
                  function  # type: callable
                  ):
        # type: (*object, **object) -> None
        """Set the given function as the decorated function."""
        functools.update_wrapper(self, function)
        self._decorated_obj = function

    def set_decorator_options(self, *args, **kwargs):
        # type: (*object, **object) -> None
        """Set or override the options of the decorator."""
        self._deco_args = args
        self._deco_kwargs = kwargs

    def invoke(self, *args, **kwargs):
        # type: (*object, **object) -> object
        """When the decorated function is called
          this function is called by __call__.
        This must be overridden by the class that inherit this class.
        """
        return self._decorated_obj(*args, **kwargs)


# Monkey patch
ABD = AbstractBaseDecorator


class BaseDecorator(ABD):
    """Most basic decorator"""

    def invoke(self, *args, **kwargs):
        # type: (*object, **object) -> object
        return self._decorated_obj(*args, **kwargs)


if __name__ == '__main__':
    """Local tests"""
    Deco = Deco1 = Deco2 = BaseDecorator

    # 1 - Decorator without options
    @Deco
    def func(*args, **kwargs):
        return args, kwargs
    assert func.decorator_options == ((), {})
    assert func('arg', kw='kwarg') == (('arg',), {'kw': 'kwarg'})

    # equal to
    def func(*args, **kwargs):
        return args, kwargs
    func = Deco(func)
    assert func.decorator_options == ((), {})
    assert func('arg', kw='kwarg') == (('arg',), {'kw': 'kwarg'})

    # 2 - Decorator with options
    @Deco('opt', opt='opt')
    def func(*args, **kwargs):
        return args, kwargs
    assert func.decorator_options == (('opt',), {'opt': 'opt'})
    assert func('arg', kw='kwarg') == (('arg',), {'kw': 'kwarg'})

    # equal to
    def func(*args, **kwargs):
        return args, kwargs
    func = Deco(func, 'opt', opt='opt')
    assert func.decorator_options == (('opt',), {'opt': 'opt'})
    assert func('arg', kw='kwarg') == (('arg',), {'kw': 'kwarg'})

    # 3 - Decorator stack, outer without options, inner with options
    @Deco2
    @Deco1('opt', opt='opt')
    def func(*args, **kwargs):
        return args, kwargs
    assert func.decorator_options == ((), {})
    assert func('arg', kw='kwarg') == (('arg',), {'kw': 'kwarg'})

    # equal to
    def func(*args, **kwargs):
        return args, kwargs
    func = Deco2(Deco1(func, 'opt', opt='opt'))
    assert func.decorator_options == ((), {})
    assert func('arg', kw='kwarg') == (('arg',), {'kw': 'kwarg'})

    # 4 - Decorator stack, outer with options, inner without options
    @Deco2('opt', opt='opt')
    @Deco1
    def func(*args, **kwargs):
        return args, kwargs
    assert func.decorator_options == (('opt',), {'opt': 'opt'})
    assert func('arg', kw='kwarg') == (('arg',), {'kw': 'kwarg'})

    # equal to
    def func(*args, **kwargs):
        return args, kwargs
    func = Deco2(Deco1(func), 'opt', opt='opt')
    assert func.decorator_options == (('opt',), {'opt': 'opt'})
    assert func('arg', kw='kwarg') == (('arg',), {'kw': 'kwarg'})

    # 5 - Wrapper without options
    def func(*args, **kwargs):
        return args, kwargs
    wrapper = Deco(func)
    assert not hasattr(func, 'decorator_options')
    assert wrapper.decorator_options == ((), {})
    assert func('arg', kw='kwarg') == (('arg',), {'kw': 'kwarg'})
    assert wrapper('arg', kw='kwarg') == (('arg',), {'kw': 'kwarg'})

    # 6 - Wrapper with options
    def func(*args, **kwargs):
        return args, kwargs
    wrapper = Deco(func, 'opt', opt='opt')
    assert not hasattr(func, 'decorator_options')
    assert wrapper.decorator_options == (('opt',), {'opt': 'opt'})
    assert func('arg', kw='kwarg') == (('arg',), {'kw': 'kwarg'})
    assert wrapper('arg', kw='kwarg') == (('arg',), {'kw': 'kwarg'})

    # 7 - Wrap (without options) a decorated function (without options)
    @Deco1
    def func(*args, **kwargs):
        return args, kwargs
    wrapper = Deco2(func)
    assert func.decorator_options == ((), {})
    assert wrapper.decorator_options == ((), {})
    assert func('arg', kw='kwarg') == (('arg',), {'kw': 'kwarg'})
    assert wrapper('arg', kw='kwarg') == (('arg',), {'kw': 'kwarg'})

    # equal to
    def func(*args, **kwargs):
        return args, kwargs
    func = Deco1(func)
    wrapper = Deco2(func)
    assert func.decorator_options == ((), {})
    assert wrapper.decorator_options == ((), {})
    assert func('arg', kw='kwarg') == (('arg',), {'kw': 'kwarg'})
    assert wrapper('arg', kw='kwarg') == (('arg',), {'kw': 'kwarg'})

    # 8 - Wrap (with options) a decorated function (without options)
    @Deco1
    def func(*args, **kwargs):
        return args, kwargs
    wrapper = Deco2(func, 'opt', opt='opt')
    assert func.decorator_options == ((), {})
    assert wrapper.decorator_options == (('opt',), {'opt': 'opt'})
    assert func('arg', kw='kwarg') == (('arg',), {'kw': 'kwarg'})
    assert wrapper('arg', kw='kwarg') == (('arg',), {'kw': 'kwarg'})

    # equal to
    def func(*args, **kwargs):
        return args, kwargs
    func = Deco1(func)
    wrapper = Deco2(func, 'opt', opt='opt')
    assert func.decorator_options == ((), {})
    assert wrapper.decorator_options == (('opt',), {'opt': 'opt'})
    assert func('arg', kw='kwarg') == (('arg',), {'kw': 'kwarg'})
    assert wrapper('arg', kw='kwarg') == (('arg',), {'kw': 'kwarg'})

    # 9 - Wrap (without options) a decorated function (with options)
    @Deco1('opt', opt='opt')
    def func(*args, **kwargs):
        return args, kwargs
    wrapper = Deco2(func)
    assert func.decorator_options == (('opt',), {'opt': 'opt'})
    assert wrapper.decorator_options == ((), {})
    assert func('arg', kw='kwarg') == (('arg',), {'kw': 'kwarg'})
    assert wrapper('arg', kw='kwarg') == (('arg',), {'kw': 'kwarg'})

    # equal to
    def func(*args, **kwargs):
        return args, kwargs
    func = Deco1(func, 'opt', opt='opt')
    wrapper = Deco2(func)
    assert func.decorator_options == (('opt',), {'opt': 'opt'})
    assert wrapper.decorator_options == ((), {})
    assert func('arg', kw='kwarg') == (('arg',), {'kw': 'kwarg'})
    assert wrapper('arg', kw='kwarg') == (('arg',), {'kw': 'kwarg'})

    # 10 - Wrap (with options) a decorated function (with options)
    @Deco1('opt', opt='opt')
    def func(*args, **kwargs):
        return args, kwargs
    wrapper = Deco2(func, 'opt', opt='opt')
    assert func.decorator_options == (('opt',), {'opt': 'opt'})
    assert wrapper.decorator_options == (('opt',), {'opt': 'opt'})
    assert func('arg', kw='kwarg') == (('arg',), {'kw': 'kwarg'})
    assert wrapper('arg', kw='kwarg') == (('arg',), {'kw': 'kwarg'})

    # equal to
    def func(*args, **kwargs):
        return args, kwargs
    func = Deco1(func, 'opt', opt='opt')
    wrapper = Deco2(func, 'opt', opt='opt')
    assert func.decorator_options == (('opt',), {'opt': 'opt'})
    assert wrapper.decorator_options == (('opt',), {'opt': 'opt'})
    assert func('arg', kw='kwarg') == (('arg',), {'kw': 'kwarg'})
    assert wrapper('arg', kw='kwarg') == (('arg',), {'kw': 'kwarg'})
