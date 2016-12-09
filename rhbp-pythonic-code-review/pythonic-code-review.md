
Pythonic code review
====================

*Ilya Etingof, Red Hat Product Security*

Most of us, programmers, go through technical interviews every once
in a while. At other times many of us sit at the opposite side of the 
table running these interviews. Stakes are high, emotions run strong,
intellectual pressure builds up. I found that an unfortunate code review 
may turn into something similar to a harsh job interview.

While it is theoretically in the best interest of the whole team to 
end up with high quality code, variations in individual's technical 
background, cultural differences, preconceptions built up on previous 
experience, personality quirks, and even temper may get in the way of 
luring people into a fierce fight over relatively unimportant matters.

Consider an imaginary pull request. There we typically have two actors:
author and code reviewers. Sometimes authors tend to overestimate the
quality  of their code what provokes them to be overly defensive and 
even hostile to any argument. People reviewing the code may find themselves
being in a position of power to judge author's work. Once the actors
collide over a matter where they take orthogonal and sufficiently
strong sides, all is fair in love and war.

Another interesting phenomena I encountered while reviewing Python code
can probably be attributed to Python's low entry barrier for newcomers.
Programmers switching over from other languages bring along customs and 
idioms they are used to at their mother tongue. I could frequently 
tell former Java, Perl or Bash programmer from their Python code. As 
much as I admire other technologies and expertise, I believe it is 
most efficient and enjoyable to code in harmony with the language rather 
than stretching it beyond its intended design. 

In this blog post I'll focus on my personal experience in authoring
and reviewing Python code from both psychological and technical
perspectives. Keeping in mind my ultimate goal of striking a balance 
between code reviews being enjoyable and technically fruitful.

Why we review code
------------------

The most immediate purpose of a code review is to make code better by
focusing more eyeballs at it. But code review seems to be a lot more
than that!
 
It is also a way for the engineers to communicate, learn and even 
socialize over a meaningful and mutually interesting topic. In a team where 
both senior and junior engineers work together, a code review provides the 
opportunity for the junior engineers to observe masters at work and learn 
from them. 

Seniors, in turn, get a chance to couch fellow engineers, be challenged and
thus prove their authority (which is healthy). Everyone could see the
problem from different perspectives, that ultimately contributes to a
better outcome.

For mature Pythonistas coding with newbies, code review is a way to teach
them how we do things in Python up to the extent of brewing idiomatic Python
coders out of them.

For the greater good
--------------------

The best we can do on the psychological side is to, as an author, relinquish 
our emotional attachment to our code and, as a reviewer, consciously 
restrain ourselves from attacking other authors' ideas, focusing on 
mentoring them.

For a review to be a productive and relatively comforting experience, 
a reviewer should stay positive, thankful, honestly praise the author's
work and talent in a genuine matter. Suggested changes should be justified 
by solid technical grounds but never the reviewer's personal taste.

For authors it may help to keep reminding themselves how much time and
effort it might have taken for reviewers to work with author's 
code -- their feedback is precious! 

As idealistic as it sounds, my approach aims at downplaying my ego by
optimizing for a healthier team and an enjoyable job. I suspect that it might 
come at the cost of compromised quality of the code we collectively produce.
My hope here is that even if we do merge suboptimal code at times, we will 
eventually learn from that and refactor later. That's way cheaper compared 
to ending up with a stressed, despaired and demotivated team effectively 
stuck at its project.

When I'm an author
------------------

As an author, I'm not taking PRs lightly. My day's worth of code is 
likely to keep fellow reviewers busy for a good couple of hours.
I know that it's a hard and expensive endeavour. Proper code 
review may require my team mates to reverse engineer business logic 
behind a change, trace code execution, conduct thought experiments, 
search for edge cases. I do keep that in mind and feel grateful for
their time.

I try to keep my changes small. The larger the change is, the more effort 
it would take for reviewers to finish the review. That gives smaller, 
isolated changes better chances for a quality treatment, while huge 
and messy blobs of diffs risk turning a blind eye on my PR.

Well-debugged code accompanied with tests, properly documented changes 
complying with team policies -- those PR qualities are signs of respect
and care towards reviewers. I feel myself more confident once I run 
a quick self code review against my prospective PR prior to submitting it 
to fellow engineers.

When I'm a reviewer
-------------------

To me, the most important qualities of code is to be clean
and as Pythonic as circumstances permit.

