
.. Type hinting hands-on slides file, created by
   hieroglyph-quickstart on Sat Oct 22 15:06:37 2016.


Type hinting hands-on
=====================

*by Ilya Etingof*

Agenda
======

* Variables, types and their interplay
* Why type checking?
* Function and variable annotations
* Type hints
* Practicing Python gradual typing

What is a variable?
===================

BTW, that's an interview question! ;-)

Variable is:
============

* Storage + name
* Name gets hold of stored data/code
* Name introduces scoping and inheritance
* Type defines a way to structure and interpret data

Concepts of Type:
=================

Many ways to define what Type is:

* ...based on all possible values
* ...based on all operations that could be performed on variables of given Type (AKA duck typing)

May get incredibly complicated.

Demystifying the buzzwords
==========================

* Static vs Dynamic: name<->storage type [re]binding
* Strong vs Weak: degree of automatic value adaptation

.. code-block:: python

    x = 1           # `x` name points to integer object
    x = '1'         # now repoint `x` to a string object -- that's dynamic

    x = '1' + 1     # fails on `+` operation -- sign of strong typing
    x = '1' + b'1'  # but this succeeds -- sign of weak typing

Types compatibility
===================

When it is safe to carry out an operation on a variable of given type?

* Variables of the same type are always safe to deal with
* Variables of different types? It depends...

.. code-block:: python

    1 + 1     # OK
    1.0 + 1   # OK

    1 << 8    # OK
    1.0 << 8  # FAIL

Computing types compatibility
=============================

Approaches to subtype relationships computation:

* By relationships (inheritance)
* By interface (duck typing)

Gradual typing in Python
========================

Implementation based on two otherwise independent features:

* Function and variable annotations (introduced in 2006)
* Type hints (part of Python 3.5 since 2015)

Annotations
===========

* Python expressions attaching arbitrary (!) objects to names
* Can annotate function parameters, return values, variables
* 100% optional, no predefined semantics
* Python 3: part of the language
* Python 2: mini-language embedded into comments

Function and variable annotations
=================================

* Function parameters: optional expression following parameter name
* Function return: optional expression following '->' token
* Global, local, class variable: optional expression following name

.. code-block:: python

    # foo(identifier [: expression] [= expression]) [-> expression]:
    def foo(bar: 'bar goes in') -> 'bar goes out':
        return bar

    # identifier [: expression] [= expression]
    y: 'ordinate' = 1

Annotation examples
===================

Documenting with annotations:

.. literalinclude:: /../code/01-annotations/00-documentation.py
   :language: python

*File: code/01-annotations/00-documentation.py*

.. nextslide::

You can annotate with pretty much any object:

.. literalinclude:: /../code/01-annotations/01-computed.py
   :language: python

*File: code/01-annotations/01-computed.py*

.. nextslide::

Annotations are stored in `__annotations__` as a dict:

.. literalinclude:: /../code/01-annotations/02-introspection.py
   :language: python

*File: code/01-annotations/02-introspection.py*

Type hints classes
==================

* Part of Python 3.5 (the `typing` module)
* Designed for type checker use only (a separate program)
* Should never be instantiated by user code
* Do not impose performance penalties or compatibility issues

Type annotations
================

This is where ends meet: annotating function and variables with
either regular Python types...

.. code-block:: python

    def factorial(n: int) -> int:
        if n == 0:
            return 1
        else:
            return n * factorial(n-1)

.. nextslide::

...or type hints classes (to capture the semantics of more complex types):

.. code-block:: python

    from typing import List

    def list_multiplication(l: List[int], n: int) -> List[int]:
        return [x*n for x in l]

    n = list_multiplication([1, 2, 3], 10)

Running type checker
====================

* Performed by a stand-alone program
* Not in run time
* Infers types or consumes type annotations
* Type consistency evaluation based on class hierarchy

.. code-block:: bash

    $ mypy --python-version 3.6 --fast-parser example.py

.. nextslide::

Can analyze unannotated code...:

.. literalinclude:: /../code/02-type-hints/00-inferring-types.py
   :language: python

*File: code/02-type-hints/00-inferring-types.py*

.. nextslide::

...or code annotated with built-in types...:

.. literalinclude:: /../code/02-type-hints/01-builtin-types.py
   :language: python

*File: code/02-type-hints/01-builtin-types.py*

.. nextslide::

...or code annotated with user classes...:

.. literalinclude:: /../code/02-type-hints/02-user-types.py
   :language: python

*File: code/02-type-hints/02-user-types.py*

Typing based on ABC
===================

* Class hierarchy based type checking is too rigid
* Can use Abstract Base Classes that capture interfaces, not hierarchy
* In `typing`, ABCs extended to support type hinting

Fundamentals: Any
=================

* `Any` is a subclass of `object`
* `object` is a subclass of `Any`

.. code-block:: python

    from typing import Any

    issubclass(Any, object)  # yields True
    issubclass(object, Any)  # yields True

    issubclass(int, object)  # yields True
    issubclass(object, int)  # yields False

.. nextslide::

Non-hinted variables implicitly belong to `Any` type

.. code-block:: python

    from typing import Any

    def func(x: int, y: Any):
        return x + y

    func(1, 1)       # mypy: OK
    func(1, 'text')  # mypy: OK
    func('text', 1)  # mypy: Argument 1 to "func" has incompatible
                     #       type "str"; expected "int

Fundamentals: Union
===================

Types that are subtype of at least one of types (int, str) are subtypes of `Union`

.. code-block:: python

    from typing import Union

    def sum_of_numbers(*numbers: Union[int, float]) -> float:
        return sum(numbers)

