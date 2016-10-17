
Writing SNMP Apps in Python
===========================

*Ilya Etingof <ilya@glas.net>, October 2015*

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

History of SNMP
===============

* Research project, successor of SGMP
* SNMPv1 in 1988: initial revision
* SNMPv2 in 1993: improvements
* SNMPv3 in 1999: full redesign
* SNMPv3: backward compatible
* SNMPv3: full Internet standard (STD0062)
* Interim solution since 1988!

Terminology
===========

* Managing entity: collects, process, displays
* Managed entity: enumerates and quantifies properties and states
* Network management protocol: moves data over [unstable] network

Architecture
============

.. image:: nms-components.svg

SNMP - network management framework
===================================

* Principal components:

  + data model
  + database schema
  + protocol

* Components are modular

SNMP components: data model
===========================

* Base types: identify and quantify states and properties
* Data definition language (SMI) for higher level constructs

SNMP components: database
=========================

* Database "schema" of management objects - MIB
* Object represents state or a property
* Related objects gathered into MIB modules
* MIB modules written in SMI

SNMP components: protocol
=========================

* Defines operations
* Describes procedures
* Identifies packet format

Is it still relevant?
=====================

* Widely supported by hardware and software vendors
* No patents or copyright licensing fees
* Internet infrastructure is being monitored via SNMP
* Home automation: Wi-Fi router, UPS, sensors
* Internet of Things is coming!

Network monitoring station
==========================

* Collects and graphs CPU load, disk space, network traffic stats,
  routing tables and many other things

.. image:: cacti-graph.png

Other alternatives?
===================

* NETCONF (RFC6241)
* CMIP (Common Management Information Protocol)
* WMI (Microsoft Windows only)
* Proprietary HTTP/XML/JSON-based solutions

Bustering SNMP myths
====================

* It is NOT JUST a protocol
* It is NOT that simple
* It CAN BE secure (despite its abbreviation)

SNMP support in Python
======================

* Net-SNMP bindings

  + very fast

* Pure-Python implementations

  + more Pythonic and functional

Net-SNMP bindings
=================