Clean code tends to be well-structured where logically distinct parts
are isolated from each other via clearly visible boundaries. Ideally,
each part is specialized on solving a single problem. As Zen of Python
puts it: "If the implementation is easy to explain, it may be 
a good idea".

Signs of clear code include self-documented functions and variables 
describing problem entities, not implementation details.

Readability counts, indeed, though I would not sweat full PEP8
compliance up to the cost of nitpicking and bikesheding.

I praise the author's coding on the shoulders of giants -- abstracting
problem into canonical data structures/algorithms and working from
there. That gives me a warm feeling of author belonging to the same 
trade guild as myself and confidence that we both know what to expect 
from the code.

When I'm a Pythonista
---------------------

The definition of code being Pythonic tends to be somewhat vague and
subjective. It seems to be influenced by one's habits, taste, picked
up idioms and language evolution. I keep that in mind and restrain
myself from evangelizing my personal perception of what's Pythonic 
towards fellow Pythonistas.

Speaking from my experience in the fields, let me offer the reader a 
handful of code observations I encountered along with the suggestions
leveraging features that are native to Python so that people with
different backgrounds may be unaware of them.

Justified programming model
^^^^^^^^^^^^^^^^^^^^^^^^^^^

People coming from Java tend to turn everything into a class. That's
probably because Java heavily enforces the OOP paradigm. Python programmers
enjoy a freedom of picking a programming model that is best suited for 
the task.

Choice of object-based implementation looks reasonable to me when
there is a clear abstraction for the task being solved. Statefulness
and duck-typed objects are another strong reason for going the OOP way.

If author's priority is to keep related functions together, pushing
them to a class is an option to consider. Such class might never
need instantiation, though.

Free-standing functions are easy to grasp, concise and light. When a
function does not cause side-effects, it's also good for 
`functional <https://docs.python.org/3.6/howto/functional.html>`_
programming.

Pythonic loops
^^^^^^^^^^^^^^

Folks coming from C might feel at home with index-based `while` loops:

.. code-block:: python

    # Non-Pythonic
    choices = ['red', 'green', 'blue']
    i = 0
    while i < len(choices):
        print('{}) {}'.format(i, choices[i]))
        i += 1

or with `for` loops like this:

.. code-block:: python

    # Non-Pythonic
    choices = ['red', 'green', 'blue']
    for i in range(len(choices)):
        print('{}) {}'.format(i, choices[i]))

When index is not required, a more Pythonic way would be to run a 
`for` loop over a collection:

.. code-block:: python

    # Pythonic!
    choices = ['red', 'green', 'blue']
    for choice in choices:
        print(choice)

Otherwise `enumerate <https://docs.python.org/3/library/functions.html#enumerate>`_
the collection and run a `for` loop over the enumeration:

.. code-block:: python

    # Pythonic!
    choices = ['red', 'green', 'blue']
    for idx, choice in enumerate(choices):
        print('{}) {}'.format(idx, choice))

As a side note, Python's `for` loop is quite different
from what we have in C, Java or JavaScript. Technically, it's a
`foreach <https://en.wikipedia.org/wiki/Foreach_loop>`_ loop.

What if we got many collections to loop over? As naive as it
could get:

.. code-block:: python

    # Non-Pythonic
    preferences = ['first', 'second', 'third']
    choices = ['red', 'green', 'blue']
    for i in range(len(choices)):
        print('{}) {}'.format(preferences[i], choices[i]))

But there is a better way -- use `zip <https://docs.python.org/3/library/functions.html#zip>`_:

.. code-block:: python

    # Pythonic!
    preferences = ['first', 'second', 'third']
    choices = ['red', 'green', 'blue']
    for preference, choice in zip(preferences, choices):
        print('{}) {}'.format(preference, choice))

Comprehensions, no tiny loops
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Even perfectly a Pythonic loop can be further improved by turning it
into a list or dictionary comprehension. Consider quite a mundane 
for-loop building a sublist on a condition:

.. code-block:: python

    # Non-Pythonic
    oyster_months = []
    for month in months:
        if 'r' in month:
            oyster_months.append(month)

`List comprehension <https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions>`_
reduces the whole loop into a one-liner!

.. code-block:: python

    # Pythonic!
    oyster_months = [month for month in months if 'r' in month]

Dictionary comprehension works similarly, but for mapping types.

Readable signatures
^^^^^^^^^^^^^^^^^^^

