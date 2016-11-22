
.. Type hinting hands-on slides file, created by
   hieroglyph-quickstart on Sat Nov 19 20:06:37 2016.

Optional static typing
======================

*by Ilya Etingof, Red Hat Product Security*

Agenda
======

* Variables, types and their interplay
* Why checking types?
* Type checkers
* Adoption of static typing

Variable
========

* Named storage
* Name helps addressing stored data/code
* Name introduces scoping and inheritance

Variable types
==============

* Type helps structuring and interpreting the data.
* But what is Type?

Concepts of Type
================

Ways to define type:

* Based on all possible values
* Based on all operations defined on values of given Type

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

Is Strong better than Weak?
===========================

Different strengths and weaknesses:

========= ================================ =================
    -           Strong Typing                Weak Typing
========= ================================ =================
  Good      More deterministic behavior      Convenience
========= ================================ =================

Is Dynamic better than Static
=============================

Different strengths and weaknesses:

====== ========================== ==============
   -              Static            Dynamic
====== ========================== ==============
  Good   Better error checking      Convenience
====== ========================== ==============

What about Python?
==================

* On stronger side of the spectrum
* Highly dynamic by design

Could we make it static when we need to?

Static                        Dynamic
^-----------------------------^
-                ^
-                Gradual

What is type checking?
======================

Statically typing variables implies type checking.

Two steps:

1. What type given variable belongs to?
2. Is it safe to execute given operation on given type?

How to compare types?
=====================

`T2` is a subtype of `T1` if:

* Any possible value of `T2` also belongs to values of `T1` and
* Any operation allowed on `T1` also works on `T2`

When `T2` is a subtype of `T1`:

* The set of `T2` values may only be smaller
* The set of operations on `T2` may only be larger
* Every type is also a subtype of itself

Computing types relationships
=============================

Approaches:

* By inheritance relationship (AKA nominal)
* By interface (AKA structural)

Testing inheritance
===================

Python types are arranged in a tree with `object` at its root:

.. code-block:: python

    >>> issubclass(bool, int)
    True
    >>> issubclass(float, int)
    False
    >>> issubclass(int, object)
    True

Testing interfaces
==================

Unrelated types may exibit identical behaviour (AKA duck typing):

.. code-block:: python

    >>> issubclass(UserDict, dict)
    False
    >>> hasattr(UserDict, '__getitem__') and hasattr(dict, '__getitem__')
    True
    >>> hasattr(UserDict, 'keys') and hasattr(dict, 'keys')
    True

Structural typing is hard to implement!

Is it worth the trouble?
========================

Dynamic typing is error-prone:

.. code-block:: python

    def gcd(a, b):
        while a:
            a, b = b%a, a
        return b

    >>> gcd(4, 6)
    2
    >>> gcd('a', 'b')
    TypeError: not all arguments converted during string formatting

Static typing in Python
=======================

* Long running research dating back to 2004
* Many implementations: PyContracts, typechecker, mypy etc.
* Highly controversial topic!

PyContracts
===========

* Runtime
* Ensures proper function args and return types
* Supports arithmetic constraints, predicates
* Can be disabled for production

Validates types by inheritance:

.. code-block:: python

    @contract
    def my_function(a : 'int,>0', b : 'list[N],N>0') -> 'list[N]':
         # Requires b to be a nonempty list, and the return
         # value to have the same length.
         ...

.. nextslide::

Enforces interface contract:

.. code-block:: python

    class Base(with_metaclass(ContractsMeta, object)):
        @abstractmethod
        @contract
        def sample(self, probability: 'float,>=0,<=1'):
            ...

    class Derived(Base):
        # The contract above is automatically enforced,
        # without this class having to know about PyContracts!
        def sample(self, probability):
            ....

Mypy
====

* Runs at linting time
* Ensures proper types of function args, return and free variables
* Infers variables types from first assignment
* Validates types only by inheritance (at present)
* Influences type hints

Type hints
==========

Common framework for all type checkers. In stdlib since Python 3.5.

Based on two otherwise independent features:

* Function and variable annotations
* Type hints