* Net-SNMP: reference implementation of SNMP protocol (written in
  C - http://www.net-snmp.org)
* netsnmp module as shipped with Net-SNMP
* yapsnmp
* pyNetSNMP
* easysnmp

Pure-Python modules
===================

* libsnmp
* fastsnmp (Cython fork of libsnmp)
* pysnmp
* +possibly others

PySNMP project
==============

* Started as a home automation project
* Pure-Python, open source and free
* Aims at full standards compliancy
* Works with all reasonable Pythons (2.4-3.5)
* Supports most SNMP features

PySNMP basics sub-agenda
========================

* Data types
* Management objects database
* Protocol
* Applications

Base SNMP types
===============

* SNMP data types are ASN.1 types
* ASN.1 - way to structure and serialize data
* Pure ASN.1 types:

  + INTEGER
  + OCTET STRING
  + OBJECT IDENTIFIER

We can identify everything!
===========================

* OID: unique path in a tree
* OID: sequence of numbers (or labels)

.. image:: oid-tree.svg

More SNMP types
===============

* Specialized ASN.1 types:

  + Integer32/Unsigned32 - 32-bit integer
  + Counter32/Counter64 - ever increasing number
  + Gauge32 - positive, non-wrapping 31-bit integer
  + TimeTicks - time since some event
  + IPaddress - IPv4 address
  + Opaque - uninterpreted ASN.1 string

PyASN1 objects
==============

* SNMP data types are ASN.1 types
* ASN.1 types are PyASN1 objects

.. class:: prettyprint lang-python

::

    >>> from pyasn1.type.univ import *
    >>> Integer(21) * 2
    Integer(42)
    >>> Integer(-1) + Integer(1)
    Integer(0)
    >>> int(Integer(42))
    42
    >>> OctetString('Hello') + ', ' + OctetString(hexValue='5079436f6e21')
    OctetString('Hello, PyCon!')

See also: https://pypi.python.org/pypi/pyasn1/

PyASN1 OID object
=================

* Mimics a sequence of OID tree nodes (as a tuple)

.. class:: prettyprint lang-python

::

    >>> from pyasn1.type.univ import *
    >>> internetId = ObjectIdentifier((1, 3, 6, 1))
    >>> internetId
    ObjectIdentifier('1.3.6.1')
    >>> internetId[2]
    6
    >>> [ x for x in internetId ]
    [1, 3, 6, 1]
    >>> internetId + (2,)
    ObjectIdentifier('1.3.6.1.2')
    >>> internetId[1:3]
    ObjectIdentifier('3.6')
    >>> internetId[1] = 2
    ...
    TypeError: object does not support item assignment

Database of objects
===================

* Text file written in a SMI DSL
* Functionally similar to a database schema
* Lists "interesting" properties of managed entity
* MIB objects are identified by unique OIDs and symbolic,
  human-friendly names
* MIB objects carry data type information

MIB facts
=========

* RFCs define about 10,000 MIB objects
* At least 9,000 MIBs were created by vendors
* Vendors get their own subtrees under "enterprises" node managed
  by IANA (PySNMP got a fancy one: 20408)
* Many MIBs were shipped with syntax errors!

Two consumers of MIB
====================

* Managing entity

  + Looks up OID by MIB object name
  + Casts value to proper type of MIB object
  + Humans read comments left by other humans

* Managed entity

  + Implements MIB objects in code

MIB at PySNMP
=============

* All MIB constructs are Python objects
* Load Pythonized MIBs from stand-alone files whenever needed
* PySNMP MIB modules are universal - consumed by managing and managed entities
* MIB parsing and Python code generation is done by PySMI

See also: https://pypi.python.org/pypi/pysmi/

Demythifying MIBs
=================

* SNMP CAN work without MIBs
* MIB does NOT contain values
* MIB is NOT always device/vendor specific
* MIB is made for humans by humans

SNMP protocol
=============

* Two modes of operation:

  + Request-response messages
  + Unsolicited messages

* Message envelope carries identification or authentication information
  and encapsulates PDU

SNMP PDU types
==============

* Manager-to-agent

  + GetRequest, SetRequest, GetNextRequest, GetBulkRequest,
    InformRequest

* Manager-to-manager

  + InformRequest, Response

* Agent-to-manager

  + SNMPv2-Trap, Response

SNMP Applications
=================

* Five standard SNMP applications
* Usually only some of them are implemented

.. image:: snmp-apps.svg

SNMP Apps at PySNMP
===================

* Standard SNMP apps implemented by *pysnmp.entity.rfc3413*
* Run over abstract network transport
* API aligned with RFC3413 - verbose and complex
* Use high-level API whenever possible

SNMP engine
===========

* Coordinates workings of all components

.. image:: snmp-engine.svg

Configuration
=============

* All configuration resides at LCD
* LCD is a collection of MIBs
* MIB objects represent configuration settings
* LCD could be managed via SNMP

.. class:: prettyprint lang-bash

::

    $ snmpget -v2c -c public demo.snmplabs.com SNMPv2-MIB::snmpInTotalReqVars.0
    SNMPv2-MIB::snmpInTotalReqVars.0 = Counter32: 3141220
    $ snmpget -v2c -c public demo.snmplabs.com SNMPv2-MIB::snmpInTotalReqVars.0
    SNMPv2-MIB::snmpInTotalReqVars.0 = Counter32: 3141223

PySNMP design
=============

* SNMP engine is the central, umbrella object

.. image:: pysnmp-design.svg

PySNMP Engine
=============

* SnmpEngine class instance is always used
* PySNMP app can run multiple SnmpEngine's
* SNMP engine has unique identifier

.. class:: prettyprint lang-python

::

    >>> SnmpEngine()
    SnmpEngine(snmpEngineID=OctetString(hexValue='80004fb80567'))

Community Name
==============

* *CommunityData* class used to add new entry to LCD
* Controls SNMP v1/v2c version to use

.. class:: prettyprint lang-python

::

    CommunityData('public', mpModel=0)
    CommunityData('public')

USM user name
=============

* *UsmUserData* class used to add new entry to LCD
* Configures SNMPv3 user
* Optionally configures keys and crypto algorithms

.. class:: prettyprint lang-python

::

    UsmUserData('testuser', authKey='myauthkey')
    UsmUserData('testuser', authKey='myauthkey', privKey='myenckey')

USM crypto
==========

* Authentication: MD5, SHA based HMAC
* Encryption: DES, 3DES, AES128/192/256
* *UsmUserData* accepts algorithm ID
* Algorithms are identified by OIDs

Making a query
==============

* Let's make a GET query!
* Query public SNMP simulator at *demo.snmplabs.com*
* Other SNMP commands also available

.. class:: prettyprint lang-python

::

    >>> from pysnmp.hlapi import *
    >>> [ x for x in dir() if 'Cmd' in x]
    ['bulkCmd', 'getCmd', 'nextCmd', 'setCmd']
    >>> getCmd
    <function getCmd at 0x222b330>
    >>> g = getCmd(

SNMP version
============

* Most widely used is still SNMP v2c (default)
* Or we could use SNMPv1 (via mpModel=0)
* Both are 100% insecure!

.. class:: prettyprint lang-python

::

    >>> from pysnmp.hlapi import *
    >>> g = getCmd(CommunityData('public'),
    ...

Transport and target
====================

* Use UDP-over-IPv4 transport
* Default I/O framework is *asyncore*
* Destination is public SNMP simulator

.. class:: prettyprint lang-python

::

    >>> from pysnmp.hlapi import *
    >>> g = getCmd(CommunityData('public'),
    ...            UdpTransportTarget(('demo.snmplabs.com', 161)),
    ...


SNMP context
============

* Is a parameter in SNMP (v3) message
* Addresses specific collection of MIBs
* SNMP engine could serve many identical MIB instances
* Let's use default 'empty' context

.. class:: prettyprint lang-python

::

    >>> from pysnmp.hlapi import *
    >>> g = getCmd(CommunityData('public'),
    ...            UdpTransportTarget(('demo.snmplabs.com', 161)),
    ...            ContextData(),
    ...

MIB object
==========

* Let's read sysDescr MIB object instance from SNMPv2-MIB

.. class:: prettyprint lang-python

::

    >>> from pysnmp.hlapi import *
    >>> g = getCmd(CommunityData('public'),
    ...            UdpTransportTarget(('demo.snmplabs.com', 161)),
    ...            ContextData(),
    ...            ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)))

Iterate
=======

* Synchronous high-level API is based on Python generators
* Let's iterate over generator object we just created

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

More on  USM security
=====================

* SNMP can be secure since 1999
* Settings are bound to user name (can be many users)
* Authentication and encryption on per-user basis
* Everything is stored in LCD

UsmUserData class
=================

* *UsmUserData* accumulate all USM entry info
* Conveys prospective USM entry data into LCD

.. class:: prettyprint lang-python

::

    UsmUserData('testuser')
    UsmUserData('testuser', 'myauthkey')
    UsmUserData('testuser', 'myauthkey', 'myencryptionkey')

Crypto algorithms
=================

* USM uses HMAC for authenticity:

  + MD5, SHA

* And these algorithms for ciphering:
  + DES, 3DES, AES128/192/256

* Algorithms are identified by OIDs

Crypto algorithms selection
===========================

* Crypto configuration is done via *UsmUserData*
* If no keys are given, no crypto is used
* If keys are given, MD5 & DES are the defaults
* Non-default algorithms set via *UsmUserData*

Crypto options to UsmUserData
=============================

* *authProtocol* and *privProtocol* keyword parameters
* Encryption implies authentication

.. class:: prettyprint lang-python

::

    UsmUserData('testuser',
                authKey='myauthkey',
                authProtocol=usmHMACSHAAuthProtocol,
                privKey='myenckey',
                privProtocol=usmAesCfb256Protocol)

MIB support in PySNMP
=====================

* Problem statement:

  + On protocol level, MIB objects are identified by OIDs
  + But humans tend to address them by name
  + We want both!

.. class:: prettyprint lang-bash

::

    $ snmpget -v2c -c public demo.snmplabs.com SNMPv2-MIB::sysDescr.0
    SNMPv2-MIB::sysDescr.0 = STRING: SunOS zeus.snmplabs.com
    $
    $ snmpget -v2c -c public demo.snmplabs.com 1.3.6.1.2.1.1.1.0
    SNMPv2-MIB::sysDescr.0 = STRING: SunOS zeus.snmplabs.com

MIB names and OIDs
==================

* Both object name and OID come from MIB
* Name and OID linking is done by OBJECT-TYPE clause
* OBJECT-TYPE is a high-level SMI construct

OBJECT-TYPE construct
=====================

* Example: MIB object *sysUpTime*
* OID is ...mgmt.mib-2.system.3
* Value type is *TimeTicks*

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

ObjectIdentity class
====================

* Represents ways to address MIB object
* Needs MIB lookup to reach resolved state
* Can resolve MIB symbol name into OID

.. class:: prettyprint lang-python

::

    >>> x = ObjectIdentity('SNMPv2-MIB', 'system')
    >>> # ... calling MIB lookup ...
    >>> tuple(x)
    (1, 3, 6, 1, 2, 1, 1, 1)
    >>> x = ObjectIdentity('iso.org.dod.internet.mgmt.mib-2.system.sysDescr')
    >>> # ... calling MIB lookup ...
    >>> str(x)
    '1.3.6.1.2.1.1.1'

ObjectIdentity class
====================

* ...or other way round

.. class:: prettyprint lang-python

::

    >>> x = ObjectIdentity('1.3.6.1.2.1.1.1')
    >>> # ... calling MIB lookup ...
    >>> x.prettyPrint()
    'SNMPv2-MIB::sysDescr'
    >>> x = ObjectIdentity((1, 3, 6, 1, 2, 1, 1, 1))
    >>> # ... calling MIB lookup ...
    >>> str(x)
    '1.3.6.1.2.1.1.1'

MIB object instance
===================

* Objects in MIBs are just declarations
* Data is stored in MIB object instances
* Instances are addressed by OID suffix

.. image:: mib-object-instances.svg

ObjectIdentity for scalars
==========================

* Index is zero for scalar values by convention
* "index" parameter addresses MIB object instance

.. class:: prettyprint lang-python

::

    >>> x = ObjectIdentity('SNMPv2-MIB', 'system', 0)
    >>> # ... calling MIB lookup ...
    >>> tuple(x)
    (1, 3, 6, 1, 2, 1, 1, 1, 0)

SNMP tables
===========

* Related OBJECT-TYPEs can be grouped
* INDEX clause indicates common index

.. class:: prettyprint lang-smi

::

    ifEntry OBJECT-TYPE
        SYNTAX      IfEntry
        INDEX   { ifIndex }
    ::= { ifTable 1 }

    ifIndex OBJECT-TYPE
        SYNTAX      InterfaceIndex
    ::= { ifEntry 1 }

    InterfaceIndex ::= TEXTUAL-CONVENTION
        DISPLAY-HINT "d"
        SYNTAX       Integer32 (1..2147483647)

ObjectIdentity with index
=========================

* Table index is non-zero integer, or string
* Or any base SNMP type
* DISPLAY-HINT clause defines index conversion rules

.. class:: prettyprint lang-python

::

    >>> x = ObjectIdentity('NET-SNMP-EXAMPLES-MIB',
    ...                    'nsIETFWGName', 'Python')
    >>> # ... calling MIB lookup ...
    >>> str(x)
    '1.3.6.1.4.1.8072.2.2.1.1.1.6.80.121.116.104.111.110'

Composite indices
=================

* Some tables are indexed by many indices
* Indices reflect significant differences in MIB objects

.. class:: prettyprint lang-smi

::

    tcpConnectionEntry OBJECT-TYPE
        SYNTAX  TcpConnectionEntry
        INDEX   { tcpConnectionLocalAddressType,
                  tcpConnectionLocalAddress,
                  tcpConnectionLocalPort,
                  tcpConnectionRemAddressType,
                  tcpConnectionRemAddress,
                  tcpConnectionRemPort }
    ::= { tcpConnectionTable 1 }

ObjectIdentity with indices
===========================

* *ObjectIdentity* accept many indices
* Indices are in human-readable form

.. class:: prettyprint lang-python

::

    >>> x = ObjectIdentity('UDP-MIB', 'udpLocalAddress',
    ...                    '127.0.0.1', 12345)
    >>> # ... calling MIB lookup ...
    >>> str(x)
    '1.3.6.1.2.1.7.5.1.1.127.0.0.1.12345'

ObjectType class
================

* ObjectIdentity identifies MIB object / instance
* ObjectType links ObjectIdentity with value / type
* ObjectType looks like a tuple of (OID, value)

.. class:: prettyprint lang-python

::

    >>> x = ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0),
                       'Linux i386 box'))
    >>> # ... calling MIB lookup ...
    >>> x[0].prettyPrint()
    'SNMPv2-MIB::sysDescr.0'
    >>> x[1].prettyPrint()
    'Linux i386 box'

