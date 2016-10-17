.. title:: I/O concurrency: asyncio
.. meta::
  :author: Ilya Etingof

.. class:: context

:data-scale: 1.5

I/O concurrency: asyncio
========================

* Ilya Etingof, August 2015


Agenda
======

* What is concurrency, why we sometimes want it?
* Different approaches to concurrency (with Python code snippets)
* Python features relevant to asyncio framework
* Asyncio architecture
* Asyncio idioms
* Asyncio libraries

Computation model
=================

Many computing tasks take some time to complete, and there are two 
reasons why a task might take some time:

* It is computationally intensive so it is CPU-bound; or
* It is not computationally intensive but has to wait for data to 
  be available to produce a result. So it is I/O-bound.

Known solutions include:

* Handle each connection in a separate operating system process
* Handle each connection in a separate thread of execution
* Use non-blocking system calls to handle all connections in one thread

First two works for both CPU and I/O-bound tasks, while the last works best
for programs performing I/O with many peers exchanging data in small chunks.

Base case: HTTP client
======================

Trivial synchronous HTTP client:

.. code-block:: python

  import socket

  def httpGet(host, port=80):
      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      s.connect((host, port))
      s.send('GET / HTTP/1.1\r\n\r\n')
      data = s.recv(1024*1024)
      return data

  httpGet('www.github.com')
  httpGet('www.github.com')

...but no concurrency! Everything goes sequentially.

Multiple processes
==================

Extensive approach: many stand-alone synchronous clients:

.. code-block:: python

   import concurrent.futures
   import socket

   sites = ['www.github.com', 'www.github.com']

   def httpGet(host, port=80):
       s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       s.connect((host, port))
       s.send(b'GET / HTTP/1.1\r\n\r\n')
       return s.recv(1024*1024)

   with concurrent.futures.ProcessPoolExecutor() as executor:
       for response in executor.map(httpGet, sites):
           print(response)

The above code is:

* highly concurrent
* immune to GIL plague
* very inefficient resource-wise

Multiple threads of execution
=============================

Next step towards efficiency:

* Single process
* Lesser memory footprint
* More efficient internal communication

.. code-block:: python

   import concurrent.futures
   import socket

   sites = ['www.github.com', 'www.github.com']

   def httpGet(host, port=80):
       s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       s.connect((host, port))
       s.send(b'GET / HTTP/1.1\r\n\r\n')
       return s.recv(1024*1024)

   with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
       for response in executor.map(httpGet, sites):
           print(response)

Multiple threads of execution (cont)
====================================

Multiple threads solution has drawbacks:

* Suboptinal in terms of threads management expense
* May quickly hit stack memory/scheduler performance limits 
  (by just a few hundreds of threads)
* Prone to subtile bugs related to resource management (e.g. locking,
  memory management etc) especially in imported code
* In case of Python, GIL is a bottleneck - just one thread can run
  at a time even on multi-CPU/multicore CPU system

On the bright side:

* Threads execution scheduling is still done by OS kernel
* Works for both I/O and CPU bound situations

Non-blocking sockets
====================

Works best in I/O-bound situations where many I/O streams are served.

* Network applications
* GUI

Relies on OS services:

* Turn file descriptors into a non-blocking operation mode
* Use select()/poll()/epoll()/kpoll()/IOCP OS-level events scheduler
  to catch I/O events and timeouts
* Call user functions to process I/O events and timers
* Scales up to hundreds of thousands connections (AKA C10K problem)

Application becomes structured like this:

* Main loop from where OS event dispatcher is called
* Multiple event-specific functions
* Heap-based data structure to carry state between functions

In large apps program logic appears scattered across many small 
functions what leads to a phenomena known as...

Callback Hell
=============

  *"It requires super human discipline to write readable code in callbacks
  and if you don’t believe me look at any piece of JavaScript code."*

  *-- Guido van Rossum*