Differing from many languages, in Python, names of function
parameters are always part of function signature:

.. code-block:: python

    >>> def count_fruits(apples, oranges):
    ...     return apples + oranges
    ... 
    >>> count_fruits(apples=12, oranges=21)
    >>> count_fruits(garlic=14, carrots=12)
    TypeError: count_fruits() got an unexpected keyword argument 'garlic'

The outcome is twofold: a caller can explicitly refer to a parameter name 
to improve code readability. The function's author should be aware of 
callers possibly binding to a once announced name and restrain from 
changing names in public APIs.

At any rate, passing named parameters to the functions we call
adds to code readability.

Named tuples for readability
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Wrapping structured stuff into a tuple is a recipe for communicating 
multiple items with a function. Trouble is that it quickly becomes 
messy:

.. code-block:: python

    # Non-Pythonic
    >>> team = ('Jan', 'Viliam', 'Ilya')
    >>> team
    ('Jan', 'Viliam', 'Ilya')
    >>> lead = team[0]
    
`Named tuples <https://docs.python.org/3/library/collections.html#collections.namedtuple>`_
simply add names to tuple elements so that we can enjoy object notation for 
getting hold of them:

.. code-block:: python

    # Pythonic!
    >>> Team = collections.namedtuple('Team', ['lead', 'eng_1', 'eng_2'])
    >>> team = Team('Jan', 'Viliam', 'Ilya')
    >>> team
    Team(lead='Jan', eng_1='Viliam', eng_2='Ilya')
    >>> lead = team.lead

Using named tuples improves readability at a cost of creating an extra
class. Keep in mind, though, that `namedtuple` factory function
creates new class by `exec`'ing a template -- that may slow things down
in a tight loop. 

Exceptions, no checks
^^^^^^^^^^^^^^^^^^^^^

Raising an exception is a primary vehicle for communicating errors in
a Python program. It's easier to ask for forgiveness than permission,
right?

.. code-block:: python

    # Non-Pythonic
    if resource_exists():
        use_resource()
        
    # Pythonic!
    try:
        use_resource()
    except ResourceDoesNotExist:
        ...

Beware likely failing exceptions in tight loops, though -- those may slow
down your code.

It is generally advisable to subclass built-in exception classes. That
helps to clearly communicate errors that are specific to our problem
and differentiate errors that bubble up from our code from other, less
expected failures.

Ad-hoc namespaces
^^^^^^^^^^^^^^^^^

When we encounter colliding variables, we might want to isolate them from
each other. The most obvious way is to wrap at least one of them
into a class:

.. code-block:: python

    # Non-Pythonic
    class NS:
        pass

    ns = NS()
    ns.fruites = ['apple', 'orange']

But there is a handy Pythonic shortcut:

.. code-block:: python

    # Pythonic!
    ns = types.SimpleNamespace(fruites=['apple', 'orange'])

The `SimpleNamespace <https://docs.python.org/3/library/types.html#types.SimpleNamespace>`_
object acts like any class instance -- we can add, change or remove 
attributes at any moment.

Dictionary goodies
^^^^^^^^^^^^^^^^^^

Python `dict <https://docs.python.org/3/library/stdtypes.html#dict>`_
is a well-understood canonical data type much like a Perl `hash` or a 
Java `HashMap`. In Python, however, we have a few  more built-in 
features like returning a value for a missing key:

.. code-block:: python

    >>> {}.get('missing key', 'failover value')
    'failover value'

Conditionally setting a key if it's not present:

.. code-block:: python

    >>> {}.setdefault('key', 'new value')
    'new value'
    >>> {'key': 'old value'}.setdefault('key', 'new value')
    'old value'

Or automatically generate an initial value for missing keys:

.. code-block:: python

    >>> d = collections.defaultdict(int)
    >>> d['missing key'] += 1
    >>> d['missing key']
    1

A dictionary that maintains key insertion order:

.. code-block:: python

    >>> d = collections.OrderedDict()
    >>> d['x'] = 1
    >>> d['y'] = 1
    >>> list(d)
    ['x', 'y']
    >>> del d['x']
    >>> d['x'] = 1
    >>> list(d)
    ['y', 'x']

Newcomers may not be aware of these nifty little tools -- let's tell them! 

Go for iterables
^^^^^^^^^^^^^^^^
 
When it comes to collections, especially large or expensive ones
to compute, the concept of `iterability <https://docs.python.org/3/glossary.html#term-iterable>`_
kicks right in. To start with, a `for` loop implicitly operates over 
`Iterable` objects:

.. code-block:: python

    for x in [1, 2, 3]:
        print(x)

    for line in open('myfile.txt'):
        print(line)

Many built-in types are already iterable. User objects can become 
iterable by supporting the iteration protocol:

.. code-block:: python
    
    class Team:
        def __init__(self, *members):
            self.members = members
            self.index = 0
        
        def __iter__(self):
            return self
            
        def __next__(self):
            try:
                return self.members[self.index]
            except IndexError:
                raise StopIteration
            finally:
                self.index += 1

so they can be iterated over a loop:

.. code-block:: python

    >>> team = Team('Jan', 'Viliam', 'Ilya')
    >>> for member in team:
    ...     print(member)
    ...         
    Jan
    Viliam
    Ilya

as well as in many other contexts where an iterable is expected:

.. code-block:: python

    >>> team = Team('Jan', 'Viliam', 'Ilya')
    >>> reversed(team)
    ['Ilya', 'Viliam', 'Jan']

Iterable user functions are known as `generators <https://docs.python.org/3/glossary.html#term-generator>`_:

.. code-block:: python

    def team(*members):
        for member in members:
            yield member

    >>> for member in team('Jan', 'Viliam', 'Ilya'):
    ...     print(member)
    ...     
    ... 
    Jan
    Viliam
    Ilya

The concept of an iterable type is firmly built into the Python 
infrastructure and it is considered Pythonic to leverage iterability
features.

Besides being handled by built-in operators, there is a collection
of functions in the 
`itertools <https://docs.python.org/3.6/library/itertools.html#module-itertools>`_ 
module that are designed to consume and/or produce iterables.

Properties for gradual encapsulation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
 
Java and C++ are particularly famous for promoting object state
protection by operating via "accessor" methods also known as 
getters/setters. A Pythonic alternative to them is based on
the `property` feature. Unlike Java programmers, Pythonistas do
not begin with planting getters and setters into their code. They
start out with simple, unprotected attributes:

.. code-block:: python

    class Team:
        members = ['Jan', 'Viliam', 'Ilya']
    
    team = Team()
    print(team.members)

Once a need for protection arises, we turn an attribute into a 
`property <https://docs.python.org/3/library/functions.html#property>`_
by either adding access control into setter:

.. code-block:: python

    class Team:
        _members = ['Jan', 'Viliam', 'Ilya']
        
        @property
        def members(self):
            return list(self._members)
    
        @members.setter
        def members(self, value):
            raise RuntimeError('This team is too precious to touch!')
    
    >>> team = Team()
    >>> print(team.members)
    ['Jan', 'Viliam', 'Ilya']
    >>> team.members = []
    RuntimeError('This team is too precious to touch!',)

Python properties are implemented on top of 
`descriptors <https://docs.python.org/3/reference/datamodel.html#descriptors>`_ 
which is a lower-level but more universal mechanism to get hold on attribute
access.

Context managers to guard resources
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It is common for programs to acquire resources, use them, and clean
up after. A simplistic implementation might look like this:

.. code-block:: python

    # Non-Pythonic
    resource = allocate()
    try:
        resource.use()
    finally:
        resource.deallocate()

In Python, we could refactor this into something more succinct, leveraging
the `context manager protocol <https://docs.python.org/3/library/stdtypes.html#typecontextmanager>`_:

.. code-block:: python

    # Pythonic!
    with allocate_resource() as resource:
        resource.use()
        
The expression following a `with` must support the context manager
protocol. Its `__enter__` and `__exit__` magic methods will be called
respectively before and after the statements inside the `with` block.

Context managers are idiomatic in Python for all sorts of resource 
control situations: working with files, connections, locks, processes.
To give a few examples, this code will ensure that a connection to
web server is closed once the execution gets out of `with` block: 

.. code-block:: python
 
    with contextlib.closing(urllib.urlopen('https://redhat.com')) as conn:
        conn.readlines()

The `supress` context manager silently ignores the specified
exception if it occurs within the body of the with statement:

.. code-block:: python

    with contextlib.suppress(IOError):
        os.unlink('non-existing-file.txt')

Decorators to add functionality
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Python `decorators <https://www.python.org/dev/peps/pep-0318/>`_
work by wrapping a function with another function. Use cases 
include memoization, locking, pre/post-processing, access control, 
timing, and many more.