Does it make sense?
===================

* SNMP is not that simple
* It takes 10K+ lines of Python code
* Let's practice!

PySNMP applications
===================

* High-level API: function per SNMP operation
* Flavours:

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

* We can do more queries by feeding new queries to generator

.. class:: prettyprint lang-python

::

    >>> from pysnmp.hlapi import *
    >>> g = nextCmd(< initialization code here > )
    >>>
    >>> g.send([ObjectType(ObjectIdentity('IF-MIB', 'ifInOctets'))])
    (None, 0, 0, [(ObjectType(ObjectIdentity('1.3.6.1.2.1.2.2.1.10.1'),
                              Counter32(284817787))])

Fetch unrelated MIB objects
===========================

* SNMP PDU can take many unrelated OIDs

.. class:: prettyprint lang-python

::

    >>> from pysnmp.hlapi import *
    >>> g = getCmd(
    ...     < initialization code here >
    ...     ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)),
    ...     ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysUpTime', 0))
    ... )
    >>> next(g)
    (None, 0, 0, [ObjectType(ObjectIdentity('1.3.6.1.2.1.1.1.0'),
                             DisplayString('SunOS zeus.snmplabs.com')),
                  ObjectType(ObjectIdentity('1.3.6.1.2.1.1.3.0'),
                             TimeTicks(44430646))])

