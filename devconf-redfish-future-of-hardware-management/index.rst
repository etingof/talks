
Redfish - future of hardware management
=======================================

*by Dmitry Tantsur and Ilya Etingof, Red Hat*

Why hardware management?
========================

Late night, you are in your bed:

* 4:00am - SMS alert: core app is down
* 4:05am - ping works but ssh does not work
* 4:10am - your boss gives you 15 more minutes...

What do you do now?

Immediate response
==================

* Reboot the machine
* Change boot device
* Get the console

Management of scale
===================

* Large fleet of servers
* Mass deployment
* Frequent re-purposing
* Automation

How it works
============

* An independent satellite computer (BMC)
* Out-of-band access to the main system
* Many protocols, standard and proprietary

What is Redfish
===============

* The new standard to rule them all
* Based on well-understood technologies
* Extensible

Before the Redfish
==================

* IPMI (Intelligent Platform Management Interface)
* ILOM (Integrated Lights Out Manager)
* iDRAC (Integrated Dell Remote Access Controller)
* IAMT (Intel Active Management Technology)

Even earlier
============

* Remote KVM switches
* Console servers
* Circuit breakers
* In-band remote access: VNC, RDS

When it all started
===================

* Night shifts at the DC

Redfish design
==============

* REST API service
* Rigid JSON schema
* A/synchronous operation
* Extensibility

Redfish benefits
================

* Human readable and self documented
* Tools readily available
* Language independent
* Easy automation

Redfish design components
=========================

* Resources
* Operations (HTTP CRUD & Actions)
* Services

Redfish resources
=================

* Systems (server, CPU, memory, devices, etc.)
* Managers (BMC, Enclosure Manager, etc.)
* Chassis (Racks, Enclosures, Blades, etc.)

Redfish operations
==================

* Operate on resources
* HTTP CRUD
* Redfish Actions (e.g. power cycle)

Redfish services
================

* Tasks (jobs executed against resources)
* Sessions (related operations executed against a resource)
* AccountService (service for creating users)
* EventService (service for pushing events to subscribers)

Example: list servers
=====================

* Possibly live example

Example: power-on server
========================

* Possibly live example

Redfish OEM extensions
======================


Swordfish: storage extension
============================

