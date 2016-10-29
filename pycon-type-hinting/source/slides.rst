
.. Type hinting hands-on slides file, created by
   hieroglyph-quickstart on Sat Oct 22 15:06:37 2016.


Type hinting hands-on
=====================

*by Ilya Etingof, Red Hat Product Security*

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

Variable
========

* Named storage
* Name gets hold of stored data/code
* Name introduces scoping and inheritance

Define Type
===========

.. figure:: snake-clipart-image-1.png
   :scale: 150 %
   :align: center

.. nextslide::

Type helps structuring and interpreting the data

How many types we need?
=======================

How different they are? How types relate to each other? What is type?

.. figure:: dragon-clipart-image-1.png
   :scale: 50 %
   :align: center

Concepts of Type
================

Ways to define type:

* Based on all possible values
* Based on all operations that could be performed on values of given Type

Static vs Dynamic
=================

.. figure:: snake-clipart-image-2.png
   :scale: 150 %
   :align: center

.. nextslide::

Strength of name-to-type binding:

.. code-block:: python

    x = 1    # `x` name points to integer object
    x = '1'  # now point `x` to a string object -- that's dynamic

Strong vs Weak
==============

.. figure:: snake-clipart-image-3.png
   :scale: 150 %
   :align: center

.. nextslide::

Willingness to coerce to unrelated type when no one is looking:

.. code-block:: python

    x = '1' + 1  # fails on `+` operation -- sign of stronger typing
    y = 1 + 1.0  # but this succeeds -- sign of weaker typing

What about Python?
==================

* On stronger and dynamic sides of spectrum
* Can be static, more or less

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

...or type hints.

Type hints classes
==================

* Based on Abstract Base Classes (ABC)
* Captures semantics of types relationship based on interfaces/protocols
* Designed for type checker use only (a separate program)
* Should never be instantiated by user code
* Do not impose performance penalties or compatibility issues

.. nextslide::

.. code-block:: python

    from typing import List

    def list_multiplication(l: List[int], n: int) -> List[int]:
        return [x*n for x in l]

    n = list_multiplication([1, 2, 3], 10)

Running type checker
====================

* Performed by a stand-alone program
* At compile and/or run time
* Infers types or consumes type annotations
* Type consistency evaluation based on class hierarchy

.. code-block:: bash

    $ mypy example.py

.. code-block:: python

    @ensure_annotations
    def f(x: int, y: float) -> float:
        return x+y

    f(1, 2.3)  # ensure.EnsureError is raised

.. nextslide::

Can analyze non-annotated code...:

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

Wait, is it a lecture?
======================

Let's get used to the tools, practice is coming!

.. figure:: snake-clipart-image-4.png
   :scale: 80 %
   :align: center

Type hints: Any
===============

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

Type hints: Union
=================

Types that are subtype of at least one of types (int, str) are subtypes of `Union`

.. code-block:: python

    from typing import Union

    def sum_of_numbers(*numbers: Union[int, float]) -> float:
        return float(sum(numbers))

Type hints: Tuple
=================

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

Type hints: containers
======================

.. literalinclude:: /../code/02-type-hints/05-container-types-with-elements.py
   :language: python

*File: code/02-type-hints/05-sequence-types-with-elements.py*

Other type hints
================

Many specialized type hints in `typing` module:

* `Sequence`: type supporting sequence protocol
* `Iterable`: type supporting iterator protocol
* `Callable`: function type
* `Generator`: generator type
* `Awaitable`: asyncio coroutine return
* ... and other predefined in `typing.py`

Generic functions
=================

* Generic function: takes generic types as `type variables`
* Type checker substitutes type variable with concrete type
* Way to statically type related function arguments and return value

.. nextslide::

.. literalinclude:: /../code/02-type-hints/09-type-variables.py
   :language: python
   :end-before: # Continuing

*File: code/02-type-hints/09-type-variables.py*

Defining generic types
======================

* By subclassing `Generic` class
* New generic types are parameterizable with generic or concrete types.
* Way to statically type related attributes and method parameters

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

Benefits of gradual typing
==========================

* Facilitates static analysis
* Also serves as documentation
* Helps understanding the codebase
* Lets you refactor aggressively
* Powers IDEs nifty features (code completion etc)

Benefits: code readabilty
=========================

With legacy docstrings:

.. code-block:: python

    def ahoj(name='nobody'):
        """Greet a person

        :param name: string value
        :rtype: string value
        """
        return 'Ahoj {}!'.format(name)

with Type Hints (with `sphinx-autodoc-annotation`):

.. code-block:: python

    def ahoj(name: str = 'nobody') -> str:
        """Greet a person"""
        return 'Ahoj {}!'.format(name)

Benefits: IDE support
=====================

PyCharm 2016 supports type hinting in function annotations and comments:

.. figure:: pycharm.png

Hey, what about the batteries?
==============================

* Optional stub files (.pyi) keep the signatures
* The `typeshed` repo (https://github.com/python/typeshed) maintains stubs
* Python lib and some third-party libs already covered

Summary
=======

* Python remains dynamically typed language
* Type hints do not influence your program
* Static typing can harden your code
* ...and makes it more readable
* ...and easier refactorable

Practice time!
==============

* Get lab access credentials
* Choose your student ID (use your seat number 01..64)
* Log into the lab machine as studentXX
* Do as many assignments as you can

.. code-block:: bash

    $ wget -o student.pem https://goo.gl/jQp34P
    $ chmod 600 student.pem
    $ ssh -i student.pem studentXX@209.132.178.69
    Enter passphrase for key 'student.pem':
    [studentXX@pycon ~]$ cd practice

Assignment: fix bugs in code
============================

In this assignment you are requested to find and fix
wrong/misplaced function call parameters.

* Run `mypy` over scripts `*-fix-a-bug.py` one by one
* Analyze the problems type checker is reporting
* Fix the errors, re-run `mypy` and the scripts

Assignment: fix annotations
===========================

In this assignment you are requested to improve type annotations
so that type checker would be able to find and report an issue
before you hit it at run time.

Run each of the `*-fix-annotations.py` scripts

* Analyze what causes script to fail
* Improve type annotations
* Run `mypy` to make sure it catches the problem

Type hints cheetsheet
=====================

Type hints uses in hands-on assignments:

* Tuple[T, ...]
* Tuple[T1, T2]
* Dict[KT, VT]
* Callable[..., ReturnType]
* Generator[YieldType, SendType, ReturnType]
* T = TypeVar['T']
* Generic[T]

Further reading
===============

* `Literature Overview for Type Hints <https://www.python.org/dev/peps/pep-0482/>`_
* `The theory of type hints <https://www.python.org/dev/peps/pep-0483/>`_
* `Type hints <https://www.python.org/dev/peps/pep-0484/>`_
* `Gradual Typing for Functional Languages <http://scheme2006.cs.uchicago.edu/13-siek.pdf>`_
* `Function Annotations <https://www.python.org/dev/peps/pep-3107/>`_
* `Variable annotations <https://www.python.org/dev/peps/pep-0526/>`_
* `MyPy Syntax Cheat Sheet <http://mypy.readthedocs.io/en/latest/cheat_sheet.html>`_
* This talk's materials `https://github.com/etingof/talks/tree/master/pycon-type-hinting <https://github.com/etingof/talks/tree/master/pycon-type-hinting>`_