Fetch table element
===================

* SNMP table elements addressed via indices
* Index translates into OID suffix

.. class:: prettyprint lang-python

::

    >>> from pysnmp.hlapi import *
    >>> g = nextCmd(
    ...     < initialization code here >
    ...     ObjectType(ObjectIdentity('UDP-MIB', 'udpLocalAddress',
    ...                               '127.0.0.1', 0))
    ... )
    >>> next(g)
    (None, 0, 0, [ObjectType(ObjectIdentity('1.3.6.1.2.1.11.1.0'),
                             Counter32(3208685))])

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

Fetching MIB objects in bulk
============================

* GETBULK command return up to *R* "next" OIDs
* And a single "next" OID for first *N* OIDs

.. class:: prettyprint lang-python

::

    >>> from pysnmp.hlapi import *
    >>> N, R = 0, 25
    >>> g = bulkCmd(< initialization code here >
    ...             N, R,
    ...             ObjectType(ObjectIdentity('1.3.6')))
    >>> next(g)
    (None, 0, 0, [ObjectType(ObjectIdentity('1.3.6.1.2.1.1.1.0'),
                             DisplayString('SunOS zeus.snmplabs.com'))])
    >>> next(g)
    (None, 0, 0, [ObjectType(ObjectIdentity('1.3.6.1.2.1.1.2.0'),
                             ObjectIdentifier('1.3.6.1.4.1.20408'))])

