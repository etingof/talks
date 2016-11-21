
.. Type hinting hands-on slides file, created by
   hieroglyph-quickstart on Sat Nov 19 20:06:37 2016.

Optional static typing
======================

*by Ilya Etingof, Red Hat Product Security*

Agenda
======

* Variables, types and their interplay
* Why type checking?
* Function and variable annotations
* Type hints
* Static typing showcases
* Adoption of static typing

Variable
========

* Named storage
* Name helps addressing stored data/code
* Name introduces scoping and inheritance

Variable types
==============

Type helps structuring and interpreting the data

How many types we need?
=======================

* What is the difference between types?
* How types relate to each other?
* What's the definition of type?

Concepts of Type
================

Ways to define type:

* Based on all possible values
* Based on all operations that could be performed on values of given Type

Static vs Dynamic
=================

Reflects the strength of name-to-type binding:

.. code-block:: python

    # `x` name points to integer object
    x = 1

    # now point `x` to a string object -- that's dynamic
    x = '1'

Strong vs Weak
==============

Willingness to coerce to unrelated type when no one is looking:

.. code-block:: python

    # fails on `+` operation -- sign of stronger typing
    x = '1' + 1

    # but this succeeds -- sign of weaker typing
    y = 1 + 1.0

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

.. nextslide::

You can annotate with pretty much any object:

.. literalinclude:: /../code/01-annotations/01-computed.py
   :language: python

.. nextslide::

Annotations are stored in `__annotations__` as a dict:

.. literalinclude:: /../code/01-annotations/02-introspection.py
   :language: python

Type annotations
================

This is where ends meet: annotating function and variables with
either regular Python types!

Annotating with built-in types (or user classes):

.. code-block:: python

    def factorial(n: int) -> int:
        if n == 0:
            return 1
        else:
            return n * factorial(n-1)

Type checker program
====================

* Stand-alone tool
* Infers types of non-annotated variables
* Consumes type annotations
* Figures out types relationships

Many competing implementations anticipated, `mypy` is the king:

.. code-block:: bash

    $ mypy example.py
    $

Kinds of code
=============

* Non-annotated code
* mypy infers type from first assignment
* Relationship computed based on type hierarchy

.. literalinclude:: /../code/02-type-hints/00-inferring-types.py
   :language: python

.. nextslide::

* Code annotated with built-in types
* Relationship computed based on type hierarchy

.. literalinclude:: /../code/02-type-hints/01-builtin-types.py
   :language: python

.. nextslide::

* Code annotated with user classes
* Relationship computed based on type hierarchy

.. literalinclude:: /../code/02-type-hints/02-user-types.py
   :language: python

.. nextslide::

* Code annotated with type hints
* Relationship computed based on type hierarchy and interfaces

.. literalinclude:: /../code/02-type-hints/03-iterable-types.py
   :language: python

Is it tough?
============

Tolerate a bit more of a theory - we are crawling to the show time!

.. figure:: snake-clipart-image-4.png
   :scale: 70 %
   :align: center

Type hints classes
==================

* Based on Abstract Base Classes (ABC)
* Compute types relationship based on both inheritance and interfaces/protocols
* Designed for type checker use only
* Should never be instantiated by user code
* Do not impose performance penalties or compatibility issues

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

First syntax: to model structures

* Fixed set of types
* `Tuple[int, str]` -> `(1, 'ahoj')`

.. code-block:: python

    from typing import Tuple

    Tuple[int, str]

.. nextslide::

First syntax: to model structures

.. literalinclude:: /../code/02-type-hints/06-tuple-of-different-types.py
   :language: python
   :end-before: # Continuing

.. nextslide::

Second syntax: to model arrays

* Variadic set of homogeneous types
* `Tuple[int, ...]` -> `(1, 2, 3)`

.. code-block:: python

    from typing import Tuple

    Tuple[int, ...]

.. nextslide::

Second syntax: to model arrays

.. literalinclude:: /../code/02-type-hints/06-tuple-of-different-types.py
   :language: python
   :start-after: # Continuing

Type hints: containers
======================

Use case: to type dictionaries and lists

.. literalinclude:: /../code/02-type-hints/05-container-types-with-elements.py
   :language: python

Other type hints
================

Many specialized type hints in `typing` module:

* `Sequence`: type supporting sequence protocol
* `Iterable`: type supporting iterator protocol
* `Callable`: function type
* `Generator`: generator type
* `Awaitable`: asyncio coroutine return
* ... and other predefined in `typing.py`

Practice time
=============

Challenge: annotate function to catch mistyped parameter

.. code-block:: python
   :linenos:
   :emphasize-lines: 5

    def count_letters(sentence: str, letter) -> int:
        return sentence.count(letter)

    cnt = 0
    cnt += count_letters('Beautiful is better than ugly.', 1)

.. nextslide::

Solution:

.. code-block:: python
   :linenos:
   :emphasize-lines: 1,5

    def count_letters(sentence: str, letter: str) -> int:
        return sentence.count(letter)

    cnt = 0
    cnt += count_letters('Beautiful is better than ugly.', 1)

.. nextslide::

Something fishy is going on here... Can `mypy` catch that?

.. code-block:: python
   :linenos:
   :emphasize-lines: 13

    class Employee(object):
        def work(self): print('Employee is working...')

    class Manager(Employee):
        def fire(self): print('Manager fires someone!')

    def work(x): x.work()
    def fire(x): x.fire()

    e = Employee(); m = Manager()

    work(m); work(e)
    fire(m); fire(e)

.. nextslide::

Annotation ensures firing power belongs to `Manager` objects:

.. code-block:: python
   :linenos:
   :emphasize-lines: 7, 8, 13

    class Employee(object):
        def work(self): print('Employee is working...')

    class Manager(Employee):
        def fire(self): print('Manager fires someone!')

    def work(x: Employee): x.work()
    def fire(x: Manager): x.fire()

    e = Employee(); m = Manager()

    work(m); work(e)
    fire(m); fire(e)

.. nextslide::

Catch mistyped dicts

.. nextslide::

Catch mistyped duck-typed objects

Benefits of static typing
=========================

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

Can I use static typing?
========================

If you are at Python:

* 3.6+: just install `mypy-lang`
* 3.5+: like 3.6, but variable annotations go to comments
* 3.1..3.4: like 3.5 plus need to `pip install typing`
* 2.7: like 3.4 plus all annotations go to comments
* 2.6: I admire your seniority, oh... ;-)

Should I use gradual typing?
============================


How to annotate existing code?
==============================




Hey, what about the batteries?
==============================

* Optional stub files (.pyi) keep the signatures
* The `typeshed` repo (https://github.com/python/typeshed) maintains stubs
* Python lib and some third-party libs already covered

Practice time
=============

The plot:

* You see code snippet with a bug highlighted
* Figure out what type hint would help catching the bug
* You see the solution


Tough subject ahead
===================

* So far we've touched basic typing features
* To solve upcoming cases we need to look into Generics

Generic functions
=================

* Generic function: takes generic types as `type variables`
* Type checker substitutes type variable with concrete type
* Way to statically type related function arguments and return value

.. nextslide::

.. literalinclude:: /../code/02-type-hints/09-type-variables.py
   :language: python
   :end-before: # Continuing

Defining generic types
======================

* By subclassing `Generic` class
* New generic types are parameterizable with generic or concrete types.
* Way to statically type related attributes and method parameters

.. nextslide::

.. literalinclude:: /../code/02-type-hints/10-generic-classes.py
   :language: python
   :end-before: # Continuing

.. nextslide::

Concrete type inferred from annotation:

.. literalinclude:: /../code/02-type-hints/10-generic-classes.py
   :language: python
   :start-after: # Continuing

Practice time
=============

The Evil Spirit has planted itself into Programmer's soul and he utterly
forgot to keep function input/output compatible. Can you save Programmer
from failing miserably? (hint: he always runs `mypy` prior to commit)

.. code-block:: python
   :linenos:
   :emphasize-lines: 8, 9

    T = typing.TypeVar('T')

    def sum_up_anything_similar(a: T, b: T) -> T:
        return sum([a, b])

    sum_up_anything_similar('x', 'y') + 'z'
    sum_up_anything_similar(1, 2) + 3
    sum_up_anything_similar('x', 'y') + 3
    sum_up_anything_similar(1, 2) + 'z'



Summary
=======

* Python remains dynamically typed language
* Type hints do not influence your program
* Static typing can harden your code
* ...and makes it more readable
* ...and easier refactorable




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
