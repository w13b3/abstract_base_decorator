Example code using [abd](https://pypi.org/project/abd/ "Abstract Base Decorator")
---

# :warning: Warning :warning:️ <sup>:bug:</sup>
These examples may not work with any Python version.  
Usage is not recommended, looking at the examples voids warranty.  
The code in this directory is not tested and are *proof of concept* only.

---

### Example: [contract.py](./contract.py)  
A decorator that reads the annotations of the decorated function.  
and assures that the incoming and outgoing values are of the annotated type.

### Example: [logio.py](./logio.py)
A class decorator *logger*, to decorate classes.  
It wraps all the methods in the decorated class and logs the input, and what the method returns.

### Example: [redo.py](./redo.py)
A decorator that stores the input in memory.  
It adds functions to the decorated function to redo the previous actions.

### Example: [implicit_default.py](./implicit_default.py)
A decorator wich provides the decorated function implicit default parameters.