Modifying MIB object
====================

* SET command
* Designed to configure devices remotely
* Supports advisory locking
* Transactional at PDU level
* Can create new table rows
* Often not implemented

SET operation
=============

* ObjectIdentity addresses MIB object
* ObjectType takes new value and converts it into proper SNMP type

.. class:: prettyprint lang-python

::

    >>> from pysnmp.hlapi import *
    >>> g = setCmd(
    ...     < initialization code here >
    ...     ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0),
    ...                               'Linux i386'))
    ... )
    >>> next(g)
    (None, 0, 0, [ObjectType(ObjectIdentity('1.3.6.1.2.1.1.1.0'),
                             DisplayString('Linux i386'))])

SNMP notifications
==================

* Can't poll too many MIB objects
* Unsolicited messaging on "interesting" events
* Events are enumerated and have definite semantics
* Manager can go on polling Agent on certain event

NOTIFICATION-TYPE
=================

* SMI construct to define notification
* Assignes unique OID
* References relevant OBJECT-TYPE's
* OBJECTS go into notification message

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

* Identified by ObjectIdentity
* Refers to relevant OBJECT-TYPE's
* Looks like a sequence of ObjectType class instances

.. class:: prettyprint lang-python

::

    >>> from pysnmp.hlapi import *
    >>> x = NotificationType(ObjectIdentity('IF-MIB', 'linkUp'))
    >>> # ... calling MIB lookup ...
    >>> >>> [ str(y) for x in n ]
    ['SNMPv2-MIB::snmpTrapOID.0 = 1.3.6.1.6.3.1.1.5.3',
     'IF-MIB::ifIndex = ', 'IF-MIB::ifAdminStatus = ',
     'IF-MIB::ifOperStatus = ']

