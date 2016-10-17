
Writing SNMP Apps in Python
---------------------------

*Ilya Etingof <ietingof@redhat.com>, October 2015*

The history of SNMP
-------------------

In the early days of networking, when computer networks were research
artifacts rather than a critical infrastructure used by 3 billion 
people, "network management" was an unheard of thing.  If one
encountered a network problem, one might run a few pings to locate the
source of the problem and then modify system settings, reboot hardware
or software, or call a remote colleague to do so.

A very interesting discussion of the first major "crash" of the
ARPAnet in 1980, long before network management tools were
available, and the efforts taken to recover from and understand the
crash can be read in RFC789.

As the public Internet and private intranets have grown from small
networks into a large global infrastructure, the need to more
systematically manage the huge number of hardware and software
components within these networks has grown more important as well.   

SNMP was quickly designed and deployed by a group of university network
researchers and users at a time when the need for
network management was becoming painfully clear. It was initially thought
as an interim solution to fill the need for network management
tool while a more theoretically sound system was being developed by
the ISO. Although that transition never occurred!

Since then, SNMP has evolved through three major versions and found 
widespread use and acceptance. Today, SNMP has emerged as the most
widely used and deployed network management framework.

The IETF recognizes SNMP version 3 as defined by RFC3411-RFC3418 (also
known as STD0062) as the current standard version of SNMP. The IETF
has designated SNMPv3 a full Internet standard, the highest maturity
level for an RFC. 

In practice, SNMP implementations often support multiple versions:
typically SNMPv1, SNMPv2c, and SNMPv3

Terminology
-----------

The network management field has its own specific terminology  for the
various components of a network management  architecture, and so we
adopt that terminology here. 

One of the pecularities of this terminology is that the word "management"
is greately overused. So bare with it.

There are three principle components of a network management architecture:
a managing entity, the managed devices, and a network management protocol.

TODO: Network management architecture

* The managing entity is an application, typically with a
  human-in-the-loop, running in a centralized network management
  station.  The managing entity is the central locus of activity for
  network management -  it controls the collection, processing,
  analysis, and/or display of network management information.  It is
  here that actions are initiated to control network behavior and here
  that  the human network administrator interacts with the network
  devices.

* A managed device is a piece of hardware or software that resides on
  a managed network.  It enumerates and formalizes some of its
  properties and states, important for healthy operation, thus making
  them available to the managing entity.

  A managed device might be a host, router, switch, printer, or any 
  other device.

  Finally, also resident in each managed device is a network management
  agent, a  process running in the managed device that communicates
  with the managing entity, taking local actions on the managed device
  under the command and control of the managing entity. 

* The third piece of a network management architecture is the network
  management protocol.  The protocol  runs between the managing entity
  and the managed devices, allowing the managing entity to query the
  status of managed devices and indirectly effect actions in these
  devices via its agents.  Agents can use the the network management
  protocol to inform the managing entity of exceptional events (e.g.,
  component failures or violation of  performance thresholds).

SNMP components
---------------

Contrary to what the name SNMP might suggest, network management in
the Internet is much more than just a protocol for moving management
data. Over time it has grown to be more complex than the word "simple"
might suggest. 

The Internet Network Management Framework consists of four parts:

* Definitions of network management objects known as MIB objects.  In
  the Internet network management framework, management information is
  represented as a collection of managed objects that together form a
  virtual information store, known as the Management Information Base
  (MIB).  A MIB object might be a counter, such as the number of IP
  datagrams discarded at a router due to errors in an IP datagram header
  or the number of carrier sense errors in an Ethernet interface,
  descriptive information such as the server software running on a DNS
  server;  status information such as whether a particular device is
  functioning correctly or not, or protocol-specific information such as
  a routing path to a destination.  MIB objects thus define the
  management information maintained by a managed node. Related MIB
  objects are gathered into so-called MIB modules.

* A data definition language, known as SMI (Structure of Management
  Information) that defines the data types, an object model, and rules
  for writing and revising management information;  MIB objects are
  specified in this data definition language. 

* A protocol, SNMP,  for conveying information and commands
  between a managing entity and an agent executing on behalf of that
  entity within a managed network device; 
  
* security and administration capabilities. The addition of these
  capabilities represents the major enhancement in SNMPv3 over SNMPv2.

The Internet network management architecture is thus modular by
design, with a protocol-independent data definition language
and a protocol.

Interestingly, this modular architecture was first put in place to
ease the transition from an SNMP-based network management to a network
management framework being developed by the ISO, the competing network
management architecture when SNMP was first conceived - a transition
that never occurred.

Over time, however, SNMP's design  modularity has allowed it to evolve
through three major revisions, with each of the four majors parts of
SNMP discussed above evolving independently.

SNMP support in Python
----------------------

Two schools of thought: Net-SNMP bindings and pure-Python.

Net-SNMP-based:

Pro: seriously fast, supports most of SNMP features
Con: not easily portable, may crash your Python, API is very limited

Pure-Python:

Pro: Pythonic, flexible, reliable
Con: slow

PySNMP implementation
---------------------

Pure-Python, open source and free.

Aims at full standards compliancy. Internal library structure is aligned
with abstract service interfaces as described in RFCs.