Earlier implementation: bare sockets
=====================================

...slide space is too limited to fit such monster!

Earlier implementation: asyncore
================================

Initially known as Medusa, in stdlib since Python 1.x.  Early attempt to 
pack/hide/simplify callback and context management.

.. code-block:: python

    class HttpClient(asyncore.dispatcher):
        def __init__(self, host, port=80, req=b'GET / HTTP/1.1\r\n\r\n'):
            asyncore.dispatcher.__init__(self)
            self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
            self.read_buffer = b''
            self.write_buffer = req
            self.connect((host, port))

        def writable(self): return len(self.write_buffer) > 0
        def readable(self): return True

        def handle_write(self):
            sent = self.send(self.write_buffer)
            self.write_buffer = self.write_buffer[sent:]

        def handle_read(self):
            self.read_buffer += self.recv(8192)

    clients = [ HttpClient('www.python.org'), HttpClient('www.github.com) ]
    asyncore.loop()

Earlier implementation: Twisted
===============================

* Introduces the concepts of Transports, Protocols and Deferreds
* Multiple mainloops called Reactors

.. code-block:: python

    class HttpClient(LineReceiver):
        def connectionMade(self):
            self.sendLine('GET / HTTP/1.1\r\n\r\n')

    class HttpClientFactory(ClientFactory):
        protocol = HttpClient
        def __init__(self):
            self.done = Deferred()

    def bootstrap(reactor):
        factory = HttpClientFactory()
        reactor.connectTCP('www.github.com', 80, factory)
        return factory.done

    task.react(bootstrap)

A twist: Deferred
=================

Callbacks are traditionally used to deliver the result of a non-blocking 
operation at some point in the future.

.. code-block:: python

    def startNonBlockingOperation(inSuccessCbFun, onErrorCbFun):
        ...
        onSuccessCbFun(...)

Twisted Deferred is an object created as a result of non-blocking operation 
start. User can attach a pair of callbacks (and context) to Deferred:

.. code-block:: python

    d = startNonBlockingOperation()
    d.addCallback(inSuccessCbFun)
    d.addErrback(onErrorCbFun)

Once non-blocking operation is completed (or failed), user callback is invoked.

Deferreds can be chained by one callback returning new Deferred thus saying: 
"this callback doesn't have the answer yet, but when this Deferred fires 
it will!".

Introducing asyncio
===================

Features synchronous, sequential, blocking style of coding while
being internally asynchronous.

.. code-block:: python

   import asyncio

   @asyncio.coroutine
   def httpGet():
       reader, writer = yield from asyncio.open_connection(host, port=80)
       writer.write(b'GET / HTTP/1.1\r\n\r\n')
       while True:
           line = yield from reader.readline()
           if not line:
               break
           print(line)

       writer.close()

   loop = asyncio.get_event_loop()
   loop.run_until_complete(httpGet('www.github.com'))

* Converts callbacks into Python generators iterated by main loop
* Keeps context in closures (technically, stack frames)
* Makes an illusion of sequential flow of execution

Python features: decorators
===========================

Functions are First Class Citizens (e.g. objects), so we can
pass them around like any other object:

.. code-block:: python

   def doWork(): pass

   def repeatWork(fn, times):
       for i in range(times):
           fn()

   repeatWork(doWork)

Functions can be declared within the scope of another function what
creates a closure that can be used as a decorator (@decorator syntax 
is kind of a shortcut):

.. code-block:: python

   def outer(fn):
       def inner(*args, **kwargs):
           print("Calling %s" % (fn.func_name))
           return fn(*args, **kwargs)
       return inner

  f = outer(lambda x: x+1)
  f(42)

 
Python features: iterators
==========================

Reading data items from an object one by one is called iteration:

.. code-block:: pycon

   >>> mylist = [1, 2, 3]
   >>> for i in mylist:
   ...    print(i)
   1
   2
   3

mylist is an iterable.

Iterables are handy because read can be incremental and incomplete. But
all values may have to be stored in memory what may be expensive.

Any object implementing *__iter__()* method is iterable. Any object 
implementing *__next__()* comprises an iterator. 

Objects return iterators to iterate on themselves. Iterators are objects 
that let you iterate on iterables.

Python features: generators
===========================

Generators are one-time iterators. It's because they do not store all
the values in memory, they generate the values on the fly.

.. code-block:: pycon

   >>> mygenerator = (x*x for x in range(2))
   >>> for i in mygenerator:
   ...    print(i)
   0
   1

When a function uses *yield* instead of *return* statement, it becomes
and returns a generator.

.. code-block:: python

   def infiniteGenerator(start=0):
       while True:
           yield start
           start += 1

   for num in infiniteGenerator(4):
       print(num, end=' ')

Calling conventional function will execute its code immediately, whereas
calling function with *yield* will just return generator object.

Python features: generators (cont)
==================================

Once called (through *__next__()*), generator function postpones execution 
when hitting *yield*. 

Generator function preserves its state (local variables, next instruction)
between runs till generator's exhausted.

.. code-block:: pycon

   >>> class Bank():
   ...    crisis = False
   ...    def create_atm(self):
   ...        while not self.crisis:
   ...            yield "100CZK"
   >>> csob = Bank()
   >>> atm = csob.create_atm()
   >>> print(atm.next())
   100CZK
   >>> print([atm.next() for cash in range(5)])
   ['100CZK', '100CZK','100CZK','100CZK','100CZK']
   >>> csob.crisis = True
   >>> print(atm.next())
   <type 'exceptions.StopIteration'>

News flash! Generators can be duplex: you can send data inside running 
generator!

Python features: delegating to subgenerator
===========================================

Consider a generator that looks like this:

.. code-block:: python

    def generator():
        for i in range(10):
            yield i
        for j in range(10, 20):
            yield j

that can be rewriten like this:

.. code-block:: python

    def generator2():
        for i in range(10):
            yield i

    def generator3():
        for j in range(10, 20):
            yield j

    def generator():
        yield from generator2()
        yield from generator3()

Transfers iteration to upper level. Utterly important in asyncio.

Asyncio architecture
====================

Greately influenced by existing asynchronous frameworks, notably
Twisted (see PEP3156).

Concepts:

* Coroutine: just a generator. Its power comes from a way asyncio uses it.
* Futures: object that promises to hold some result (including exceptions)
  if it's available or indicate that's not yet there.
* Tasks: is a subclass of Future which can accomodate a coroutine.

Building blocks:

* Event loop: serves two purposes - multiplex different activities and
  offers API for creating base...
* Transports
* Protocols

Asyncio: mainloop
=================

Mainloop facts:

* It is a per-process or per-thread singleton
* User replaceable by supporting public API

Multiplexor role:

.. code-block:: python

   import asyncio

   @asyncio.coroutine
   def hello_world():
       print("Hello World!")

   loop = asyncio.get_event_loop()

   # Blocking call which returns when the hello_world() coroutine is done
   loop.run_until_complete(hello_world())

   loop.close()

Asyncio: mainloop (cont)
========================

As a multiplexor, designed to handle callbacks as well as coroutines:

.. code-block:: python

   import asyncio

   def hello_world(loop):
       print('Hello World')
       loop.stop()

   loop = asyncio.get_event_loop()

   # Schedule a call to hello_world()
   loop.call_soon(hello_world, loop)

   # Blocking call interrupted by loop.stop()
   loop.run_forever()
   loop.close()

also supports time-wise call scheduling, can be used for periodic tasks
internal to user application.

Asyncio: Transports
===================

Transport represents an endpoint of network connection. It sits between
Python app and OS network stack.

* Usually shipped with asyncio, but could be added by user
* Used by both client and server side of connection

Default mainloop supports:

* TCP/UDP/UNIX/SSL/TLS network transports
* UNIX signal handlers
* UNIX pipes 
* Threads and processes (to offload blocking code)

Asyncio: Transports (cont)
==========================

Example: open TCP client connection.

.. code-block:: python

   import asyncio

   @asyncio.coroutine
   def tcp_echo_client(loop):
       reader, writer = yield from asyncio.open_connection('127.0.0.1', 8888,
                                                           loop=loop)

       sent = yield from writer.write(b'Hello World!')
       data = yield from reader.read(100)

       writer.close()

   loop = asyncio.get_event_loop()
   loop.run_until_complete(tcp_echo_client(message, loop))

Asyncio: Protocols
==================

Protocol is task-specific code wrapped in an object. Can be seen as a
collection of callbacks with pre-defined meaning.

Protocol classes are used in conjunction with transports:

* Protocol parses incoming data and asks for the writing of outgoing data
* Transport is responsible for the actual I/O and buffering

Asyncio is shipped with base Protocol implementations. Users are expected
to subclass them and override some callbacks to define specific logic.

Asyncio: Protocols (cont)
=========================

.. code-block:: python

   import asyncio

   class LovelyProtocol(asyncio.Protocol):
       def __init__(self, loop):
           self.loop = loop

       def connection_made(self, transport):
           transport.write(b'iloveyou')

       def data_received(self, data):
           assert data == b'iloveyou', '%-('
           self.loop.stop()

   loop = asyncio.get_event_loop()
   coro = loop.create_connection(lambda: LovelyProtocol(loop),
                                 '127.0.0.1', 8888)
   loop.run_until_complete(coro)
   loop.run_forever()

Asyncio: Futures
================

The concurrent.futures.Future class encapsulates the asynchronous execution 
of a callable. Only makes sense in the context of a dispatcher managing 
Future instances (concurrent.futures.{Thread|Process}PoolExecutor).

Asyncio Future is:

* Simular to Futures from concurrent.futures (PEP-3148)
* *yield from* works with Future!

.. code-block:: python

   f = Future()
   r = yield from f  # r <- f.result()

Future will yield itself (as a generator) till Future is done (result becomes
available).

Asyncio: Future eats Callback
=============================

Stepping away from callbacks:

* Isolate callback stuff in a coroutine
* Promote coroutine as your official API

.. code-block:: python

   @asyncio.coroutine
   def sync_looking_function(*args):
       f = acyncio.Future()
       def cb(result, error):
           if error is not None:
               f.set_result(result)
           else:
               f.set_exception(Exception(error))
      true_async_function(cb. *args)
      return (yield from f)

Now you can call your async function as if it was synchronous:

.. code-block:: python

   result = yield from sync_looking_function()

Asyncio: Tasks
==============

.. class:: right

   *A riddle wrapped in a mystery inside an enigma.*
      -- Churchil on Russia

Task is a coroutine wrapped in a Future. Consequently, *yield from*
works for Tasks:

.. code-block:: python

   r = asyncio.Task(coro(...))  # r <- Task.result()
   
Unlike coroutines, Task can magically advance without calling them explicitly.

Tasks let coroutines running independently and concurrently with others
within the same event loop. 

When a Task wraps a coroutine, the Task is connected to the event loop, 
and then runs automatically when the loop is started, thus providing a 
mechanism for automatically driving the coroutine.


Asyncio idioms: sequential execution
====================================

Mutually sequential and ordered. But many instances of this code
can run simultaneously.

.. code-block:: python

   import asyncio
 
   @asyncio.coroutine
   def multistep_coroutine():
       yield from asyncio.sleep(4)
       yield from asyncio.sleep(3)
       yield from asyncio.sleep(1)
 
   loop = asyncio.get_event_loop()
   loop.run_until_complete(multistep_coroutine())
   loop.close()

The asyncio.sleep() is a non-blocking version of time.sleep(). We use
it here to mock some meaningful I/O operation.


Asyncio idioms: parallel execution
==================================

Mutually parallel and unordered:

.. code-block:: python

   import asyncio
 
   @asyncio.coroutine
   def my_coroutine(seconds_to_sleep):
       yield from asyncio.sleep(seconds_to_sleep)
 
   loop = asyncio.get_event_loop()
   tasks = [ asyncio.Task(my_coroutine(4)),
             asyncio.Task(my_coroutine(3)),
             asyncio.Task(my_coroutine(2)) ]
   loop.run_until_complete(asyncio.gather(*tasks))
   loop.close()

The asyncio.gather() call returns a Future aggregating results from the 
given coroutine objects or futures.


Asyncio idioms: chained execution
=================================

Coroutine can call other coroutines via *yield from* therefore executing
sequentially.

.. code-block:: python

   import asyncio
 
   @asyncio.coroutine
   def my_inner_coroutine():
       yield from asyncio.sleep(0.5)

   @asyncio.coroutine
   def my_outer_coroutine():
       for x in range(3):
           yield from my_inner_coroutine()
 
   loop = asyncio.get_event_loop()
   loop.run_until_complete(my_outer_coroutine())
   loop.close()


Asyncio idioms: timer
=====================

Spin off an infinitly looping task doing some housekeeping that
we might need in our app:

.. code-block:: python

   import asyncio
 
   @asyncio.coroutine
   def timer(period):
       while True:
           #... check something go sleeping ...
           yield from asyncio.sleep(period)
 
   loop = asyncio.get_event_loop()
   asyncio.async(asyncio.Task(timer(1)))
   loop.run_forever()

Note: asyncio.async() can receive a coroutine and wrap it into a Task.


Asyncio apps: HTTP
==================

The aiohttp is based on stdlib http, urllib and asyncio.

.. code-block:: python

   import asyncio
   import aiohttp
 
   @asyncio.coroutine
   def fetch_page(url):
       response = yield from aiohttp.request('GET', url)
       assert response.status == 200
       content = yield from response.read()
 
   loop = asyncio.get_event_loop()
   tasks = [
       fetch_page('http://devel.errata.redhat.com'),
       fetch_page('http://bugzilla.redhat.com')]
   loop.run_until_complete(asyncio.wait(tasks))
   loop.close()
 
   for task in tasks:
       print(task)


Asyncio apps: SQL
=================

The aiopg package wraps asynchronous features of the Psycopg database driver
into asyncio library module.

.. code-block:: python

   import asyncio
   import aiopg

   dsn = 'dbname=aiopg user=aiopg password=passwd host=127.0.0.1'

   @asyncio.coroutine
   def select():
       pool = yield from aiopg.create_pool(dsn)
       with (yield from pool.cursor()) as cur:
           yield from cur.execute("SELECT 1")
           ret = yield from cur.fetchone()
           assert ret == (1,)

   loop = asyncio.get_event_loop()
   loop.run_until_complete(select())
   loop.close()


Asyncio apps: Redis
===================

.. code-block:: python

   import asyncio
   from asyncio_redis import RedisProtocol

   def set_key():
       transp, proto = yield from loop.create_connection(RedisProtocol,
                                                         'localhost', 6379)

       yield from proto.set('key', 'value')

       result = yield from proto.get('key')

       assert result == 'value'

       trans.close()

   loop = asyncio.get_event_loop()
   loop.run_until_complete(set_key())
   loop.close()


Thank you!
==========

Questions?

Further reading:

* `Generator Tricks for Systems Programmers <http://www.dabeaz.com/generators/>`_
* `A Curious Course on Coroutines and Concurrency <http://www.dabeaz.com/coroutines/>`_
* `Generators: The Final Frontier <http://www.dabeaz.com/finalgenerator/>`_
* `Python Async IO Resources <http://asyncio.org/>`_



