
Writing SNMP Apps in Python
===========================

*Ilya Etingof <ilya@glas.net>*

Abstract
========

* SNMP - Simple Network Management Protocol
* SNMP is widely used by system/network administrators
* Monitoring/automation scripts are written in Python
* This talk explores the technologies involved

Agenda
======

* SNMP motivation and history
* State of SNMP support in Python
* PySNMP implementation in depth
* Massively parallel queries
* Tools built on top of PySNMP

Why network management?
=======================

* Non-existent in early networks
* Lagged behind networks development
* ...till major outages became too painful (October 1980, RFC789)
* SNMP enters the scene

History of SNMP
===============

* Research project
* SNMPv1 in 1988: initial revision
* SNMPv2 in 1993: improvements
* SNMPv3 in 1999: full redesign
* Full Internet standard (STD0062)
* Interim solution since 1988!

Terminology
===========

* Managing entity: collects and process
* Managed entity: exposes its properties and states
* Protocol: moves data over [unstable] network

.. image:: nms-components.svg

Network monitoring station
==========================

* Collects and graphs CPU load, disk space, network traffic stats,
  routing tables and many other things

.. image:: cacti-graph.png

Is it still relevant?
=====================

* Widely supported by hardware and software vendors
* No vendor control, patents licensing fees
* Internet infrastructure is being monitored via SNMP
* Home network management (Wi-Fi router, UPS, sensors)
* Internet of Things is coming bringing in 50B things in 5 years!

Other alternatives?
===================

* Not really:

  + NETCONF (RFC6241)
  + CMIP (Common Management Information Protocol)
  + WMI (Microsoft Windows only)
  + Proprietary REST API-based solutions

Bustering SNMP myths
====================

* It is NOT that simple
* It is NOT JUST a protocol
* It CAN BE secure (despite its abbreviation)

SNMP basics
===========

* Client-server model
* Exchanges data in name-value form
* Values are typed
* Messages indicate the operation to be performed

Base SNMP types
===============

* Expresses the properties of managed entities in measurable terms
* Three basic types (plus some subtypes):

  + INTEGER
  + OCTET STRING
  + OBJECT IDENTIFIER

We can identify everything!
===========================

* Tree of nodes assigned to whatever
* Sequence of numbers depicting nodes

.. image:: oid-tree.svg

SNMP MIBs
=========

* MIB - Management Information Base
* Way to collect many related properties together
* MIB objects (AKA managed objects) are properties described in MIB
* MIB - text file written in the SMI language (Structure of Management
  Information)
* Functionally similar to a database schema

MIB facts
=========

* RFCs define about 10,000 MIB objects
* At least 9,000 MIBs were created by vendors
* Vendors get their own subtrees under "enterprises" node managed
  by IANA (PySNMP got a fancy one: 20408)
* Many MIBs were shipped with syntax errors!

SNMP support in Python
======================

* Net-SNMP bindings (written in C)

  + netsnmp module as shipped with Net-SNMP
  + yapsnmp, pyNetSNMP, easysnmp

* Pure-Python implementations

  + libsnmp, fastsnmp, pysnmp

PySNMP project
==============

* Initially, home network monitoring script
* Aims at full standards compliancy
* Supports most SNMP features
* Pure-Python, open source and free
* Works with all reasonable Pythons (2.4-3.5)

PySNMP design
=============

* SNMP engine is the central, umbrella object

.. image:: pysnmp-design.svg

Building SNMP query
===================

* Let's send SNMP GET command
* By calling high-level API function...

.. class:: prettyprint lang-python

