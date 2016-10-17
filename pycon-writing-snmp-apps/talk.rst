
Writing SNMP Apps in Python
---------------------------

*Ilya Etingof <ilya@glas.net>, October 2015*

Introduction
------------

SNMP is an abbreviation for Simple Network Management Protocol. It 
is widely used in network management/monitoring as well as system
administration.

I know from experience that Python is frequently used as a glue
language for systems automation and maintenance tasks. Thus, the
availability of SNMP operations support in Python environment is helpful.

This talk is going to explore SNMP technology in general and ways we
could access and use it from Python.

Agenda
------

I will start from the history of SNMP development and motivation. Then
I'll give a brief overview on the state of SNMP support in Python
environment.

Next I will drill deeper into design and use of PySNMP
package and this is going to be the main part of this talk.

By way of PySNMP discussion, I'll touch the topic of performing
SNMP operations in parallel, what is a frequent requirement when it
comes to managing large networks.

Finally, I'll conclude with a brief reference to some PySNMP-based
software that happened to build up over the years of library existence.

The history of SNMP
-------------------

In the early days of networking, when computer networks were research
artifacts rather than a critical infrastructure used by 3 billion 
people, "network management" was an unheard of thing.  If one
encountered a network problem, one might run a few pings to locate the
source of the problem and then modify system settings, reboot hardware
or software, or call a remote colleague to check the console.

A very interesting discussion of the first major "crash" of the
ARPAnet in 1980, long before network management tools were
available, and the efforts taken to recover from and understand the
crash can be read in RFC789. The astonishment of the engineers taking
part in post-mortem investigation could be read between the lines.

As the public Internet and private intranets have grown from small
networks into a large global infrastructure, the need to more
systematically manage the huge number of hardware and software
components within these networks has grown more important as well.   

SNMP was quickly designed and deployed by a group of university network
researchers and users at a time when the need for
network management was becoming painfully clear. It was initially thought
as an interim solution to fill the need for network management
tool while a more theoretically sound system was being developed by
the ISO.

Anticipating the transition to the new network management system, SNMP
designers made SNMP modular. Although that transition never occurred,
the modularity of SNMP help it evolving through three major versions
and found widespread use and acceptance.

SNMP reached the status of full internet standard -- the highest maturity 
level for an RFC.

Terminology
-----------

The network management field has its own specific terminology for
various components of a network management architecture, and so we
adopt that terminology here. 

The peculiarity of this terminology is that the word "management"
is greatly overused. So bare with it.

There are three principle components of a network management architecture:
a managing entity, the managed entity, and a network management protocol.

* The managing entity is an application, typically with a
  human-in-the-loop, running in a centralized network management
  station.  The managing entity is the central locus of activity for
  network management -  it controls the collection, processing,
  analysis, and/or display of network management information.  It is
  here that actions are initiated to control network behavior and here
  that  the human network administrator interacts with the network
  devices.

* A managed entity is a piece of hardware or software that resides on
  a managed network. It enumerates and formalizes some of its
  properties and states, important for healthy operation, thus making
  them available to the managing entity.

  A managed entity might be a host, router, switch, printer, or any 
  other device.

* The third piece of a network management system is the network
  management protocol. The protocol runs between the managing entity
  and the managed entity, allowing the managing entity to query the
  status of managed entity and indirectly effect actions in these
  devices via its agents.

Perhaps the most visible encounter of SNMP in action could be seen on
this slide. It's a graph plotted by a network management station
on the basis on SNMP-collected statistics.

Is it still relevant?
---------------------

Considering how old SNMP is you might be wondering why it is still in
use and is there a more modern alternative? Apparently, SNMP is still
the primary way to do performance and fault management.

SNMP is universally supported by all networking hardware manufactures
and network management applications.

Perhaps one reason for SNMP being so tenacious is that, considering SNNP's
wide deployment, it takes too much effort to migrate to anything else.
But the other reason is that no significant drawbacks have been
found in SNMP at least in the areas of fault and performance
management.

Additionally, SNMP is free and not controlled by any particular vendor. No
copyright or licensing fees are required, so anyone can use it or build
SNMP products on it.

As for current SNMP deployment, I can't really estimate how many
SNMP-enabled devices run on the modern Internet. I could probably
argue that it is safe to say that SNMP monitors the all the Internet
nowdays.

You may found SNMP useful for your home network monitoring or
management needs. For instance you could easily setup an open source
network monitoring application to watch, collect and graph bandwidth
utilization at your Wi-Fi router for you home network (that helps
spotting bottlenecks).

A significant innovation might be coming in the following years. And that
is Internet of Things. All those small and low-power gadgets need to
be monitored and managed. And that may bring new life to the SNMP
technology.

I found it amusing to realize that almost 30 years ago, SNMP was
designed for heavily resource-constrained computers of that time.
Later on our computers grew in power and resources. But now we are
back to building a massive amount of low-power computers for "things"
and original SNMP lightweightness can serve us again.

