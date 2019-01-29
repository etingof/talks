

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
* Node cleaning (BIOS, RAID etc)
* Network configuration
* Boot configuration
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

* Apply BIOS settings, reassemble RAID
* Configure boot from network
* Boot IPA ramdisk
* Wipe out local drives, reassemble RAID

.. Things to talk about ^ (ietingof)

  Automated cleaning is performed to ensure consistent and clean
  system.

  During cleaning multiple steps could be performed on the node
  in the form of in-band and out-of-band cleaning.

  Out-of-band cleaning steps use BMC to set BIOS settings, assemble
  RAID, etc.

  In-band cleaning involve booting IPA ramdisk to wipe out local
  drives, assemble RAID and possibly many other things that can be done
  from within the system itself.

Deployment: Networking
----------------------

Various network management models:

* Node stays on the same network
* Ironic configures switch to move node across networks

.. Things to talk about ^ (dtantsur)

  Deployment security and bandwidth utilization could be the reasons
  why operators may want to move the node onto a dedicated network
  for deployment or cleaning.

  Ironic is integrated with OpenStack Neutron which has integration with
  certain hardware switches through Ansible and ML2 driver to move switch
  port from one network to the other during node transitioning through its
  life-cycle.

  If dedicated provisioning or cleaning network is used, ironic will
  move the node to it prior to booting.

Deployment: Boot configuration
------------------------------

* Boot from network (PXE, iPXE, Virtual Media)
* Boot IPA for deploy

.. Things to talk about ^ (dtantsur)

  Depending on the hardware capabilities, ironic can set up node
  and the surrounding infrastructure to boot the system over PXE.
  iPXE or Virtual Media.

  While PXE-boot being the most common approach, it's also least
  reliable and scalable. With virtual media boot getting traction,
  system boot becomes faster and more reliable.

  More often than not, the node has a local drive to boot from. To
  image local drive, ironic first boots the IPA ramdisk which stands
  up ironic agent inside the systems being deployed. Ironic conductor
  guides ironic agent through image flashing process.

Deployment: Deploy user image
-----------------------------

Many ways to write user image

* Over iSCSI
* Over HTTP
* BitTorrent

.. Things to talk about ^ (dtantsur)

  Most common image writing technique in the past has been over iSCSI
  where IPA exposes node's local drive as iSCSI target and ironic conductor
  writes desired image onto it.

  Faster and more reliable approach is to stream image from ironic conductor
  to IPA which immediately writes image on local drive.

  Finally, in the situation when many nodes being installed simultaneously,
  the image can be seeded by ironic conductor initially, them the nodes
  can help distribute it across the emerging fleet of bare metal nodes.

Deployment: sequence diagram
----------------------------

.. image:: ironic-sequence-pxe-deploy.png
   :align: center
   :scale: 70%

.. Things to talk about ^ (dtantsur)

  Reiteration of the above slides using PXE-boot as example.

Upcoming features
-----------------

* Deploy Templates
* Federation Capabilities
* Graphical Console Support

.. Things to talk about ^ (dtantsur)

Future use-cases
----------------

* Hyper-converged, containers
* Edge cloud

.. Things to talk about ^ (dtantsur)