::

    >>> from pysnmp.hlapi import *
    >>> [ x for x in dir() if 'Cmd' in x]
    ['bulkCmd', 'getCmd', 'nextCmd', 'setCmd']
    >>> getCmd
    <function getCmd at 0x222b330>
    >>> g = getCmd(
    ...

Setting protocol version
========================

* SNMPv1/v2c via *CommunityData* class
* SNMPv3 via *UsmUserData* class
* SNMPv1/v2c are both 100% insecure!

.. class:: prettyprint lang-python

::

    >>> from pysnmp.hlapi import *
    >>> g = getCmd(CommunityData('public'),
    ...

Setting transport and target
============================

* Use UDP-over-IPv4 transport via *UdpTransportTarget* class
* Or UDP-over-IPv6 via *Udp6TransportTarget*
* Destination is SNMP agent at *demo.snmplabs.com*

.. class:: prettyprint lang-python

::

    >>> from pysnmp.hlapi import *
    >>> g = getCmd(CommunityData('public'),
    ...            UdpTransportTarget(('demo.snmplabs.com', 161)),
    ...

Specifying MIB object
=====================

* Let's read *sysDescr* MIB object instance from *SNMPv2-MIB*
* ContextData parameter indicates SNMP context (we ignore it for now)

.. class:: prettyprint lang-python

::

    >>> from pysnmp.hlapi import *
    >>> g = getCmd(CommunityData('public'),
    ...            UdpTransportTarget(('demo.snmplabs.com', 161)),
    ...            ContextData(),
    ...            ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)))

Performing the query
====================

* Synchronous high-level API is based on Python generators
* Loop over the generator object

.. class:: prettyprint lang-python

::

    >>> from pysnmp.hlapi import *
    >>> g = getCmd(CommunityData('public'),
    ...            UdpTransportTarget(('demo.snmplabs.com', 161)),
    ...            ContextData(),
    ...            ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysUpTime', 0)))
    >>> next(g)
    (None, 0, 0, [ObjectType(ObjectIdentity('1.3.6.1.2.1.1.3.0'),
                             TimeTicks(44430646))])

PySNMP MIB objects
==================

* MIB objects glue property name and value together
* *ObjectIdentity* represents MIB object name
* *ObjectType* represents MIB object as a whole

.. class:: prettyprint lang-smi

::

   sysUpTime OBJECT-TYPE
       SYNTAX      TimeTicks
       MAX-ACCESS  read-only
       STATUS      current
       DESCRIPTION
               "The time (in hundredths of a second) since
               the network management portion of the system
               was last re-initialized."
       ::= { system 3 }

ObjectType class
================

* Holds an instance of *ObjectIdentity*
* ...and an instance of SNMP data type
* Looks like a tuple of (OID, value) e.g. variable-bindings

.. class:: prettyprint lang-python

::

    >>> x = ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0),
                       'Linux i386 box'))
    >>> # ... calling MIB look up ...
    >>> x[0].prettyPrint()
    'SNMPv2-MIB::sysDescr.0'
    >>> x[1].prettyPrint()
    'Linux i386 box'

Does it make sense?
===================

* SNMP is not that simple
* It takes 10K+ lines of Python code
* Fortunately, PySNMP ships high-level API!

PySNMP high-level API
=====================

* API flavors:

  + Synchronous
  + Asynchronous: asyncore
  + Asynchronous: Twisted
  + Asynchronous: asyncio/trollius

Synchronous API
===============

* Sequential, blocking queries
* SNMP operations occur on generator object iteration

.. class:: prettyprint lang-python

