
Enjoyable Python code review
============================

Most of us, programmers, go through the technical interviews every once
in a while. At other times many of us sit at the opposite side of the 
table running these interviews. I found that code review process may 
have something in common with job interviews.

While it is clearly in the best interest of all team members to end up
with high quality code, differences in technical background,
cultural differences, previous experience, personalities and even temper
may get in the way influencing people's behaviour.

Consider an imaginary pull request. There we typically have two actors:
author and code reviewers. Sometimes authors tend to overestimate the
quality  of their code what provokes them to be overly defensive and 
even hostile to any argument. People reviewing the code may find themselves
being in a position of power to judge on the author's work. Once the actors
find a matter where they take orthogonal and strong enough positions, then
all is fair in love and war.

Another interesting phenomena I encountered while reviewing Python code
can probably be attributed to Python's best qualities - clarity and easiness
to pick up. Programmers, who are new to Python, bring in the customs and
idioms they are used to with their mother language, so to say. Speaking
from my experience, I could frequently tell former Java, Perl or bash
programmer from their Python code. As much as I admire other technologies
and expertise, I believe it is most efficient and enjoyable to code in 
harmony with the language rather than stretching it beyond its intended
design. 

In this blog post I'm going to summarize my experience in authoring
and reviewing Python code from both psychological and technical
perspectives. My ultimate goal here is to strike a balance between
code reviews being enjoyable and technically fruitful.

Why we review code
------------------

The most immediate purpose of a code review is to make code better by
focusing more eyeballs at it. But code review seems to be a lot more
than that!
 
To my experience, it is also a way for the engineers to communicate, 
learn and even socialize over a meaningful and mutually interesting topic.
For a team where both senior and junior engineers work together, for the
latter code review gives an opportunity to observe masters at work and
learn from that.

Seniors, in turn, get a chance to couch fellow engineers, be challenged and
thus proof their authority (which is healthy). Everyone could see the
problem from other perspectives, what may ultimately contribute to better
outcome.

For mature Pythonistas coding with newbies, code review is a way to teach
them how we do things in Python up to the extent of brewing idiomatic Python
coders out of them.

Optimizing for health
---------------------

The best we can do on psychological side is if author relinquishes 
emotional attachment to their code, while reviewers consciously
restrain from attacking author's ideas, mentoring them.

Way more comforting and ultimately productive is for reviewers to stay
positive, thankful and praise the author personally. Suggested
changes should be justified by a solid technical grounds but never 
reviewer's personal preference.

For authors it may help to keep reminding themselves how much time and
effort it might have taken for reviewers to work with author's code.
So that their feedback is precious. 

As idealistic as it sounds, my approach is to downplay my ego by optimizing
for healthier team and enjoyable job. I suspect that it might come at the
cost of compromised quality of the code we, as a team, produce. My hope
here is that even if we do merge suboptimal code at times, we will eventually
learn from that and refactor later. That's way cheaper compared to ending up
with stressed, despaired and demotivated team effectively stuck at its 
project.

When I'm an author
------------------

Core review is a hard and expensive endeavour. Proper code review may 
require the reviewers to study business logic behind a change, learn 
language tricks that are new to them, trace code execution, conduct 
thought experiments, consider edge cases.

The larger is the change the more effort it would take for reviewers to
accomplish it. That gives smaller, isolated changes better chances for 
a quality review.

Authors should not take PR lightly. Properly documented change
complying with team's policies has greater chances for favorable
review and quicker merge. I feel myself more confident if I run a
quick code review against my prospective PR prior to submitting it to 
fellow engineers.

When I'm a reviewer
-------------------

To me, the most important qualities of a code is to be clean
and Pythonic.

Clean code tends to be well-structured where logically distinct parts
are isolated from each other via clearly visible boundaries. Ideally,
each part is specialized on solving a single problem. As Zen of Python
puts it: "If the implementation is easy to explain, it may be 
a good idea".

Signs of a clear code include self-documented functions and variables 
describing problem entities, not implementation details.

Readability counts, indeed, though I would not sweat full PEP8
compliance up to the cost of nitpicking and bikesheding.

I praise authors coding on the shoulders of giants, meaning abstracting
problem into canonical data structures and algorithms and working from
that. That gives me a warm feeling of author belonging to the same 
trade guild and confidence that we both know what to expect from the
code.

Pythonic touch
--------------

The definition of code being Pythonic tends to be somewhat vague and
subjective. Speaking from my experience in the fields, let me offer 
you a handful of code refactoring suggestions leveraging features
that are native to Python so that people with different backgrounds
may be unaware of them.

### Keyword args

Different from many languages, in Python, all names of function
parameters are always part of function signature:

    >>> def count_fruits(apples, oranges):
    ...     return apples + oranges
    ... 
    >>> count_fruits(apples=12, oranges=21)
    >>> count_fruits(garlic=14, carrots=12)
    TypeError: count_fruits() got an unexpected keyword argument 'garlic'

The outcome is twofold: caller can explicitly refer to parameter name 
to improve code readability. Function author should be aware of
callers possibly binding to once announced name and restrain from 
changing names in public APIs.

### Exceptions