Implementation works with all reasonable Pythons (2.4-3.5) and supports
most of SNMP features.

This talk will continue drilling to the depths of SNMP technology
going hand-to-hand with references to PySNMP implementation. In hope
that would help understand the technology and prepare you to use
Python for your SNMP needs should that ever happen.

SNMP data model: base types
---------------------------

SMI introduces eleven base data types used for representing managed
objects states. They all are actually specialized ASN.1 INTEGER
and OCTET STRING types.

Most of the data types above will be familiar (or self-explanatory) to
most readers.

PySNMP relies on the PyASN1 package for modeling these SNMP types.
With PyASN1, instances of ASN.1 types are represented by Python
objects that look like either a string or an integer. 

We can convert PyASN1 objects into Python types and back. PyASN1
objects can participate in basic arethmetic operations (numbers)
or in operations with strings (concatination, subscrption etc).
All SNMP base types are immutable like their Python counterparts.

Users of PySNMP library may encounter PyASN1 classes and objects
when passing data to or receiving data from PySNMP.

In addition to these scalar types, SNMP defines a way to collect them
into ordered arrays. From these arrays 2-d tables could be built.

The one data type we will discuss in more detail shortly is the OBJECT
IDENTIFIER data type, which is used to name an object.  With this
system, objects are identified in a hierarchical manner. 

OIDs are widly used in computing for identifying objects. This system
can be depicted as a tree whose nodes are assigned by different
organizations, knowledge domains, types of concepts or objects,
concrete instances of objects. From human perspective, an OID is a
long sequence of numbers, coding the nodes, separated by dots.

Each 'branch' of this tree has a number and a name, and the complete
path from the top of the tree down to the point of interest forms the
name of that point. This complete path is the OID, the "identifier of
an object" respectively. Nodes near the top of the tree are of an
extremely general nature.

Top level MIB object IDs (OIDs) belong to different standard
organizations. Vendors define private branches including managed
objects for their own products.

At the top of the hierarchy are the International Organization for
Standardization (ISO)  and the Telecommunication Standardization
Sector of the International Telecommunication Union (ITU-T), the two
main standards organizations dealing with ASN.1, as well as a brach
for joint efforts by these two organizations.

Under the Internet branch of the tree (1.3.6.1), there are seven
categories. Under the private (1.3.6.1.4) branch, we will find a list
of the names and private enterprise codes for huge number of companies
that have registered with the IANA.  Under the management (1.3.6.1.2)
and MIB-2 branch (1.3.6.1.2.1) of the object identifier tree, we find
the definitions of the standardized MIB modules. This is there most of
SNMP-related identifiers are located.

In PyASN1 model, OID looks like an immutable sequence of numbers.
Like it is with Python tuples, PyASN1 OID objects can be concatinated
or split apart. Subscription operation returns a numeric sub-OID.

OIDs are widly used in SNMP for various identification purposes.

Collection of management information: MIB
-----------------------------------------

MIB can be thought of as a virtual information store, holding
managed objects whose values collectively reflect the current "state"
of the system.

These values may be queried, modified by or reported
to a managing entity by sending SNMP messages to the agent that is
executing in a managed node.

For example, the typical objects to monitor on a printer are the
different cartridge states and maybe the number of printed files, and
on a switch the typical objects of interest are the incoming and
outgoing traffic as well as the rate of package loss or the number of
packets addressed to a broadcast address.

MIB objects are identified by unique OIDs. To link MIB object value
with MIB object ID a few higher level constructs are introduced by
SMI.

MIBs are collections of definitions which define the properties of the
managed object within the device to be managed. 

Every managed device keeps a database of values for each of the
definitions written in the MIB. So, the available data is actually not
dependent on the database, but on the implementation.

Each vendor of SNMP equipment has their proper section of the MIB tree
structure at their disposition.

To organize all of these properly, all the manageable features
of all products (from each vendor) are arranged in this MIB
tree structure. 

There are above 10,000 defined objects in various Internet RFC's.

In the first 5000 RFCs produces by IETF, 318 RFC contain MIBs. But
that is a mere fraction of the MIBs that have been written. At
http://mibs.snmmplabs.com/asn1/ you could find a collection of 9000+
MIB modules.

SNMP support in Python
----------------------

Higher-level SMI constructs
---------------------------

TODO: OBJECT-TYPE construct

The OBJECT-TYPE construct is used to specify the data type, status,
and semantics of a managed object. Collectively, these managed objects
contain the management data that lies at the heart of network
management.

The OBJECT-TYPE construct has four clauses. The SYNTAX clause of an
OBJECT-TYPE definition specifies the basic data type associated with
the object. The MAX-ACCESS clause specifies whether the managed object
can be read, be written, be created, or have its value included in a
notification.  The STATUS clause indicates whether object definition
is current and valid, obsolete or deprecated.  The DESCRIPTION clause
contains a human-readable textual definition of the object; this
"documents" the purpose of the managed object and should provide all
the semantic information needed to implement the managed object.

Instanced of OBJECT-TYPE is most visible and frequently encountered
human interface to SNMP. Classical example of SNMP query performed
from a UNIX box looks like this:

