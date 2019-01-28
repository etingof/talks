

Bare Metal In The Cloud: Isn’t it Ironic?
=========================================

*by Dmitry Tantsur and Ilya Etingof, Red Hat*

In this talk
------------

* Why allocating bare metal machines
* Ironic introduction and work flows
* Present and upcoming features

.. Things to talk about ^ (ietingof)

  In this talk we are going to explain bare metal management is and
  why it is becoming increasingly important.

  We will go on introducing the ironic project, it's role in the cloud
  software and typical bare metal management work flow.

  In the end we will talk about the latest and upcoming ironic features.

Why bare metal allocation
-------------------------

* Raw computing power
* Hard-to-virtualize hardware e.g. GPU
* Perfect isolation e.g. tenant security
* Cloud software deployment

.. Things to talk about ^ (ietingof)

  For cloud users it may make sense to allocate a bare metal machine
  instead of a VM instance because:

  * the workload may require the full power of bare metal
  * the workload may rely on special, non-virtualized hardware e.g. GPU
  * the workload operates on a sensitive data requiring perfect
    tenant isolation

  But there are other use-cases. For example, automated cloud software
  deployment such as OpenStack or Kubernetes nodes.

What's ironic
-------------

* OpenStack bare metal provisioning service

  + Ironic Conductor
  + Deployment Agent
  + OpenStack Nova driver

* Stand-alone bare metal provisioning tool

.. Things to talk about ^ (ietingof)

  Ironic project has been started as a fork of OpenStack Nova bare metal
  driver. It has become the main stream bare metal provisioning service
  for OpenStack and grown in functionality a great deal since then.

  Now days OpenStack ironic service consists of three parts:

  * The ironic service which orchestrates bare metal machines
  * The IPA which sometimes runs inside the bare metal machine
    being deployed to handle local tasks
  * Nova driver to schedule bare metal machines alongside VMs

  At the same time ironic could be used as a stand-alone bare
  metal machines orchestration tool for whatever purpose.

Hardware management harness
---------------------------

* Baseboard Management Controller (BMC)
* Hardware management protocols (IPMI, Redfish etc)

.. Things to talk about ^ (ietingof)

  More often than not, now days' computers, switches and storage devices
  that are designed for data centre use carry a small satellite computer
  which is always ON, connected to the network and, most importantly, has
  direct and quite deep access to the main system. This computer is known
  as BMC and it's primarily relied upon by ironic.

  The BMCs talk a specially designed protocol known as hardware management
  protocol. The mainstream protocol of this kind as known as Redfish, and
  it is rapidly replacing the IPMI protocol as well as many different
  vendor-specific protocols.

  Ironic supports many hardware management protocols via the abstraction
  layer called 'hardware type'.

Management operations
---------------------

* System power management
* Boot device configuration
* System BIOS management
* RAID configuration
* Virtual media boot
* ... and many others

.. Things to talk about ^ (ietingof)

  Probably the most important operation on a bare metal machine is
  its power control meaning the ability to flip system power on/off
  and read current power state. All though BMC, of course.

  Besides power, it is no less important to be able to change boot
  device and boot mode.

  More sophisticated and sort of optional features include the ability
  to manage BIOS settings, build local on-board RAID, perform system
  boot from virtual local CD drive and many others

Machine deployment workflow
---------------------------

* Hardware introspection
* Node cleaning
* Boot, BIOS, RAID configuration
* Switch configuration
* Image deployment
* Custom OS configuration

.. Things to talk about ^ (ietingof)

  Let's follow ironic deploying typical bare metal machine. We will
  assume that the machine has a pretty functional BMC talking Redfish
  protocol.

  With this workflow we start with blank or previously used bare metal
  machine and end up with fully configured user OS running on the machine.

Deployment: Inspection
----------------------

Discover:

* Hardware capabilities
* NICs MACs
* Allocated ports at the switch

.. Things to talk about ^ (ietingof)

  Once ironic becomes aware of a node (meaning BMC network address,
  credentials) hardware inspection could be performed. During inspection
  ironic learns the details of the node such as:

  * node hardware capabilities (can be used for scheduling)
  * node NICs MACs
  * port of the switch into which the node is plugged

  This information can be used at the subsequent steps of the deployment
  work flow.

Deployment: Cleaning
--------------------

* Reset BIOS, disassemble RAID
* Configure boot from network
* Boot IPA ramdisk
* Wipe out local drives

.. Things to talk about ^ (ietingof)




Deployment: Set up the stage
----------------------------

* Network configuration

  - Move bare metal on the provisioning network

* Hardware Introspection

  - Out-of-band and/or
  - In-band

Deployment: Prepare bare metal
------------------------------

* Configure BIOS settings
* Set up RAID
* Clean up

Deployment: Install user image
------------------------------

* Set boot device, boot mode, power ON
* Boot deploy agent
* Pull, install and customize user image

.. image:: ironic-sequence-pxe-deploy.png
   :align: center
   :scale: 70%

Deployment: the final touch
---------------------------

* Network configuration

  - Move bare metal on the provider network

* Provision the work load

  - Containers
  - OpenStack services (e.g. Triple O)
  - User applications

Latest developments
-------------------

* Ansible-based deployment
* Redfish out-of-band introspection
* Redfish BIOS configuration management

Upcoming features
-----------------

* Deploy Templates
* Federation Capabilities
* SmartNIC Support
* Graphical Console Support