Sending notification
====================

* Code is similar to command generators
* The difference is in how PDU var-binds are built
* Contents and positions of MIB objects in var-binds is important

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

No more details!
================

* We will skip some complexities:

  + How MIB objects are expanded into the instances 
  + How MIB objects instances get pulled into notification
  + How access control subsystem gets involved

* But you can catch up at http://pysnmp.sf.net

High-volume messaging
=====================

* Large networks require intensive SNMP polling
* Sequential polling takes too long
* Ways to parallelize SNMP messaging:

  + Multiple processes
  + Multiple threads
  + Asynchronous I/O

Asynchronous I/O
================

* Most efficient, lightweight and scalable
* Idea: never wait for I/O, do other work meanwhile
* Single-threaded
* Non-linear execution makes it non-intuitive
* PySNMP offers integration with three I/O frameworks: 
  asyncore, Twisted, asyncio

asyncore
========

* In Standard library for very long time
* Built around select() or poll() in main loop
* Callback-based
* No significant supporting infrastructure
* Messy to deal with

GET with asyncore
=================

* Configuration is the same as in previous examples

.. class:: prettyprint lang-python

::

   >>> from pysnmp.hlapi.asyncore import *
   >>>
   >>> def cbFun(snmpEngine, *args):
   ...     print(args):
   >>>
   >>> snmpEngine = SnmpEngine()
   >>> getCmd(< initialization code here >
   ...        ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)),
   ...        cbFun=cbFun)
   >>>
   >>> snmpEngine.transportDispatcher.runDispatcher()
   (None, 0, 0, [ObjectType(ObjectIdentity('1.3.6.1.2.1.1.1.0'),
                            DisplayString('SunOS zeus.snmplabs.com'))])