TODO: What's uptime?

The NOTIFICATION-TYPE construct is used to specify information
regarding "SNMPv2-Trap" and "InformationRequest" messages generated by
an agent, or a managing entity.  Compared to OBJECT-TYPE, this
constract refers not to a single SYNTAX value representing object
state, but to the values of other OBJECT-TYPE's present on the
system. This is done through OBJECTS clause.

The MODULE-IDENTITY  construct allows related objects to grouped
together within a "module". 

The MODULE-COMPLIANCE construct defines the set of managed objects within
a module that an agent must implement.

The AGENT-CAPABILITIES construct specifies the capabilities of agents
with respect to object and event notification definitions.

Well-known MIBs
---------------

There are a large number of MIBs defined by both standards
organizations like the IETF, private enterprises and other entities.

The internet subtree branches into management and private. All the standard
MIBs are under management, while the private MIBs are under the
private.enterprises subtree.

TODO: Kinds of MIBs

Speaking of basic, standard MIBs - under the ...management.MIB-2
branch (1.3.6.1.2.1) of the object identifier tree, we find the
definitions of the standardized MIB modules. The next slide shows some
of the important OS-oriented MIB modules (system and interface) as
well as modules associated with some of the most important Internet
protocols.

TODO: Standard MIBs

The managed objects falling under system contain general information
about the device being managed; all managed devices must support the
system MIB objects. 

< slide on system subtree >

Object Identifier    Name    Type    Description (from RFC 1213)

1.3.6.1.2.1.1.1  sysDescr    OCTET STRING    "full name and version
   identification of the system's hardware type, software
   operating-system, and networking software"

