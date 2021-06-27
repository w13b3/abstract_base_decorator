#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# test_decorator_patterns.py

import unittest

from abd import BaseDecorator


class DecoratorPatternsTest(unittest.TestCase):

    # 1 - Decorator without options
    def test_decorator_without_options(self):
        Deco = BaseDecorator

        @Deco
        def func(*args, **kwargs):
            return args, kwargs

        self.assertEqual(func.decorator_options, ((), {}))
        self.assertEqual(func('arg', kw='kwarg'), (('arg',), {'kw': 'kwarg'}))

        # equal to
        def func(*args, **kwargs):
            return args, kwargs

        func = Deco(func)
        self.assertEqual(func.decorator_options, ((), {}))
        self.assertEqual(func('arg', kw='kwarg'), (('arg',), {'kw': 'kwarg'}))

    # 2 - Decorator with options
    def test_with_options(self):
        Deco = BaseDecorator

        @Deco('opt', opt='opt')
        def func(*args, **kwargs):
            return args, kwargs

        self.assertEqual(func.decorator_options, (('opt',), {'opt': 'opt'}))
        self.assertEqual(func('arg', kw='kwarg'), (('arg',), {'kw': 'kwarg'}))

        # equal to
        def func(*args, **kwargs):
            return args, kwargs

        func = Deco(func, 'opt', opt='opt')
        self.assertEqual(func.decorator_options, (('opt',), {'opt': 'opt'}))
        self.assertEqual(func('arg', kw='kwarg'), (('arg',), {'kw': 'kwarg'}))

    # 3 - Decorator stack, outer without options, inner with options
    def test_decorator_stack_outer_without_options_inner_with_options(self):
        Deco1 = Deco2 = BaseDecorator

        @Deco2
        @Deco1('opt', opt='opt')
        def func(*args, **kwargs):
            return args, kwargs

        self.assertEqual(func.decorator_options, ((), {}))
        self.assertEqual(func('arg', kw='kwarg'), (('arg',), {'kw': 'kwarg'}))

        # equal to
        def func(*args, **kwargs):
            return args, kwargs

        func = Deco2(Deco1(func, 'opt', opt='opt'))
        self.assertEqual(func.decorator_options, ((), {}))
        self.assertEqual(func('arg', kw='kwarg'), (('arg',), {'kw': 'kwarg'}))

    # 4 - Decorator stack, outer with options, inner without options
    def test_decorator_stack_outer_with_options_inner_without_options(self):
        Deco1 = Deco2 = BaseDecorator

        @Deco2('opt', opt='opt')
        @Deco1
        def func(*args, **kwargs):
            return args, kwargs

        self.assertEqual(func.decorator_options, (('opt',), {'opt': 'opt'}))
        self.assertEqual(func('arg', kw='kwarg'), (('arg',), {'kw': 'kwarg'}))

        # equal to
        def func(*args, **kwargs):
            return args, kwargs

        func = Deco2(Deco1(func), 'opt', opt='opt')

        self.assertEqual(func.decorator_options, (('opt',), {'opt': 'opt'}))
        self.assertEqual(func('arg', kw='kwarg'), (('arg',), {'kw': 'kwarg'}))

    # 5 - Wrapper without options
    def test_wrapper_without_oprions(self):
        Deco = BaseDecorator

        def func(*args, **kwargs):
            return args, kwargs

        wrapper = Deco(func)

        self.assertFalse(hasattr(func, 'decorator_options'))
        self.assertEqual(wrapper.decorator_options, ((), {}))
        self.assertEqual(func('arg', kw='kwarg'), (('arg',), {'kw': 'kwarg'}))
        self.assertEqual(wrapper('arg', kw='kwarg'), (('arg',), {'kw': 'kwarg'}))

    # 6 - Wrapper with options
    def test_wrapper_with_options(self):
        Deco = BaseDecorator

        def func(*args, **kwargs):
            return args, kwargs

        wrapper = Deco(func, 'opt', opt='opt')

        self.assertFalse(hasattr(func, 'decorator_options'))
        self.assertEqual(wrapper.decorator_options, (('opt',), {'opt': 'opt'}))
        self.assertEqual(func('arg', kw='kwarg'), (('arg',), {'kw': 'kwarg'}))
        self.assertEqual(wrapper('arg', kw='kwarg'), (('arg',), {'kw': 'kwarg'}))

    # 7 - Wrap (without options) a decorated function (without options)
    def test_wrap_without_options_a_decorated_function_without_options(self):
        Deco1 = Deco2 = BaseDecorator
        @Deco1
        def func(*args, **kwargs):
            return args, kwargs

        wrapper = Deco2(func)

        self.assertEqual(func.decorator_options, ((), {}))
        self.assertEqual(wrapper.decorator_options, ((), {}))
        self.assertEqual(func('arg', kw='kwarg'), (('arg',), {'kw': 'kwarg'}))
        self.assertEqual(wrapper('arg', kw='kwarg'), (('arg',), {'kw': 'kwarg'}))

        # equal to
        def func(*args, **kwargs):
            return args, kwargs

        func = Deco1(func)
        wrapper = Deco2(func)

        self.assertEqual(func.decorator_options, ((), {}))
        self.assertEqual(wrapper.decorator_options, ((), {}))
        self.assertEqual(func('arg', kw='kwarg'), (('arg',), {'kw': 'kwarg'}))
        self.assertEqual(wrapper('arg', kw='kwarg'), (('arg',), {'kw': 'kwarg'}))

    # 8 - Wrap (with options) a decorated function (without options)
    def test_wrap_with_options_a_decorated_function_without_options(self):
        Deco1 = Deco2 = BaseDecorator

        @Deco1
        def func(*args, **kwargs):
            return args, kwargs

        wrapper = Deco2(func, 'opt', opt='opt')

        self.assertEqual(func.decorator_options, ((), {}))
        self.assertEqual(wrapper.decorator_options, (('opt',), {'opt': 'opt'}))
        self.assertEqual(func('arg', kw='kwarg'), (('arg',), {'kw': 'kwarg'}))
        self.assertEqual(wrapper('arg', kw='kwarg'), (('arg',), {'kw': 'kwarg'}))

        # equal to
        def func(*args, **kwargs):
            return args, kwargs

        func = Deco1(func)
        wrapper = Deco2(func, 'opt', opt='opt')

        self.assertEqual(func.decorator_options, ((), {}))
        self.assertEqual(wrapper.decorator_options, (('opt',), {'opt': 'opt'}))
        self.assertEqual(func('arg', kw='kwarg'), (('arg',), {'kw': 'kwarg'}))
        self.assertEqual(wrapper('arg', kw='kwarg'), (('arg',), {'kw': 'kwarg'}))

    # 9 - Wrap (without options) a decorated function (with options)
    def test_wrap_without_options_a_decorated_function_with_options(self):
        Deco1 = Deco2 = BaseDecorator

        @Deco1('opt', opt='opt')
        def func(*args, **kwargs):
            return args, kwargs

        wrapper = Deco2(func)

        self.assertEqual(func.decorator_options, (('opt',), {'opt': 'opt'}))
        self.assertEqual(wrapper.decorator_options, ((), {}))
        self.assertEqual(func('arg', kw='kwarg'), (('arg',), {'kw': 'kwarg'}))
        self.assertEqual(wrapper('arg', kw='kwarg'), (('arg',), {'kw': 'kwarg'}))

        # equal to
        def func(*args, **kwargs):
            return args, kwargs

        func = Deco1(func, 'opt', opt='opt')
        wrapper = Deco2(func)

        self.assertEqual(func.decorator_options, (('opt',), {'opt': 'opt'}))
        self.assertEqual(wrapper.decorator_options, ((), {}))
        self.assertEqual(func('arg', kw='kwarg'), (('arg',), {'kw': 'kwarg'}))
        self.assertEqual(wrapper('arg', kw='kwarg'), (('arg',), {'kw': 'kwarg'}))

    # 10 - Wrap (with options) a decorated function (with options)
    def test_wrap_with_options_a_decorated_function_with_options(self):
        Deco1 = Deco2 = BaseDecorator

        @Deco1('opt1', opt='opt1')
        def func(*args, **kwargs):
            return args, kwargs

        wrapper = Deco2(func, 'opt2', opt='opt2')

        self.assertEqual(func.decorator_options, (('opt1',), {'opt': 'opt1'}))
        self.assertEqual(wrapper.decorator_options, (('opt2',), {'opt': 'opt2'}))
        self.assertEqual(func('arg', kw='kwarg'), (('arg',), {'kw': 'kwarg'}))
        self.assertEqual(wrapper('arg', kw='kwarg'), (('arg',), {'kw': 'kwarg'}))

        # equal to
        def func(*args, **kwargs):
            return args, kwargs

        func = Deco1(func, 'opt1', opt='opt1')
        wrapper = Deco2(func, 'opt2', opt='opt2')

        self.assertEqual(func.decorator_options, (('opt1',), {'opt': 'opt1'}))
        self.assertEqual(wrapper.decorator_options, (('opt2',), {'opt': 'opt2'}))
        self.assertEqual(func('arg', kw='kwarg'), (('arg',), {'kw': 'kwarg'}))
        self.assertEqual(wrapper('arg', kw='kwarg'), (('arg',), {'kw': 'kwarg'}))


if __name__ == '__main__':
    unittest.main()