Other alternatives?
-------------------

Despite significant efforts made by technology companies and standards
bodies over all these years, no other network monitoring standard
was adopted so far. The most prominent alternative is probably
NETCONF. However it mostly targets configuration management tasks rather
than fault or performance monitoring. Additionally, NETCONF is
significantly more resource intensive than SNMP is.

It is obviously possible to for everybody to come up with its own
ad-hoc management system. That can be done very easily on top of
HTTPS/JSON, for example. However that would only work with your
application. Also, SSL engine might be heavier on resources.

SNMP basics
-----------

SNMP is designed around a client-server model. What's interesting that both
managing and managed entities contain client and server components.

Clients and servers exchange data in a name-value form.

Values are strongly typed.

SNMP base types
---------------

SNMP quantifies the properties of managed entities. To express their
values in measurable terms, SNMP uses integers and strings. Those
SNMP integers and strings belong to ASN.1 types that SNMP borrows.

ASN.1 is a way to describe, structure and serialize arbitrary data.

If INTEGER and OCTET STRING types are self-explanatory, the OID type
is more curious. It's a way to identify everything in a decentralized
fashion.

This system can be depicted as a tree whose nodes are assigned by
different organizations, knowledge domains, concepts, objects.  From
human perspective, an OID is a long sequence of numbers, coding the
nodes, separated by dots.

SNMP MIBs
---------

SNMP introduces a concept of MIBs that are designed to group somehow
relevant managed entity properties together. Properties described in
MIB are called managed objects or MIB objects.

Each MIB object has a unique identifier (OID) and associated data type.

MIBs are text files written in DSL called SMI.

MIBs are functionally similar to database schemas.

SNMP support in Python
----------------------

As it usually goes with Python, when you want to bring in some new
functionality, there are two principal approaches. Either you could
wrap or anyhow call some existing C code thus providing access to it
from Python, or you could implement the whole thing from the scratch
in pure-Python.

As for SNMP, there is number-one implementation which is Net-SNMP.
It is a reference implementation that goes along with the development
of SNMP standards. So Python bindings are shipped with it and also
there are a number of third-party wrappers.

The other way, that is building SNMP stack from the scratch all in
Python, was taken by just a few projects. Among them the pysnmp is
probably the most functionally complete.

I'm going to spend a good portion of my talk on PySNMP library's interfaces
and use cases.

PySNMP project
--------------

The PySNMP project started as a home automation effort to track
bandwidth usage of my home network.

Shortly thereafter, SNMP design attracted my attention and I aimed at
making it fully compliant with the standards. That's why internal library
structure is aligned with abstract service interfaces as described in RFCs.

By this time it supports most of SNMP features.

Pure-Python, open source and free.

PySNMP works with all reasonable Pythons (2.4-3.5).

PySNMP design
-------------

Internally, PySNMP is very much aligned with abstract service
interfaces described in the standards. Library structure is also
similar to canonical SNMP engine design.

SnmpEngine is a central object taking part in all PySNMP calls.

Building SNMP query
-------------------

Let's make a simple SNMP query to read one MIB object. For that, we
will call a getCmd function passing it some parameters. In the
following slides we will gradually build this call.

Setting protocol version
------------------------

Here we have a choice of three SNMP protocol versions. To employ
versions 1 or 2c, we pass properly initialized instance of
CommunityName class. For the third SNMP version we pass UsmUserData
class instance.

Setting transport and target
----------------------------

Next we have to choose network transport to use (and the options here
are UDP over IPv4 or IPv6) and network address of the managed entity.

Specifying MIB object
---------------------

Finally, we have to specify the MIB object we want to read. We do that
with help of two classes - ObjectType and ObjectIdentity. We will talk
about them in greater details in a moment, for now it's interesting to
note now that we request the sysUpTime property now.

PySNMP MIB objects
------------------

One of the main reasons for MIB objects to exist is to glue properies
names and values together. In PySNMP we use the ObjectIdentity class
that is responsible for properties identification. The ObjectType
class groups ObjectIdentity with SNMP data type.

ObjectIdentity class
--------------------

ObjectIdentity could be initialized with MIB object name, after a MIB
look up it starts behaving like an OID.

ObjectType class
----------------

ObjectType is a container object that references ObjectIdentity and SNMP
type instances.

Does it make sense?
-------------------

You can probably get a feeling that SNMP is not that simple. Afterall,
it takes about 10K lines of Python code. Fortunately, PySNMP ships a
high-level API that hides many details and simplifies SNMP use.

PySNMP high-level API
---------------------

PySNMP high-level API comes in two flavors: synchronous and
asynchronous. The first is most intuitive, but it can only perform one
SNMP operation at a time.

The second can run multiple SNMP operations simultaneously on top of
one of the supported asynchronous I/O frameworks.