1.3.6.1.2.1.1.2  sysObjectID OBJECT IDENTIFIER   Vendor assigned
   object ID that "provides an easy and unambiguous means for
   determining `what kind of box' is being managed."

1.3.6.1.2.1.1.3  sysUpTime   TimeTicks   "The time (in hundredths
   of a second) since the network management portion of the system was
   last re-initialized."

1.3.6.1.2.1.1.4  sysContact  OCTET STRING    "The contact person
   for this managed node, together with information on how to contact
           this person."

1.3.6.1.2.1.1.5  sysName OCTET STRING    "An
           administratively-assigned name for this managed node.  By
           convention, this is the node's fully-qualified domain name"

1.3.6.1.2.1.1.6 sysLocation OCTET STRING    "The physical
            location of this node."

1.3.6.1.2.1.1.7 sysServices Integer32   A coded value that
            indicates the set of services available at this node:
            physical (e.g., a repeater), datalinkl/subnet (e.g.,
            bridge), internet (e.g., IP gateway), end-end (e.g.,
            host), applications.

< slide on UDP MIB subtree >

UDP protocol at a managed entity. 

Object Identifier    Name    Type    Description (from RFC 2013)

1.3.6.1.2.1.7.1  udpInDatagrams  Counter32   "total number of UDP
   datagrams delivered to UDP users"

1.3.6.1.2.1.7.2  udpNoPorts  Counter32   "total number of received
   UDP datagrams for which there was no application at the destination
   port"

1.3.6.1.2.1.7.3  udpInErrors Counter32   "number of received UDP
   datagrams that could not be delivered for reasons other than the
   lack of an application at the destination port"

1.3.6.1.2.1.7.4  udpOutDatagrams Counter32   "total number of UDP
   datagrams sent from this entity"

1.3.6.1.2.1.7.5  udpTable    SEQUENCE of UdpEntry    a sequence of
   UdpEntry objects, one for each port that is currently open by an
   application, giving the IP address and the port number used by
   application

SNMP protocol design
--------------------

The protocol part of SNMP is used to convey MIB information that has
been specified in the SMI among managing entities and agents executing
on behalf of managing entities.

TODO: SNMP protocol

The most common usage of SNMP is in a request-response mode -  an SNMP
managing entity sends a request to an SNMP agent, who receives the
request, performs some action and sends a reply to the request.
Typically, a request will be used to retrieve or modify MIB object
values associated with a managed device.

A second common usage of SNMP is for an agent to send an unsolicited
message, known as a trap message, to a managing entity. Trap messages
are used to notify a managing entity of an exceptional situation that
has resulted in changes to MIB object values. Network administrator
might want to receive a trap message, for example, when an interface
goes down, congestion reaches a predefined level on a link, or some
other noteworthy event occurs. 

Note that there are a number of important tradeoffs between polling
(request-response interaction) and trapping.

TODO: SNMP PDU types

SNMPv2 defines seven types of messages, known generically as Protocol
Data Units - PDUs.

The GetRequest, GetNextRequest, and GetBulkRequest PDUs are all sent
from a managing entity to an agent to request the value of one or more
MIB objects at the agent's managed device. The object identifiers of
the MIB objects whose values are being requested are specified in the
variable binding portion of the PDU.  

GetRequest, GetNextRequest, and GetBulkRequest differ in the
granularity of their data requests. GetRequest can request an
arbitrary set of MIB values; multiple GetNextRequests can be used to
sequence through a list or table of MIB objects; GetBulkRequest allows
a large block of data to be returned, avoiding the overhead  incurred
if multiple GetRequest or GetNextRequest messages were to be sent.  In
all three cases, the agent responds  with a Response PDU containing
the object identifiers and their associated values.

The SetRequest PDU is used by a managing entity to set the value of
one or more MIB objects in a managed device. An agent replies with a
Response PDU with the 'noError' Error Status to confirm that the value
has indeed been set.

The InformRequest PDU is used by a managing entity to notify another
managing entity of  MIB information that is  remote to the receiving
entity.  The receiving entity replies with a Response PDU with the
'noError' Error Status to acknowledge receipt of the InformRequest
PDU.

Given the request-response nature of SNMPv2, it is worth noting here
that although SNMP PDU's can be carried via many different transport
protocols, the SNMP PDU is typically carried in the payload of  a UDP
datagram.  Since UDP is an unreliable transport protocol,
there is no guarantee that a request, or its response will be received
at the intended destination.  The Request ID field of the PDU is used
by the managing entity to number its requests to an agent; an agent's
response takes its Request ID from that of the received request.
Thus, the Request ID field can be used by the managing entity to
detect lost requests or replies. It is up to the managing entity to
decide whether to retransmit a request if no corresponding response is
received after a given amount of time.

The final type of SNMPv2 PDU is the trap message.  Trap message are
generated asynchronously, i.e., not in response to a received request
but rather in response to an event for which the managing entity
requires notification. A received trap request has no required response
from a managing entity.

SNMP applications
-----------------
  
The so-called SNMP applications consist of a command generator,
notification receiver and proxy forwarder (all of which are typically
found in a managing entity); a command responder and notification
originator (both of which are typically found in an agent); and the
possibility of other applications.

TODO: SNMP Applications

The command generator generates the GetRequest, GetNextRequest,
GetBulkRequest and SetRequest PDUs and handles the received responses
to these PDUs.  The command responder executes in an agent and
receives, processes and replies (using the Response message) to
received GetRequest, GetNextRequest, GetBulkRequest and SetRequest
PDUs.

The notification originator application in an agent generates Trap
PDUs; these PDUs are eventually received an processed in a
notification receiver application at a managing entity.  The proxy
forwarder application forwards request, notification, and response
PDUs.

PySNMP fully implements all these Standard SNMP applications within
pysnmp.rfc3413 sub-package and also offers high-level API to some
of them. That high-level API wraps and isolates the details making
it much easier for user to perform most common SNMP operations.
Since most frequently people send SNMP queries to fetch data or
deliver a notification, high-level API is currently provided only
for "client-side" roles of these applications.

TODO: Snmp Apps at PySNMP

SNMP engine
-----------

A PDU sent by an SNMP application next passes through the SNMP
"engine" before it is sent via the appropriate transport protocol.

TODO: SNMP engine

Next slide shows how a PDU generated by the command generator
application first enters the dispatch module, where the SNMP version
is determined.  The PDU is then processed in the message processing
system, where the PDU is wrapped in a message header containing the
SNMP version number, a message ID and message size information.  If
encryption or authentication is needed then the appropriate header
fields for this information is included as well.
Finally, the SNMP message (the application-generated PDU
plus the message header information) is passed to the appropriate
transport protocol.

Configuration store
-------------------

An SNMP entity retains all configuration information in a Local
Configuration Datastore (LCD). Interestingly, LCD is defined and
implemented as a collection of managed objects. In other words
all SNMP engine configuration and controls appear like a dedicated
managed entity.

One of the consequences of this design is that SNMP engine can be
entirely manipulated and configured remotely, via SNMP.  Even shared
secret keys can be changed in a secure way at a newly configured SNMP
engine.

For instance, the following slide shows command-line SNMP manager
querying SNMP engine LCD for accumulated operational statistics.

TODO: Configuration

PySNMP design
=============

In PySNMP, SnmpEngine class is an umbrella object gathering together
all SNMP engine components shown on the slide. Besides that, it
carries SNMP engine identification (SNMP Engine ID), that is used
on the protocol level, and is the only stateful object in the system.

TODO: PySNMP design

There can be many SnmpEngine objects (thus many running SNMP Engines)
in PySNMP application.

TODO: PySNMP Engine

Protocol security
-----------------

SNMP messages are used to not just to monitor, but also to control (e.g.,
through the SetRequest command) network elements.  Clearly, an
intruder that could intercept SNMP messages and/or generate its own
SNMP packets into the management infrastructure could wreak havoc in
the network. Thus, it is crucial that SNMP messages be transmitted
securely.

Surprisingly, it is only in SNMP version 3 that security has received
the attention that it deserves. As of SNMP v1 and v2c versions,
no data authentication or encruption is provided. The only real protection
against unauthorized access would be to firewall SNMP traffic. The
only parties identification mechanism that exists in those SNMP
versions is so-call Community Name - atbitrary string grouping
together a set of SNMP entities probably under some common
administration. People tended to think of Community name as a extermely
weak security measure, but it is not the case.

PySNMP uses CommunityName class to bring SNMP community name into
SNMP engine configuration.

TODO: Community Name

SNMPv3 provides for encryption, authentication, protection against
playback attacks, and access control. SNMPv3 security is known as
user-based security in that there is the traditional concept of a
user, identified by a user name, with which security information such
as a password, key value, or access privileges are associated.

TODO: USM user name

* Authentication. SNMP combines the use of a hash function, such as
the MD5 or SHA algorithms, with a secret key value
to provide both authentication and protection against tampering.  The
approach, known as HMAC (Hashed Message Authentication Codes)

* Encryption.  SNMP PDUs can be encrypted  using the DES, 3DES and AES
algorithms in cipher block chaining mode. Note that SNMP is designed
to use a shared key encryption system, so the secret key of the user
encrypting data must be known at the receiving entity that must decrypt
the data.

PySNMP supports practically all authentication and encryption
algorithms standartized for SNMP to the moment.

User name, authentication and encryption keys and algorithms
selection are conveyed to PySNMP engine via the UsmUserData object.
Of course algorithms to use are identified with OIDs.

TODO: USM crypto

* Protection against playback.  In the SNMP scenario, the message
receiver wants to insure that a received message is not a replay of
some earlier message.  In order to assure this, the receiver requires
that the sender include a value in each message that is based on a
counter in the receiver. This counter, which functions as a nonce,
reflects the amount of time since the last reboot of the receiver's
network management software and the total number of reboots since the
receiver's network management software was last configured.  As  long
as the counter in a received message is within some margin of error
from the receiver's actual value, the message is accepted as a
non-replay message, at which point is may be authenticated and/or
decrypted. 

* Access control. SNMPv3 provides a view based access control 
which controls which network management information can be
queried and/or set by which users.

Putting it all together
-----------------------

We will devote more attention to client-side operations, as they are
generally more frequent and supported by high level API. We start with
the most intuitive synchronous interface.

To fire up SNMP query several components would be needed. First we
should decide on what SNMP command we wish to execute. Mind you,
our options here include GET, SET, GETNEXT and GETBULK. Let's pick
GET as most straightforward.

TODO: Putting it all together

Then we need to chose SNMP version. That mostly depends on your SNMP
agent capabilities. Let's assume it talks SNMP v2, which is probably
still most common.

TODO: Choose SNMP version

Next is network transport address of SNMP agent we are going to
query. Network address format and properties depend on communication
technology being used. SNMP can use many different transports:

We will use UDP-over-IPv4 as most widly used.

TODO: Choose transport and destination

There is another SNMP option we have not touched so far and it is SNMP
context. The idea is that a single SNMP engine can potentially serve
many instances of identical MIBs. In that case there will be multiple
MIB objects with exactly the same overlapping OID namespace. To
resolve that conflict SNMP introduces the concept of "context".
That can be thought of as an additional identifier that goes along with 
OIDs in SNMP query.

Let us use default "empty" context here:

Finally, we want to request specific MIB object. The most intuittive way
is probably this:

TODO: SNMP context

Here we request a symbol as defined in a MIB. Besides symbol name we also
speficy so-called managed object instance by adding '0' in symbol reference
(more on that in a moment). Many MIB objects can be passed to SNMP query
in this fashion.

This call will build an SNMP packet and send it over UDP/IPv4 to SNMP
agent at demo.snmplabs.com.  Once response is received, getCmd call
returns a sequence containing error indications (if occurred) and
the current value of requested MIB object(s).

TODO: Iterate!

MIB object
----------

As we already know, MIB objects are enumerated with OIDs. 

Thus, to address MIB object, PySNMP users are expected to utilize
ObjectIdentity class that represents MIB object identification.
At the protocol level, MIB objects are identified by OID. However
for humans, MIB objects are more convenient to deal with when
addressing them by name.

TODO: More on MIB objects

To catch that duality of MIB objects, PySNMP introduces the
ObjectIdentity class. It works like an immutable object - once you
instantiate it, its value can't be changed anymore.

The primary way is to refer to MIB and symbol.

TODO: ObjectIdentity

Alternatively, full OID associated with given MIB object could be
given in form of string or tuple of numbers.

Upon instantiation, ObjectIdentity holds only a single MIB
object representation - either MODULE::symbol or OID. In that state
MibIdentifier is not particulary useful. To enrich it with the other,
initially missing, MIB object identification information, PySNMP
searchies through a MIB. Once the complimentary identification
information is found, MibIdentity object is fully usable.

< slide on .resolveWithMib() call >

This MIB object ID resolution is performed automatically, user is not
required to participate in it.

MIB object instance
-------------------

One key aspect of MIBs is that, only the types of objects on the
managed device are specified by the MIB and not the specific objects
(or instances).

For example, ifInOctets in IF-MIB specifies a type of object, for
number of input octets on an interface, but the specific objects or
instances of that type are specified as ifInOctets.1, ifInOctets.2,
etc., depending on the number of interfaces. 

TODO: MIB object instance

To obtain values of objects from the agent, you need to specify the
instance of the object. Appending an instance index to the object
identifier specifies the instance of an object. 

For example, the last 0 in:

   .iso.3.dod.1.mgmt.mib.1.sysUpTime.0

TODO: ObjectIdentity for scalars

is the instance index. An instance index of "0" (zero) specifies
the first instance, "1" specifies the second instance, and so on.

Since sysUpTime is a scalar object, it has only one instance.
Therefore, an instance index of zero is always specified when
retrieving the value of a scalar object.

When instance index is not properly specified, the agent responds with
a "No such instance" error.

An instance index higher than 0 can only be used in the case of
columnar objects (in table), which can have multiple instances.
Tabular objects define multiple related object instances that are
grouped in MIB tables.

To make tabular objects indices more human friendly, SNMP defines
rules for OID conversion to/from integer or string values. More
generally, conversion rules exist for all SNMP types. The conversion
process is defined by two SMI constructs: TEXTUAL-CONVENTION and
OBJECT-TYPE INDEX clause.

Consider it a way that all of the interfaces at a computer or router
are broken down and assigned a value. If any information needs to be
polled for that particular interface, it must use that interface
number value.  So this is like a primary key of all objects related to
the same entity.

TODO: SNMP tables

The DISPLAY-HINT clause sets the rules for OID mapping to
human-friendly representation and back. In this case any single
integer number, representing interface number, is mapped to a single
sub-OID. More complex mappings exist for strings and IP addresses.

For any MIB, a quick way to tell what index organizes a table is to look
at the table entry:

TODO: Composite indices

In this case the value of ifIndex columnar MIB object will be
converted to all other OIDs in ifEntry table that are related to
particular interface.

For example, the other column in this table is ifName. To address
isName MIB object for the first interface you'd use ifName.1.

This conceptual table concept is fully captured by ObjectIdentity
class.

MIB object value and type
-------------------------

MIB objects sometimes call MIB variables for a good reason - like
normal variables, MIB objects have a name (OID) and a value of certain
type. So far we have only talked about MIB object identification. Now,
the value part.

Syntaxically, value type is chosen by MIB designed to best represent
phisical or logical properties of the object being managed. Once type
is chosen (from a collection of SNMP types), it goes to OBJECT-TYPE's
SYNTAX clause.

< slide on OBJECT-TYPE >

As we know, MIBs never hold values of the objects. Rather they
enumerate MIB objects (assigning them OIDs) and specify what kind of
value each MIB object can communicate to the outer world. You can
think of MIB as a database schema rather than a database snapshot.

To capture the concept of MIB object value type, PySNMP offers the
ObjectType class. It is designed as a container class which holds two
items: instance of ObjectIdentity and instance of one of SNMP base
type.

TODO: ObjectType class

This layout is designed after a concept of variable-binding used in
SNMP PDU. Naturally, instances of ObjectType act like a two-component
tuple.

ObjectType is normally initialized with at least ObjectIdentity instance.
Until MIB lookup is performed, type information for this MIB object is
not known. However some value could also be passed to ObjectType
constructor. As soon as MIB object type becomes known, passed value
will be casted into appropriate type. If value is not given, it
defaults to SNMP NULL value.

< slide on ObjectType + value initializer >

The rest of interface and behaviour is very similar to ObjectIdentity.

Using SNMPv3
------------

Enough for MIB stuff for the moment! Though, we will get to it later
when we will be talking about SNMP notifications.

The introduction of SNMP v3 framework and User Security Model for
provisioning authencity and confidenciality, made the protocol part
way more complex and secure.

However, with PySNMP's high-level API, all complications are well
hidden under the hood. All you need to do when configuring USM is to
pass properly initialized UsmUserData object to PySNMP engine.

To use SNMP v3 without any authentication and ciphering, just omit
authentication and encryption keys on UsmUserData instantiation:

< slide on UsmUserData initialization >

Likewise, to enable HMAC MD5-based message authentication, just add
shared key. Finally, to employ both authentication and DES-based
encryption - supply both keys.

SNMP standardize several hashing and encryption algorithms to use with
USM. You can tackle those by passing appropriate constants to
UsmUserData.

TODO: Crypto algorithms selection

Like it goes for many things in SNMP, algorithms identifiers are
OIDs.

Despite simple appearance at the API level, USM is a rather "heavy"
stuff. Once used for SNMP message communication, it invokes SNMP
remote engine ID discovery, inter-SNMP engines time synchronization 
procedures followed by actual packet signing and/or ciphering.

Error handling
--------------

With all PySNMP calls, errors are communicated to user by two variables:

< slide on errors >

* If errorIndication object evaluates to True, that indicates SNMP engine
level valure. Just printing it out like a string reveals the exact cause.
Examples: request timeout, encryption problems.
* If errorStatus is non-zero, that indicates a problem with PDU processing.
Accompanying errorIndex refers to MIB object in request that caused
this error.  Unlike errorIndication, there is a finite, standartized
set of possible errorStatus values.  Examples: MIB access denial,
inconsistent data in request, bad value type.

Fatal, non-standartized errors may cause PySnmpError exception.

Fetching MIB data
-----------------

Now we are well prepared for using full power of SNMP. On the
following few slides we will discover many variations of how MIB
values could be fetched from SNMP agent.

These examples will be based on the same call of PySNMP high-level
API, differences will be in the details.

High-level, synchronous PySNMP API is designed around the idea of
iterating a generator object. One way of using it is to create a
generator with some fixed parameters (including MIB object to work
with), then, on each iteration, SNMP query is performed and result
returned.

TODO: Synchronous, high-level API

Generator will exhaust whenever no more relevant MIB objects remains
or if error occurs.

It is also possible to pass new MIB object to query to running Python
generator. That prevents generator to exhaust immediately, instead
it goes on and makes another SNMP query.

TODO: Feeding generator object

GET MIB variable by OID
-----------------------

Normally, humans prefer using symbols when referring to MIB objects.
However, if you do not have a MIB, but somehow figured MIB object OID,
you could use it right away.

< slide on GET for OID >

GET many unrelated MIB objects
------------------------------

SNMP PDU can carry around many variable-bindings. There is no hard
limit on that (it's actually set to 2^31 in the standard but that's
more of a joke). So the practical limit is imposed by maximum datagram
size that parties can exchange and agent resources required for
collecting information for all requested MIB variables.

TODO: Unrelated MIB objects

GET table object by composite index
-----------------------------------

If you remember our discussion in regards to SNMP table design and
addressing, this is a real-life example. Here we fetch MIB object that
resides in SNMP table that has four-component index! This is a table
of TCP/IP connections. As we all know, TCP/IP connection is defined by
a pair of IP addresses, belonging to each of the peers, and a pair of
TCP port numbers. The TCP-MIB::tcpConnTable captures that by indexing
all its rows by a composite index

TODO: Fetch table element

To address this MIB object in PySNMP, we will initialize
ObjectIdentity with all those components as its index.

Fetching a series of MIB objects
---------------------------------

SNMP tables can be very dynamic. Agent may add or move entire rows at
any moment. Imagine SNMP table representing TCP/IP connections - those
connections can appear and disappear very frequently and SNMP manager
has no way to predict that.

To handle such cases SNMP offers GETNEXT operation. When using it,
SNMP manager does not ask for specific MIB object. Instead it asks
agent to send it the object that is "next" to the given one. Here
adjucency is defined as if in a sorted list of OIDs that enumerate MIB
objects.

TODO: Fetch a sequence of MIB objects

Manager can even fetch the whole collection of MIB objects implemented by
an agent by iterating over it with the GETNEXT command.

TODO: Sequence of MIB objects

Getting MIB objects in bulk
---------------------------

To save on packet roundtrip delays and processing overhead, SNMP
defines GETBULK command. It works as a combination of GET and GETNEXT,
but addionally it can fetch many MIB objects that follow the given one.

TODO: Fetching MIB objects in bulk

To distinguish on what MIB objects GET should be performed from
those that need GETNEXT treatment, the GETBULK command includes
non-repeaters parameter - it indicates at what position in input list
of MIB objects GETNEXT ones start. For MIB objects before
non-repeaters, agent will respond with just a single value. For
others, many subsequent MIB objects followed the given one will be
returned.

The upper limit for how many MIB objects will be fetched in a single
GETBULK is defined by max-repetitions parameter.

< slide on a non-repeaters > 0 >

Modifying MIB objects
---------------------

As you might remember from the first parts of this talk, SNMP was
designed with configuration facilities in mind. So it offers the SET
command that basically commits new value to the MIB object specified.

It is ObjectType class that takes new value on input, figures out what
SNMP type is associated with given MIB object, and coerces one into
the other.

TODO: SET operation

In cases when MIB is unavailable, you can still do SNMP SET by
using both MIB object OID and SNMP type.

It's worth noting that while SET operation looks simple, it is not. As
it is defined in SNMP RFCs, MIB objects modified by a single SNMP
query must be modified transactionally meaning either all or none.
That's the responsibility of SNMP agent.

Since concurrent MIB object modification is not impossible, SMI
defines certain locking mechanism to prevent data corruption. For
this locking to work when modifying MIB objects, managers must behave
collaboratively by following specific MIB object modification rules as
described in MIBs.

SNMP notifications
------------------

The idea behind SNMP notification is that if a manager is responsible
for a large number of devices, and each device has a large number of
objects, it is impractical for the manager to poll or request
information from every object on every device.

The solution is for each agent on the managed device to notify the
manager without solicitation. It does this by sending a message known
as a trap of the event.

After the manager receives the event, the manager displays it and can
choose to take an action based on the event. For instance, the manager
can poll the agent directly, or poll other associated device agents to
get a better understanding of the event.

The use of notification can result in substantial savings of network
and agent resources by eliminating the need for massive SNMP
requests. However, it is not possible to totally eliminate SNMP
polling. SNMP requests are required for discovery and topology
changes. In addition, a managed device agent can not send a trap, if
the device has had a catastrophic outage.

TODO: SNMP notifications

Contents of notification
------------------------

SNMP notification are identified by an OID. In order for a management 
system to understand a trap sent to it by an agent, the management
system must know what the OID defines.

To describe notifications SMI prescribes using NOTIFICATION-TYPE constuct
in MIBs. The NOTIFICATION-TYPE basically defines unique OID for this
kind of notification and lists additional MIB objects that should
accompany this particular notification.

TODO: NOTIFICATION-TYPE

Objects that are transmitted with the notifications contain additional
information about the reported event. 

For example, in the OBJECTS section the following three varbinds have
been specified: ifIndex, ifAdminStatus, and ifOperStatus. Therefore,
ifIndex is the first varbind to be encoded, ifAdminStatus is the
second, and ifOperStatus is encoded third. Checking the IF-MIB we find
that the ifIndex object type is defined as InterfaceIndex which is a
TEXTUAL-CONVENTION that resolves into Integer32 type.

Therefore, when the PDU arrives to the manager, the first varbind will
be an integer. To determine what that integer means, manager must
reference the IF-MIB module, look up ifIndex, and read the associated
object information.

In PySNMP we use NotificationType object for forming proper notifications.
Like ObjectType, NotificationType object is a container referencing
ObjectIdentity instance that identifies the trap.

TODO: NotificationType class

Since a single NOTIFICATION-TYPE can resolve into a sequence of
var-binds, the fully initialized NotificationType object behaves like
a sequence of ObjectType instances.

Filling in OBJECTS
------------------

When SNMP agent prepare MIB objects to put into PDU, it looks up the
collection of MIB objects it serves and pulls those that are required
for this particular notification.

More often than not, we want to build SNMP notification from scratch,
e.g. using MIB values we know in advance rather than running a
full-blown SNMP agent with its own set of MIB objects. To build SNMP
trap from the scratch, NotificationType constructor accepts a
dictionary of OIDs those values will be pulled in when building
a sequence of OBJECTS.

< slide on objects >

Another twist is that in NOTIFICATION-TYPE you specify MIB objects.
to resolve them into MIB objects instances, the instanceIndex parameter
is used.

Generating notifications
------------------------

We will be using synchronous high-level API for simplicity. Sending
SNMP notification is not that different compared to sending SNMP
command. 

TODO: Sending notification

The difference is in how variable-bindings are generated and
provisioned.


Besides trap notification, SNMP also defines Information Request
operation that was initially thought to be used for manager-to-manager
communication, but later on that was reconsidered to allow
agent-to-manager communication in form of INFORMs.

In PySNMP TRAP and INFORM generation works very similar, most
prominent difference is the notifyType parameter.

Asynchronous I/O
----------------

Large intranets may run thousands of hosts, routers and other
equipment. Monitoring them would require quite intensive SNMP
communication. If we'd do that in sequential fashion, e.g. waiting for
previous operation to complete prior to initiating the next one, the
polling period could grow to unacceptable lengths.

A way to improve things in that regard is to skip waiting for response
to arrive but send a bunch of SNMP queries at once. This way of making
I/O-bound applications highly efficient is very popular in software
design.

The basic idea behind asynchronous I/O is very simple.
Essentially it is the idea that the program can do something else
while it is waiting for I/O to complete. That is unlike the normal
operation, where doing an I/O blocks the program. There have been lots of
approaches to asynchronous I/O over the years, including
interrupts, threads, callbacks, and events.

Threads are well-understood, and programmers can still write
synchronous code because a thread will just block when waiting for
I/O, but the other threads will still run. However, threads have their
limits, and OS threads are somewhat costly. A program with ten threads
is fine, but 100 threads may start to cause some worry. Once you get
up to 1000 threads, you are "already in trouble".

The way to do asynchronous I/O without threads is by using select()
and poll(), which is the mechanism that most I/O framework use.

The event loop is special because it serializes the execution of the
program. It guarantees that while your code is running, nothing else
is, and that the shared state cannot be changed until "you say you are
done with it"

There are lots of Python and C implementations of async frameworks.
Most prominent are Twisted, Tornado, ZeroMQ, gevent.

Asynchronous I/O

As of this talk, PySNMP supports three of them: asyncore, twisted and
asyncio/trollius.

Let's investigate them briefly!

XXX need image

asyncore
--------

The asyncore module is one of the first asynchronous I/O library
designed for Python under the name of Medusa. It is present in
standard library for a long time, that is the main reason why it is
used as a default I/O infrastructure in PySNMP.

However asyncore is showing its age, it isn't very extensible, and
most people ignore it entirely and write their own asynchronous code
using select() and poll().

TODO: asyncore

Callables must comply certain calling signature. That is the way how
query results are delivered to the application.

You could run different SNMP operations with different Agents using
different SNMP versions.

< asyncore to multiple agents and different versions >

Twisted
-------

Twisted is one of the earliest and hugely popular asynchronous I/O
framework.  With Twisted, your code will mostly live in isolated
functions, but unlike as it is with callback-based design, with
Twisted work-in-progress is represented by a Deferred class instance
effectively carrying state and context of running operation. Your
callback functions will be attached to these Deferred objects and
invoked as Deferred is done.

TODO: GET with Twisted

Based on Twisted infrastructure, individual asynchronous functions
could be chained to run sequentially or in parallel.

asyncio
-------

The asyncio module first appeared in standard library since Python 3.3
(on provisional basis). Its main design feature is that it makes
asynchronous code looking like synchronous one thus eliminating the
"callback hell".

With asyncio built-in facilities, you could run many SNMP queries in
parallel and/or sequentially, interleave SNMP queries with I/O
operations with other systems. 

That asyncio is a new big thing. There is a repository of
asyncio-compatible libraries at http://asyncio.org

TODO: GET with asyncio

