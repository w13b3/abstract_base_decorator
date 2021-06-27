#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# test_abstract_base_decorator.py

import unittest
from unittest import mock

from abd import ABD, AbstractBaseDecorator


class AbstractBaseDecoratorTest(unittest.TestCase):

    def setUp(self) -> None:
        class DecoWithoutInvoke(ABD):
            pass

        class DecoWithInvoke(ABD):
            def invoke(self, *args: object, **kwargs: object):
                return self.decorated_object(*args, **kwargs)

        self.DecoWithoutInvoke = DecoWithoutInvoke
        self.DecoWithInvoke = DecoWithInvoke

    def test_ABD_is_AbstractBaseDecorator(self):
        self.assertIs(ABD, AbstractBaseDecorator)

    def test_class_attributes(self):
        self.assertTrue(hasattr(ABD, 'decorated_object'))
        self.assertTrue(hasattr(ABD, 'decorator_options'))
        self.assertTrue(hasattr(ABD, 'set_decorator_options'))
        self.assertTrue(hasattr(ABD, 'invoke'))

    def test_decorator_without_invoke_raises_TypeError(self):
        with self.assertRaises(TypeError):
            @self.DecoWithoutInvoke
            def func(*args, **kwargs):
                return args, kwargs

        with self.assertRaises(TypeError):
            def func(*args, **kwargs):
                return args, kwargs
            self.DecoWithoutInvoke(func)

    def test_decorator_with_invoke_no_error(self):
        @self.DecoWithInvoke
        def func(*args, **kwargs):
            return args, kwargs

        def func(*args, **kwargs):
            return args, kwargs
        self.DecoWithInvoke(func)

    def test_invoke(self):
        # create a class
        class InvokeCheck(ABD):
            def invoke(self, *args, **kwargs) -> bool:
                return self.decorated_object(*args, **kwargs)

        # create a spy
        with mock.patch.object(InvokeCheck, 'invoke') as invoke_spy:
            @InvokeCheck
            def func(given, expected=None):
                nonlocal self
                self.assertEqual(given, expected)

            # invoke should not yet has been called
            self.assertEqual(invoke_spy.call_count, 0)

            # call func which passes current call-count to invoke
            # func checks of the numbers are equal
            func(invoke_spy.call_count, 0)
            # invoke call-count has increased
            self.assertEqual(invoke_spy.call_count, 1)

            # call func directly without calling invoke
            # func checks of the numbers are equal
            func.decorated_object(invoke_spy.call_count, 1)
            self.assertEqual(invoke_spy.call_count, 1)

    def test_change_of_decorator_options(self):
        # create a class
        class OptionsCheck(ABD):
            def invoke(self, *args, **kwargs) -> bool:
                # pass the decorator options to the decorated function
                deco_args, deco_kwargs = self.decorator_options
                return self.decorated_object(*deco_args, **deco_kwargs)

        @OptionsCheck(True, option=True)
        def check_options(*opt_args, **opt_kwargs):
            nonlocal self
            # opt_args and opt_kwargs given to this function by invoke
            _bool, *_ = opt_args
            option = opt_kwargs.get('option')
            # check if the first argument and the keyword option are equal
            self.assertEqual(_bool, option)

        # call the decorated function which calls invoke.
        check_options()
        # change the decorator options
        check_options.set_decorator_options(False, option=False)
        # check after change
        check_options()
        # change the decorator options to something that fails the check
        check_options.set_decorator_options(True, option=False)

        with self.assertRaises(self.failureException):
            # check after change
            check_options()
