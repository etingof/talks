
Redfish - future of hardware management
=======================================

*by Dmitry Tantsur and Ilya Etingof, Red Hat*

Why hardware management?
========================

Late night, you, as a sysadmin, are in your deep sleep. Suddenly,
you woke up from a monitoring system call notifying you that the company's
core application has become unresponsive.

You dressed up, reached out for your computer, hopped on the
company's network, tried to ssh into the main production servers
but ssh connection hung.

Desperate, you were trying to understand the problem by pinging
the servers - ping works.

Uh, your cell phone rung, that's your boss. They were very concerned,
almost freaking out. So you got 15 more minutes to figure it out or...

What do you do next?

Hardware management to rescue
=============================

As this story goes, the lucky sysadmin had some form of hardware management
system installed. So you used it to get on remote console of the server.
You observed a severe filesystem corruption, so you went ahead booting
server from network, repairing the filesystem and booting back to normal.

Imagine what would happen if there was no hardware management in place...

Management of scale
===================

The other use case when hardware management can be a game changer is a
large-scape deployment e.g. the situation when you got to run a large farm
of servers perhaps at a DC.

With some form of hardware management system capable of booting the servers,
hooking on console, updating firmware, monitoring physical parameters etc.
can significantly improve data centre automation.

You will appreciate the difference whenever you need to enroll or update
thousands servers at a time.

How it works
============

Typically, the hardware management system is based on a small satellite
computer known as BMC. It has direct access to the parts of the main
system what allows it to power up/down the main system, change BIOS
settings etc.

The fact that it is an independent computer makes so-called out-of-band
access to the main system possible. Out-of-band here means that the
main system takes no part in the management operations. It can be up and
running or completely dead.

The BMC is running a software agent which acts as a frontend to all the
features of the management platform. This software agent implements a
protocol over which the clients can talk to the BMC.

This talk is about the Redfish protocol, however many others exist now
days or existed in the past.

The problem with so many standards is that you can't easily choose one.
More often than not, you are forced to support some of them to fully manage
your fleet.

It is anticipated, that the legacy protocols will be eventually phased
out in favour of the Redfish.

Even earlier
============

But it used to be worse in the past!

Before the BMC era, sysadmins used bulky remotely controlled
keyboard-video-mouse switches, console servers (which aggregate the
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
roaring racks hugging a pager tight...

Redfish design
==============

The Redfish protocol is quite new. It has been released as an official
standard of the Distributed Management Task Force organization in 2015.

To put it simple, Redfish is a web service exposing REST API communicating
JSON-serialized data.

It implements synchronous and asynchronous calls and is designed for
future extensibility what allows, for example, hardware vendors to seamlessly
support their proprietary features within the Redfish server.

Redfish benefits
================

* Human readable and self documented
* Tools readily available
* Language independent
* Easy automation
