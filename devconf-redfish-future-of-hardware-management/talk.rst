
Redfish - future of hardware management
=======================================

*by Dmitry Tantsur and Ilya Etingof, Red Hat*

Why hardware management?
========================

Imagine you are sysadmin. It's late night, you are in your deep sleep.
Suddenly, you wake up - a shift engineer calls you notifying that company's
core application has become unresponsive.

You jump out of your bed, reach out for your computer, hop on the
company's network to realize that the system is down.

Desperate, you are trying to understand the problem when the phone
rings again. Uh, that's your boss. They are very concerned,
almost freaking out. So you got 10 more minutes to figure it out or...

What do you do next?

Hardware management to rescue
=============================

Luckily, you are a wise sysadmin! You have done your disaster recovery
homework. You got some form of hardware management at your disposal.

So you used it to get on remote console of the server to figure out that
it's a data corruption problem. So you went ahead booting server from
network, restoring the data and booting back to normal.

End of story.

The purpose of this is to show one of the cases when hardware management
makes sense.

Management of scale
===================

The other use case when hardware management can become a game changer is a
large-scale deployment e.g. the situation when you got to run a large farm
of servers perhaps at a DC.

A hardware management system capable to boot the servers, hook on the
console, update the firmware, monitor physical parameters etc. can
significantly improve data centre automation.

Keep in mind that a single company as large as Microsoft can have about
a million hardware servers in operation. When you have so many units,
they tend to come and go almost all the time.

This is where server automation may bring huge savings of all sorts.

How it works
============

Typically, the hardware management system is based on a small satellite
computer known as BMC (baseboard management controller). It is frequently
a SoC running alongside the main board. It has direct access to the parts
of the main system what allows it to power up/down the main system, change
BIOS settings etc.

The fact that it is an independent computer makes so-called out-of-band
access to the main system possible. Out-of-band here means that the
main system takes no part in the management operations. It can be up and
running or completely dead.

The BMC is running a software agent which acts as a frontend to all the
features of the management platform. This software agent implements a
protocol over which the clients can talk to the BMC.

What is Redfish
===============

This talk is about the Redfish protocol, however many others exist now
days or existed in the past.

The problem with so many standards is that you can't easily choose one.
More often than not, you are forced to support some of them to fully manage
your fleet.

It is anticipated, that the legacy protocols will be eventually phased
out in favour of the Redfish.

Before the Redfish
==================

The IPMI (Intelligent Platform Management Interface) is the direct
predecessor of the Redfish. It was designed 20 years ago to run on
the weak computers of the time.

Now days IPMI turned out to be difficult to deal with because of:

* it's hard to script with it
* does not scale up due to UDP transport
* not quite secure

Many advanced Redfish features first appeared in various proprietary
protocols designed by hardware vendors like HP, Dell, Intel and others
for their own products.

Even earlier
============

But it used to be worse in the past!

Before the BMC era, sysadmins used bulky, remotely controlled
keyboard-video-mouse switches, serial console servers (which aggregate the
consoles of the servers to a single, networked server).

For hard power-cycling people used remotely controlled circuit breakers.

Way less reliable in-band technologies were also used for emergency system
access. Such as VNC or RDS. The problem with the in-band access is that
it relies on the main system being in a reasonably good health what may
not be the case in case of emergency.

When it all started
===================

But it used to be even worse in the past!

In the early years of my career in computing, I carried out night
shifts at the DC. That involved sleeping on a folding bed between the
roaring racks hugging pager tightly...

Redfish design
==============

The Redfish protocol is quite new. It has been released as an official
standard of the Distributed Management Task Force organization in 2015.

To put it simple, Redfish is a web service exposing REST API communicating
JSON-serialized data.

It implements synchronous and asynchronous calls and it is designed for
future extensibility. That allows, for example, hardware vendors to
seamlessly support their proprietary features within the Redfish server.

Redfish benefits
================

From functionality standpoint, Redfish is not a groundbreaking development.

Its usability lies in its wide adoption in the future and the very well
understood technologies Redfish is based on. That makes it easy for
the the operators to integrate Redfish into their existing workflow
and tooling.

Redfish core components
=======================

Redfish models all manageable physical components of the computer. The models
are exposed through the REST API as resources. So models and resources are
roughly the same things.

Clients request operations to carry out on resources. The operations that
can be done in CRUD manner are mapped to HTTP methods.

Besides simple resource state changes, Redfish implements higher
level features, called Services, that also operate on resources,
but indirectly.

Redfish resources
=================

As the current core Redfish schema goes, a Redfish agent exposes Systems
branch where it has configuration, inventory and state information for all
the computers being managed.

At the DC, individual computers are normally mounted in the racks. Or blades
are mounted in an enclosure. The Chassis branch references all racks or
enclosures being managed, the inventory information, rack configuration and,
most importantly, it links-in the computers mounted in each rack by
referencing them in the Systems branch.

Finally, there is the Managers branch that exposes capabilities, state,
configuration and actions related to the BMC, enclosure manager,
rack e.g. the out-of-band management system being controlled by this
Redfish agent. As you might expect, the Managers branch references
the Systems and Chassis this Manager controls.

Redfish operations
==================

Redfish uses vanilla HTTP for many things. For example, if you want to
read current state of a resource, you just do HTTP GET. To create some
new configuration entity you will use HTTP PUT while changing a property
of a resource may be done though HTTP PATCH.

But HTTP methods only map well on idempotent operations. Sometimes
you may want to apply the same operation on a collection of resources, or
request a state change (such as system reboot) which is not idempotent and
which does not lead to immediate reflection on the resource state.

To accommodate such operations, Redfish has the concept of Actions.
With Actions you just notify Redfish what you need to do, not the
desired state of a specific resource. Examples include flipping
system power or rebooting the system.

Redfish services
================

The Redfish services is a collection of tools providing the features that
are not always directly relevant to hardware management.

When an otherwise normal operation is going to take more than a few seconds
to complete, Redfish agent may decide to run that operation asynchronously.
It then creates a task at the Task service and returns HTTP code
202 (Accepted) along with a link to that task. The client is expected to
poll that URL waiting for task to complete and eventually to receive
the response.

As a web service, Redfish supports basic user authentication as well as
sessions. Client can obtain an authentication token through the Sessions
service.

The user accounts used by clients talking to the Redfish agent are created
at the Redfish agent via the AccountService.

Some resources may need to communicate alerts or error conditions to the
clients at random times. To accommodate that need the EventService can
be used by clients to register the URL they will implement and listen at
for each Resource they are interested in.