Fundamentals: Tuple
===================

Two syntaxes:

* Fixed set of types e.g. (1, 1.2)
* Variadic set of homogeneous types e.g. (1, 2, 3)

.. code-block:: python

    from typing import Tuple

    Tuple[int, str]
    Tuple[int, ...]

.. nextslide::

.. literalinclude:: /../code/02-type-hints/06-tuple-of-different-types.py
   :language: python
   :end-before: # Continuing

*File: code/02-type-hints/06-tuple-of-different-types.py*

.. nextslide::

.. literalinclude:: /../code/02-type-hints/06-tuple-of-different-types.py
   :language: python
   :start-after: # Continuing

*File: code/02-type-hints/06-tuple-of-different-types.py*

Fundamentals: Callable
======================

A function with positional argument types and return type:

.. literalinclude:: /../code/02-type-hints/07-callback-types.py
   :language: python

*File: code/02-type-hints/07-callback-types.py*

Typing containers
=================

.. literalinclude:: /../code/02-type-hints/04-container-types.py
   :language: python

*File: code/02-type-hints/04-container-types.py*

.. nextslide::

.. literalinclude:: /../code/02-type-hints/05-container-types-with-elements.py
   :language: python

*File: code/02-type-hints/05-sequence-types-with-elements.py*

Typing everything known
=======================

Other type hints from `typing`:

* `Iterable`: general iterable
* `Callable`: variable pointing to a callback function
* `Generator`: variable holding generator objects
* `Awaitable`: asyncio coroutine return

Generic functions
=================

* Generic type: takes generic or concrete type and produces generic or concrete type
* Generic function: takes generic types as `type variables`
* Type checker substitutes type variable with concrete type

.. nextslide::

Unconstrained type variable:

.. literalinclude:: /../code/02-type-hints/09-type-variables.py
   :language: python
   :end-before: # Continuing

*File: code/02-type-hints/09-type-variables.py*

Defining generic types
======================

* By subclassing `Generic` class
* New generic types are parameterizable with generic or concrete types.

.. nextslide::

.. literalinclude:: /../code/02-type-hints/10-generic-classes.py
   :language: python
   :end-before: # Continuing

*File: code/02-type-hints/10-generic-classes.py*

.. nextslide::

Concrete type inferred from annotation:

.. literalinclude:: /../code/02-type-hints/10-generic-classes.py
   :language: python
   :start-after: # Continuing

*File: code/02-type-hints/10-generic-classes.py*

Benefits of type checking
=========================

* Catches bugs early! Including highly latent ones.
* Improves code readability
* Makes refactoring less stressful
* Facilitates documentation builders
* Helps IDEs offering meaningful warnings and hints

Consider: code readabilty
=========================

With legacy docstrings:

.. code-block:: python

    def ahoj(name='nobody'):
        """Greet a person

        :param name: string value
        :rtype: string value
        """
        return 'Ahoj {}!'.format(name)

with Type Hints:

.. code-block:: python

    def ahoj(name: str = 'nobody') -> str:
        """Greet a person"""
        return 'Ahoj {}!'.format(name)

Consider: IDE
=============

PyCharm 2016 supports type hinting in function annotations and comments:

.. figure:: pycharm.png

What type hints IS NOT
======================

* Does not turn Python statically typed
* No changes to runtime
* No code generation
* No performance overhead

Type hints in aged Python
=========================

* Variable annotations in comments up to 3.6
* Function and variable annotations in comments up to 3.0
* Up to 3.5, `typing` module is shipped as a PyPI package

Practice time!
==============

Game plan:

0. Log into the lab
1. Fix type consistency error
2. Fix bugs as reported by type checker
3. Complete type annotations
4. Type annotate fully dynamic code

Set up the environment
======================

* Get lab access credentials
* Choose your student ID
* Log into the lab machine
* Do the assignments

.. code-block:: bash

    $ git clone https://github.com/etingof/talks.git
    $ cd talks/pycon-type-hinting
    $ ssh -i student.pem studentXX@209.132.178.69
    Enter passphrase for key 'student.pem':
    [studentXX@pycon ~]$ cd code

Assignment 1
============

Fix type consistency error:

.. code-block:: bash

    $ mypy 01-fib.py
    Incompatible types in assignment (expression has type List[int],
    variable has type Iterator[int])
    $

Assignment 2
============

There might be a problem in container type declaration. Could
you fix it?

.. code-block:: bash

    $ mypy 02-linked-list.py

Assignment 3
============

Fix bugs as found by static type checker:

.. code-block:: bash

    $ mypy 02-linked-list.py

Annotating your own code
========================

* Setup `mypy`
* Make it running successfully over unannotated code (--check-untyped-defs)
* Invoke `mypy` from git commit hook or your favorite CI
* Gradually annotate your codebase starting from core parts
* Disallow unannotated commits (--disallow-untyped-defs)

Summary
=======

* Python remains dynamically typed language
* Static typing can harden your code
* ...and makes it more readable
* ...and easier refactorable

Further reading
===============

* `Literature Overview for Type Hints <https://www.python.org/dev/peps/pep-0482/>`_
* `The theory of type hints <https://www.python.org/dev/peps/pep-0483/>`_
* `Type hints <https://www.python.org/dev/peps/pep-0484/>`_
* `Function Annotations <https://www.python.org/dev/peps/pep-3107/>`_
* `Variable annotations <https://www.python.org/dev/peps/pep-0526/>`_
* `MyPy Syntax Cheat Sheet <http://mypy.readthedocs.io/en/latest/cheat_sheet.html>`_
