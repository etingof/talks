
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

Hardware management to rescue
=============================

* Reboot the machine
* Change boot device
* Get the console

Management of scale
===================

* Large fleet of servers
* Automation
* Mass deployment
* Frequent re-purposing

How it works
============

* An independent satellite computer (BMC, Enclosure manager)
* Out-of-band access to the main system
* Many protocols, standard and proprietary

What is Redfish
===============

* The new standard to rule them all
* Based on well-understood technologies
* Highly extensible

Before the Redfish
==================

* IPMI (Intelligent Platform Management Interface)
* iLO (Integrated Lights Out Manager)
* iDRAC (Integrated Dell Remote Access Controller)
* AMT (Intel Active Management Technology)
* iRMC, CIMC, UCSM, and many more

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
* Flexible JSON schema
* A/synchronous operation
* Extensibility

Redfish benefits
================

* Human readable and self documented
* Tools readily available
* Language independent
* Easy automation
* Standard way for OEM extensions

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

Redfish OEM extensions
======================

Example: list servers
=====================

* Possibly live example

Example: power-on server
========================

* Possibly live example

Swordfish: storage extension
============================

Redfish + YANG: networking
==========================

Summary from https://www.dmtf.org/sites/default/files/Managing_Network_Infrastructure_via_Redfish_v2.pdf