Consider a straightforward memoization implementation:

.. code-block:: python

    # Non-Pythonic
    cache = {}
    def compute(arg):
        if arg not in cache:
            cache[arg] = do_heavy_computation(arg)
        return cache[arg]

This is where Python decorators come in handy:

.. code-block:: python

    def universal_memoization_decorator(computing_func):
        cache = {}
        def wrapped(arg):
            if arg not in cache:
                cache[arg] = computing_func(arg)
            return cache[arg]
        return wrapped
        
    # Pythonic!
    @universal_memoization_decorator
    def compute(arg)
        return do_heavy_computation(arg)

The power of decorators comes from their ability to modify function
behaviour in a non-invasive and universal way. That opens up
`possibilities <https://wiki.python.org/moin/PythonDecoratorLibrary>`_
to offload business logic into a specialized decorator and reuse it across
the whole codebase.

The Python standard library offers many of ready-made decorators. For
example, the above memoization tool is readily available in standard
library:

.. code-block:: python

    # Pythonic!
    @functools.lru_cache
    def compute(arg):
        return do_heavy_computation(arg)

Decorators made their way into public APIs in large projects like
Django or PyTest.

Duck typing
^^^^^^^^^^^

`Duck typing <https://en.wikipedia.org/wiki/Duck_typing>`_ is highly
encouraged in Python for being more productive and flexible. A frequent 
use-case involves emulating built-in Python types such as containers:

.. code-block:: python
    
    class DictLikeType:
        def __init__(self, *args, **kwargs):
            self.store = dict(*args, **kwargs)
            
        def __getitem__(self, key): 
            return self.store[key]
            
        ...

Full container protocol emulation requires many magic methods to
be present and properly implemented. That can become laborious and
error prone. A better way is to base user containers on top
of a `respective <https://docs.python.org/3/library/collections.abc.html>`_
abstract base class:

.. code-block:: python

    # Pythonic!
    class DictLikeType(collections.abc.MutableMapping):
        def __init__(self, *args, **kwargs):
            self.store = dict(*args, **kwargs)
    
        def __getitem__(self, key):
            return self.store[key]
            
        ...
        
Not only we'd have to implement less magic methods, the ABC harness
ensures that all mandatory protocol methods are in place. That
partly mitigates the inherent fragility of dynamic typing.

Type checks
^^^^^^^^^^^

Type checking based on types hierarchy is a popular pattern in Python
programs. People with a background in statically-typed languages tend
to introduce ad-hoc type checks like this:

.. code-block:: python

    # Non-Pythonic
    if not isinstance(x, list):
        raise ApplicationError('Python list type is expected')

While not discouraged in Python, type checks could be made more
general and reliable by testing against abstract base types:

.. code-block:: python

    # Pythonic!
    if not isinstance(x, collections.abc.MutableSequence):
        raise ApplicationError('A sequence type is expected')

That immediately makes a type check compatible with both built-in and 
user types that inherit from abstract base classes.

Static typing tends to make programs more reliable by leveraging explicit
type information, computing types compatibility based on hierarchy
and failing gracefully when type error is discovered.

Alternative to ad-hoc type checks is 
`gradual typing <https://www.python.org/dev/peps/pep-0484/>`_ technique 
which is fully supported since Python 3.6. Static typing in Python
is based on the idea of annotating important variables with type 
information, then running a `static analyzer <http://mypy.readthedocs.io>`_
over the annotated code like this:

.. code-block:: python

    def filter_by_key(d: typing.Mapping, s: str) -> dict:
        return {k: d[k] for k in d if k == s}
    
    d: dict = filter_by_key('x': 1, 'y': 2}, 'x')

In type hints technique is adopted by a project, type annotations can
fully replace ad-hoc type checks throughout the code.

Pythonista's power tools
------------------------

It may occur to a reviewer, that a more efficient solution is possibly
viable here and there. To establish solid technical grounds by backing
his refactoring proposal with hard numbers, as opposed to intuition or
personal preference, a quick analysis may come in handy. 

Among the tools I use when researching for a better solution are 
`dis <https://docs.python.org/3/library/dis.html>`_ 
(for bytecode analysis), 
`timeit <https://docs.python.org/3/library/timeit.html>`_ (for code snippets 
running time measurement) and 
`profile <https://docs.python.org/3/library/profile.html>`_
(for finding hot spots in a running Python program).

Happy reviewing!
