abd - Abstract Base Decorator
---

abd provides an `AbstractBaseDecorator` class which you can inherit from to create flexible decorators.

## Example
```Python3
>>> from abd import ABD
>>> class Decorator(ABD):
...     def invoke(self, *args, **kwargs):
...         """Must write an invoke function
...         invoke is called when the decorated function is called
...         """
...         # catch, edit and pass on the (keyword) arguments
...         #  that are given the the decorated function
...         print('invoke is called')
...         result = self.decorated_object(*args, **kwargs)
...         # function has been called and result is available
...         #   possible to edit the result here
...         return result
... 
>>> @Decorator
... def func(argument):
...     # some function logic ...
...     return argument
... 
>>> func('some text')
invoke is called
'some text'
>>> 
```

## PyPI
[pip install abd](https://pypi.org/project/abd/ "PyPI abd page")