Synchronous API
---------------

The distinctive feature of synchronous API is that it is build around
the idea of Python generator. Any function invocation ends up with a
generator object. Iteration over the generator object performs actual
SNMP communication. On each iteration SNMP message gets build and send
out, response is awaited, received and parsed.

Saving slide space
------------------

I'll leave out some code in the next slides to save space.

Feeding generator object
------------------------

Python generators can not only produce data, but it is also possible
to send data into running generator object. That feature is used by
the high-level API to repeat the same SNMP operation for a new set
of MIB objects.

Fetch table element
-------------------

SNMP defines a concept of table. Tables are used when a single given
MIB object may apply to many instances of a property. For example,
properties of network interfaces are put into SNMP table. Each
instance of a property is addressed by a suffix appended to base MIB
object.

PySNMP fully supports table operations.

Sequence of MIB objects
-----------------------

SNMP defines the GETNEXT/GETBULK commands that makes managed entity
returning "next" MIB object past the given one. MIB objects are sorted
by their OIDs.

MIB objects modification
------------------------

Configuration management part of SNMP relies on the SET command.
Although its implementation on managed entity's side proved to be
somewhat demanding (due to locking and transactional behavior
requirements), so that vendors tend to leave it out thus rendering
managed entity being read-only.

Although PySNMP fully supports SET operation.

SNMP notifications
------------------

Managed entity could send unsolicited messages to the managing entity.
That is called notification in SNMP. Notifications help reduce
polling, what may become a problem for a large network.

SNMP notifications are enumerated and each has definite semantics.

NOTIFICATION-TYPE
-----------------

Notifications are formally described in MIBs. Here's an example of
such declaration. Like OBJECT-TYPE's, notifications are identified with
OIDs.

NotificationType class
----------------------

To model NOTIFICATION-TYPE construct in PySNMP, we have the
NotificationType class. Like ObjectType is refers to ObjectIdentity to
to identify notification.

Sending notification
--------------------

Sending notification with PySNMP is no much different than sending
command. The difference is in the data we pass with the operation.

High-volume messaging
---------------------

When in comes to managing large network, reading MIB objects
sequentially introduces latency. By some point the latency becomes
intolerable. Solutions to parallelize queries are well known - you
could do that by offloading individual operations into multiple
processes, or multiple threads of execution or build your application
around the asynchronous I/O model.

PySNMP is designed with asynchronous I/O in mind.

Asynchronous I/O
----------------

Compared to other solutions, asynchronous model is most lightweight
and scalable. The idea is simple: never wait for I/O - do something
else whenever possible.

The back side of this is that execution flow becomes non-linear what
hurts program analysis by human reader.

PySNMP high-level API is adapted to work with three popular
asynchronous I/O frameworks - asyncore, Twisted and asyncio.

asyncio
-------

asyncio is a well known innovation. It lets you write asynchronously
running code in synchronous, sequential style. That practically
eliminates callbacks.

Besides that, asyncio includes a collection of conventional
synchronization primitives (like Semaphores) aligned with those in
threading module.

SNMP query with asyncio
-----------------------

Making SNMP query with asyncio is not very different than calling
synchronous high-level interface.

Parallel queries
----------------

With asyncio we could do all sort of parallelization things. We can
fire up many SNMP queries at once, or chain them anyhow. We could use
synchronization primitives to control request rate.

SNMP Agent
----------

So far we only talked about the "client" side of SNMP. But there is
also the "server" side which is frequently associated with SNMP agent.
This is the piece of software running on managed entity.

PySNMP fully supports agent operations. A typical workflow for
utilizing SNMP agent is to put user code (that might interface with
the host system/application) into MIB modules. Python version of MIB
modules, or boilerplate code, can be autogenerated.

PySNMP-based software
---------------------

PySNMP is a quite mature library, so some software happened to build
up on top of it.

Command-line tools
------------------

There is a collection of command-line SNMP management tools written in
pure-Python. From command-line perspective, they mimic their counterparts
from the Net-SNMP project, however they are cross-platform and
pypi-installable.

SNMP simulator
--------------

SNMP simulator makes an illusion that many SNMP managed entities run on
your network. They are live and all different.

Simulator can build its simulation model from other managed entities
or from MIBs or it can snoop on the wire recovering SNMP traffic and
building simulation models for all managed entities it can hear.

Proxy forwarder
---------------

This is a application-layer firewall specialized on handling SNMP
traffic. Besides the possibility to translate SNMP versions and
transports, it can block, route or modify SNMP messages on the fly. It
is also extendable via Python code snippets.

Summary
-------

SNMP is kind of old-fashioned but still very relevant. It is widely
deployed and used in network management and system administration.

It may be picked up by the Internet of Things in the future.

The PySNMP package is here to help you with quick SNMP scripting, or
testing other SNMP software or you can learn and experiment with SNMP!