Raising exception is a primary vehicle for communicating errors in
a Python program. It's easier to ask for forgiveness than permission,
right?

    # This is not Pythonic
    if resource_exists():
        use_resource()
        
    # This is Pythonic
    try:
        use_resource()
    except ResourceDoesNotExist:
        ...

It is generally advisable to subclass build-in exception classes. That
helps clearly communicating errors that are specific to your problem
and tell errors bubbling up from your code from other, less expected
failures.

### Strings concatenation

For Perl programmers, who are used to `.` operator, it may be tempting to
merge Python strings by `+`'ing them up. But proper way is to `join()`
them:
 
    >>> ' '.join(['Red', 'Hat'])
    'Red Hat'

Despite recent CPython optimization in that regard, older and other 
Python implementations still suffer from quadratic behaviour of strings
concatenation operation.

### Named tuples

Wrapping structured stuff into a tuple is a recipe for communicating 
multiple items with a function. Trouble is that it quickly becomes 
messy:

    >>> team = ('Jan', 'Viliam', 'Ilya')
    >>> team
    ('Jan', 'Viliam', 'Ilya')
    >>> lead = team[0]
    
Named tuples simply add names to tuple elements so that you can enjoy
object notation for getting hold of them:

    >>> Team = collections.namedtuple('Team', ['lead', 'eng_1', 'eng_2'])
    >>> team = Team('Jan', 'Viliam', 'Ilya')
    >>> team
    Team(lead='Jan', eng_1='Viliam', eng_2='Ilya')
    >>> lead = team.lead

Using named tuples improves readability at a cost of creating an extra
class. Keep in mind, though, that `namedtuple` factory function
creates new class by `exec`'ing a template what may be slow. 

### Ad-hoc namespaces

We may get a colliding variables which we may want to isolate from
each other. Most obvious way is to wrap one into a class:

    class NS:
        pass

    ns = NS()
    ns.fruites = ['apple', 'orange']

But there is a handy shortcut:

    ns = types.SimpleNamespace(fruites=['apple', 'orange'])

The namespace object acts like any class instance -- you can
add/reassign/remove attributes at any moment.

### Dictionaries

Python dict is a well-understood canonical data type much like 
Perl `hash` or Java `HashMap`. In Python, however, we have a few 
more built-in goodies like returning a value for a missing key:

    >>> {}.get('missing key', 'failover value')
    'failover value'

Conditionally setting key if it's not present:

    >>> {}.setdefault('key', 'new value')
    'new value'
    >>> {'key': 'old value'}.setdefault('key', 'new value')
    'old value'

Automatically generate initial value for missing keys:

    >>> d = collections.defaultdict(int)
    >>> d['missing key'] += 1
    >>> d['missing key']
    1

Dictionary that maintains key insertion order:

    >>> d = collections.OrderedDict()
    >>> d['x'] = 1
    >>> d['y'] = 1
    >>> list(d)
    ['x', 'y']
    >>> del d['x']
    >>> d['x'] = 1
    >>> list(d)
    ['y', 'x']

### Loops, Iterators and Generators
 
Despite simple and familiar appearance, there is a huge amount of
power is hiding beneath the `for` loop. It is considered highly
Pythonic to take advantage of them. 

To start with, `for` loop implicitly operates over `Iterable`s.
Objects representing a collection of something are good candidates
for being iterable:

    for x in [1, 2, 3]:
        print(x)

    for line in open('myfile.txt'):
        print(line)

Objects can become iterable by supporting the iteration protocol:
    
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

so they could be iterated over a loop:

    >>> team = Team('Jan', 'Viliam', 'Ilya')
    >>> for member in team:
    ...     print(member)
    ...         
    Jan
    Viliam
    Ilya

As well as in many other contexts where an iterable is expected:

    >>> team = Team('Jan', 'Viliam', 'Ilya')
    >>> sorted(team)
    ['Ilya', 'Jan', 'Viliam']

Iterable user functions are known as generators. Neither Java nor Perl
or Ruby offer them, so this is something worth noting:

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

The concept of iterable is firmly built into Python infrastructure.
Besides being handled by built-in operators, there is a collection
of higher-order functions in the `itertools` module operating over
iterables.

### Properties
 
Java and C++ are particularly famous for promoting object state
protection by operating via "accessor" methods also known as 
getters/setters. Pythonic alternative to them is based on
the `property` feature. Unlike Java programmers, Pythonistas do
not start planting getters and setters into their code. They
start out with simple, unprotected attributes:

    class Team:
        members = ['Jan', 'Viliam', 'Ilya']
    
    team = Team()
    print(team.members)

Once a need for protection arises, we turn attribute into property
by either adding access control into setter:

    class Team:
        _members = ['Jan', 'Viliam', 'Ilya']
        
        @property
        def members(self):
            return list(self._members)
    
        @members.setter
        def members(self, value):
            raise RuntimeError('This team is precious!')
    
    >>> team = Team()
    >>> print(team.members)
    ['Jan', 'Viliam', 'Ilya']
    >>> team.members = []
    RuntimeError('This team is precious!',)

### Context managers

### Decorators

### ABC

Tools
-----

linter, timeit, dis