asyncore thoughts
=================

* Thin and efficient
* User code lives in callbacks
* User context is managed by user
* Can fire up many concurrent SNMP queries
* Or do concurrent I/O with other socket I/O-bound apps in
  the same main loop

Twisted
=======

* Code lives in isolated functions
* Work-in-progress is represented by Deferred objects
* User callables attached to Deferreds
* Deferreds carry states
* Twisted infrastructure: manage tasks running in parallel
  or sequentially, supports data exchange between tasks

GET with Twisted
================

.. class:: prettyprint lang-python

::

   >>> from pysnmp.hlapi.twisted import *
   >>> from twisted.internet.task import react
   >>>
   >>> def success(*args):
   ...     print(args)
   ...
   >>> def snmpget(reactor):
   ...     d = getCmd(< initialization code here >
   ...                ObjectType(ObjectIdentity('SNMPv2-MIB',
   ...                                          'sysDescr', 0)))
   ...     d.addCallback(success)
   ...     return d
   ...
   >>> react(snmpget)
   (0, 0, [ObjectType(ObjectIdentity('1.3.6.1.2.1.1.1.0'),
                      DisplayString('SunOS zeus.snmplabs.com'))])

Massively Twisted
=================

* Many SNMP operations run in parallel or sequentially
* Each *snmpget* call returns Deferred object
* Feed them all to Twisted and wait till all Deferreds
  are finished

.. class:: prettyprint lang-python

::

   >>> ...
   >>> reacct(DeferredList([snmpget(), snmpget(), snmpget()]))

asyncio
=======

* Twisted reinvented
* Relies on latest language features
* Based on coroutines and Future objects
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
* Queue to manage request rate

.. class:: prettyprint lang-python

::

   >>> ...
   >>> loop = asyncio.get_event_loop()
   >>> loop.run_until_complete(
   ...     asyncio.wait([snmpget(), snmpget(), snmpget()])
   ... )

More info on asyncio
====================

* Module documentation:
  https://docs.python.org/3/library/asyncio.html
* Ready to run PySNMP scripts:
  http://pysnmp.sf.net
* Repository of asyncio-compatible libraries:
  http://asyncio.org

SNMP Agent
==========

* Design: PySNMP engine + MIB modules expressed in Python
* User code lives in MIB modules
* Boilerplate MIB modules can be autogenerated
* PySNMP core can un/load MIB modules on the fly

PySNMP-based software
=====================

* A collection of command-line tools for system administration purposes
* SNMP simulator for SNMP products developers
* Proxy forwarder to secure SNMP operations over the Internet

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
* ...and by snooping SNMP traffic
* ...and by populating MIBs with values

More info: http://snmpsim.sf.net

Proxy forwarder
===============

* A network of SNMP manager and agent nodes
* Application-layer firewall / proxy
* Translates SNMP versions and network transports
* Filters / modifies SNMP messages based on various criterias
* Extendable through Python code snippets

More info: https://pypi.python.org/pypi/snmpfwd/

Summary
=======

* SNMP technology is old-fashioned but still relevant
* Used in system and network administration
* Might be picked up by Internet of Things
* PySNMP may be helpful for quick SNMP scripting
* ...or for SNMP-related research
* ...or to learn and experiment with SNMP! ;-)

Thank you!
==========

Questions?

Further reading
===============

* `SNMP, SNMPv2, SNMPv3, and RMON 1 and 2 <http://www.amazon.com/SNMP-SNMPv2-SNMPv3-RMON-Edition/dp/0201485346>`_
* `RFC3411 <https://www.ietf.org/rfc/rfc3411.txt>`_ - `RFC3418 <https://www.ietf.org/rfc/rfc3418.txt>`_
* `PySNMP documentation and example scripts <http://pysnmp.sf.net>`_
* `A Curious Course on Coroutines and Concurrency <http://www.dabeaz.com/coroutines/>`_
* `Python Async IO Resources <http://asyncio.org/>`_