::

    >>> from pysnmp.hlapi import *
    >>> g = nextCmd(SnmpEngine(),
    ...             CommunityData('public'),
    ...             UdpTransportTarget(('demo.snmplabs.com', 161)),
    ...             ContextData(),
    ...             ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr')))
    >>> next(g)
    (None, 0, 0, [ObjectType(ObjectIdentity('1.3.6.1.2.1.1.1.0'),
                             DisplayString('SunOS zeus.snmplabs.com'))])

Saving slide space
==================

* Common parts: LCD configuration

.. class:: prettyprint lang-python

::

    ...             SnmpEngine(),
    ...             CommunityData('public'),
    ...             UdpTransportTarget(('demo.snmplabs.com', 161)),
    ...             ContextData(),

* in further code will be replaced with:

.. class:: prettyprint lang-python

::

    ...             < initialization code here >

Feeding generator object
========================

* We can do more queries by feeding new queries to the generator

.. class:: prettyprint lang-python

::

    >>> from pysnmp.hlapi import *
    >>> g = nextCmd(< initialization code here >)
    >>>
    >>> g.send([ObjectType(ObjectIdentity('IF-MIB', 'ifInOctets'))])
    (None, 0, 0, [(ObjectType(ObjectIdentity('1.3.6.1.2.1.2.2.1.10.1'),
                              Counter32(284817787))])

Fetch table element
===================

* Many instances of the same MIB object form SNMP table
* SNMP table elements addressed by extending MIB object ID

.. class:: prettyprint lang-python

::

    >>> from pysnmp.hlapi import *
    >>> g = nextCmd(
    ...     < initialization code here >
    ...     ObjectType(ObjectIdentity('IP-MIB', 'ipAddressStatus',
    ...                               1, '127.0.0.0'))
    ... )
    >>> next(g)
    (None, 0, 0, [ObjectType(ObjectIdentity('1.3.6.1.2.1.4.34.1.7.1.127.0.0.1'),
                             Integer('preferred(1)'))])

Sequence of MIB objects
=======================

* GETNEXT command return "next" adjacent OID
* We can query OIDs we are not aware of
* And fetch all OIDs that agent shows us

.. class:: prettyprint lang-python

::

    >>> from pysnmp.hlapi import *
    >>> g = nextCmd(< initialization code here >
    ...             ObjectType(ObjectIdentity('1.3.6')))
    >>> next(g)
    (None, 0, 0, [ObjectType(ObjectIdentity('1.3.6.1.2.1.1.1.0'),
                             DisplayString('SunOS zeus.snmplabs.com'))])
    >>> next(g)
    (None, 0, 0, [ObjectType(ObjectIdentity('1.3.6.1.2.1.1.2.0'),
                             ObjectIdentifier('1.3.6.1.4.1.20408'))])

MIB objects modification
========================

* SET command
* Designed to configure devices remotely
* Supports advisory locking
* Transactional at PDU level
* Can create new table rows
* Often not implemented

SNMP notifications
==================

* Polling too many MIB objects takes time
* Solution: unsolicited messaging on "interesting" events
* Events are enumerated and have definite semantics
* Manager may do followup queries to gather event details

NOTIFICATION-TYPE
=================

* SMI construct to define notification
* Assigns unique OID
* References MIB objects relevant to this event

.. class:: prettyprint lang-smi

::

   linkUp NOTIFICATION-TYPE
       OBJECTS { ifIndex, ifAdminStatus, ifOperStatus }
       STATUS  current
       DESCRIPTION
           "..."
   ::= { snmpTraps 4 }

NotificationType class
======================

* Holds an instance of *ObjectIdentity*
* ...and refers to relevant *ObjectType*'s
* Looks like a sequence of *ObjectType* class instances

.. class:: prettyprint lang-python

::

    >>> from pysnmp.hlapi import *
    >>> x = NotificationType(ObjectIdentity('IF-MIB', 'linkUp'))
    >>> # ... calling MIB look up ...
    >>> >>> [ str(y) for x in n ]
    ['SNMPv2-MIB::snmpTrapOID.0 = 1.3.6.1.6.3.1.1.5.3',
     'IF-MIB::ifIndex = ', 'IF-MIB::ifAdminStatus = ',
     'IF-MIB::ifOperStatus = ']

Sending notification
====================

* Code is similar to previous examples
* The difference is in how MIB objects are specified
* The *trap* or *inform* parameter influence PDU type being used

.. class:: prettyprint lang-python

::

   >>> from pysnmp.hlapi import *
   >>> g = sendNotification(
   ...     < initialization code here >
   ...     'trap',
   ...     NotificationType(ObjectIdentity('IF-MIB', 'linkUp'))
   ... )
   >>> next(g)
   (None, 0, 0, [])

High-volume messaging
=====================

* Large networks may require intensive SNMP polling
* Sequential polling introduces latency
* Ways to parallelize SNMP messaging:

  + Multiple processes
  + Multiple threads
  + Asynchronous I/O

Asynchronous I/O
================

* Scalable and efficient for I/O bound tasks
* Idea: never wait for I/O, do other work meanwhile
* Single-threaded
* Non-linear execution makes it non-intuitive
* PySNMP works with asyncore, Twisted and asyncio/trollius

asyncio
=======

* Twisted reinvented
* Relies on latest language features
* Asynchronous code written in sequential fashion
* *asyncio* offers conventional primitives as the *threading* module
  (Lock, Event, Condition, Semaphore)

SNMP query with asyncio
=======================

.. class:: prettyprint lang-python

::

   >>> import asyncio
   >>> from pysnmp.hlapi.asyncio import *
   >>>
   >>> @asyncio.coroutine
   ... def snmpget():
   ...     result = yield from getCmd(
                    < initialization code here >
   ...              ObjectType(ObjectIdentity('SNMPv2-MIB',
   ...                                        'sysDescr', 0))
   ...     )
   ...     print(result)
   >>>
   >>> asyncio.get_event_loop().run_until_complete(snmpget())
   (None, 0, 0, [ObjectType(ObjectIdentity('1.3.6.1.2.1.1.1.0'),
                            DisplayString('SunOS zeus.snmplabs.com'))])

Parallel queries
================

* Many SNMP operations running in parallel
* Chain SNMP operations passing data from one to the other
* Queues/conditions/semaphores to control request rate

.. class:: prettyprint lang-python

::

   >>> ...
   >>> loop = asyncio.get_event_loop()
   >>> loop.run_until_complete(
   ...     asyncio.wait([snmpget(), snmpget(), snmpget()])
   ... )

SNMP Agent
==========

* Design: PySNMP engine + MIB modules expressed in Python
* User code lives in MIB modules
* Boilerplate MIB modules can be autogenerated
* PySNMP core can un/load MIB modules on the fly

PySNMP-based software
=====================

* Solves practical problems
* Verifies library functionality
* Drives further development

Command-line tools
==================

* Net-SNMP ships command-line tools (snmp*)
* PySNMP mimics them (snmp*.py)
* Nearly identical command-line interface
* Cross-platform

More info: https://pypi.python.org/pypi/pysnmp-apps/

SNMP simulator
==============

* Makes an illusion of many SNMP agents present on the network
* Simulated agents are live and different
* Builds simulation models from real SNMP agents
* ...and by populating MIBs with values
* ...and by snooping SNMP traffic

More info: http://snmpsim.sf.net

Proxy forwarder
===============

* A network of SNMP manager and agent nodes
* Application-layer firewall / proxy
* Translates SNMP versions and network transports
* Filters / modifies SNMP messages based on various criterion
* Extendable through Python code snippets

More info: https://pypi.python.org/pypi/snmpfwd/

Summary
=======

* SNMP technology is old-fashioned but still relevant
* Used in network and system administration
* PySNMP may be helpful for SNMP scripting
* ...or for SNMP software testing
* ...or to learn and experiment with SNMP! ;-)

Thank you!
==========

Questions?

Further reading
===============

* More technical version of this talk `http://pysnmp.sf.net/pycon/2015/slides-long.html <http://pysnmp.sf.net/pycon/2015/slides-long.html>`_
* `PySNMP documentation and example scripts <http://pysnmp.sf.net>`_
* `SNMP, SNMPv2, SNMPv3, and RMON 1 and 2 <http://www.amazon.com/SNMP-SNMPv2-SNMPv3-RMON-Edition/dp/0201485346>`_
* `A Curious Course on Coroutines and Concurrency <http://www.dabeaz.com/coroutines/>`_
* `Python Async IO Resources <http://asyncio.org/>`_