Annotations
===========

* Python expressions attaching arbitrary (!) objects to names
* Can annotate function parameters, return values, variables
* 100% optional, no predefined semantics
* Supported in Py3 since 2006

.. nextslide::

* Can annotate function args, return, free-standing variables
* With weird syntax

.. code-block:: python

    def gcd(a: 'arg1', b: 'arg2') -> 'out':
        while a:
            a, b = b%a, a
        return b

    >>> gcd.__annotations__
    {'a': 'arg1', 'b': 'arg2', 'return': 'out'}

Type annotations
================

This is where ends meet: annotating functions and variables
with built-in types or user classes:

.. code-block:: python

    def gcd(a: int, b: int) -> int:
        while a:
            a, b = b%a, a
        return b

Type hints classes
==================

* Isolate the complexities of types relationship computation
* Implement inheritance and partially (!) interface validation
* Designed for type checker use only
* Do not impose runtime performance penalty
* `import typing`

.. nextslide::

Largely based on ABCs:

.. code-block:: python

    from typing import Sequence, Mapping

    def select_values(d: Mapping, s: str) -> Sequence:
        return [v for k, v in d.items() if s == k]

    select_values({1: 'x'}, 'x')

.. nextslide::

Type hints may be insanely detailed:

.. code-block:: python

    from typing import List, Dict

    def select_values(d: Dict[str, int], s: str) -> List[int]:
        return [v for k, v in d.items() if s == k]

    l: List[int]
    s: str

    l = select_values({'x': 1}, 'x')

.. nextslide::

Large collection of type hints in `typing` module:

* `Sequence`: type supporting sequence protocol
* `Iterable`: type supporting iterator protocol
* `Callable`: function type
* `Generator`: generator type
* `Awaitable`: asyncio coroutine return
* Generic variables and classes
* ...and many more

Obfuscating?
============

* Stub files (.pyi) for annotations to keep code clean
* Also works for C extensions and third-party libs
* The `typeshed` repo (https://github.com/python/typeshed) maintains
  stubs for stdlib and some other packages

.. code-block:: python

    def select_values(d: Dict[str, int], s: str) -> List[int]:
        ...

Bright sides
============

* Improves linting accuracy
* Lets you omit some runtime checks
* Serves as documentation
* Powers IDEs automation
* Comforts your refactoring

Hints static analysers
======================

Run `mypy` over your code:

* Annotated with type hints
* ...built-in types
* ...user classes
* ...or not annotated at all

.. nextslide::

.. code-block:: python

    from typing import Tuple

    def make_dict(*items: Tuple[str, int]):
        return dict(items)

    make_dict((1, 'x'))

Running `mypy` over this code yields:

.. code-block:: bash

    $ mypy example.py
    Argument 1 to "make_dict" has incompatible type
    "Tuple[int, str]"; expected "Tuple[str, int]"

Improves code readabilty
========================

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

Makes IDEs better
=================

PyCharm 2016 supports type hinting in function
annotations and comments:

.. figure:: pycharm.png

Critique
========

* Undermines duck typing
* Does not catch all typing bugs
* Introduces ugly syntax
* Litters code with typs definitions
* Stubs maintenance is a pain

Is it worth it?
===============

* The larger your project
* ...the larger your team
* ...the heavier you refactor your code
* the more you need it!

Can I use it?
=============

If you are at Python:

* 3.6+: just install `mypy-lang`
* 3.5+: like 3.6, but variable annotations go to comments
* 3.1..3.4: like 3.5 plus need to `pip install typing`
* 2.7: like 3.4 plus all annotations go to comments
* 2.6: I admire your seniority, but... ;-)

Where do I start?
=================

* Make `mypy` running successfully over unannotated code
  (--check-untyped-defs)
* Invoke `mypy` from git commit hook or your favorite CI
* Gradually annotate your codebase starting from core
  parts (try Google's `PyType` for generating `.pyi` stubs)
* Finally, disallow unannotated commits (--disallow-untyped-defs)

Questions?
==========

.. figure:: snake-clipart-image-4.png
   :scale: 70 %
   :align: center
