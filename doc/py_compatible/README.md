Versions of [abd](https://pypi.org/project/abd/ "🐍 PyPI") compatible with previous versions of Python.
---

The code in this directory is not supported and not updated.  
If you use any of these Python versions, you should have to consider updating Python.

### :link: [py22_abd.py](./py22_abd.py "🌟 Python 2.2.0")
No `@decorator` syntax, defeats the purpose of abd. wrapping functions is still a posibility.  
[property](https://docs.python.org/3/library/functions.html#property "Built-in Functions") functions are available in this version.  


### :link: [py25_abd.py](./py25_abd.py "⭐ Python 2.5.0")
First version with the [functool](https://docs.python.org/3/library/functools.html "functools — Higher-order functions and operations on callable objects") module. 


### :link: [py30_abd.py](./py30_abd.py "💫 Python 3.0.0")
[callable](https://docs.python.org/3/library/functions.html#callable "Built-in Functions") was removed from Python 3.0.0, `hasattr(object, '__call__')` had to be used.  


### :link: [py34_abd.py](./py34_abd.py "✨ Python 3.4.0")
No [typing](https://docs.python.org/3/library/typing.html "typing — Support for type hints") module and no modern typing syntax.  
[abc](https://docs.python.org/3/library/abc.html "abc — Abstract Base Classes") was introduced.  
