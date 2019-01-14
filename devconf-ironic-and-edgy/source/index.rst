
Ironic and Edgy
===============

*by Dmitry Tantsur and Ilya Etingof, Red Hat*

In this talk...
===============

* Why Edge Cloud?
* Bare Metal provisioning at the Edge
* Ironic at the Edge: now and in the future

Why Edge Cloud
==============

* Low-latency, data-hungry applications:

  * IoT and smart homes
  * 8k video delivery

* AI-managed data centres
* Autonomous or self-driving data centres

.. Things to talk about ^

  The IoT boom evokes the need to gather, aggregate and process the
  data not far from the IoT swarm.

  Cheaper (hydro) power sources in Scandinavia (near the Arctic Circle)
  combined with good Internet connectivity and cooler climate makes it
  economically viable to build DCs in such distant and not densely populated
  areas.

  When setting up a computing facility in the alienated locations, it may
  make sense to isolate it from the other control parts of the cloud
  to reduce potential attack surface.

  This need of decentralizing the infrastructure implies making
  data centres more autonomous and automated (e.g. lights-out).
  These traits align well with the other, otherwise unrelated,
  trends - using machine learning and AI for DC management.

  Ultimately, these reasons lead to stretching the cloud infrastructure
  up to the edges of the company's network.

Challenges at the Edge
======================

* No living soul to "turn it off and on again"
* Remote management over lossy and insecure network
* Low footprint: no space for redundant hardware
* Security concerns: untrusted locations

.. Things to talk about ^

  The distant pieces of the infrastructure could be hard to attend physically
  for power cycle or replacement. And the may not be free space or power
  to allocate separate management units. That makes versatile remote management
  even more relevant.

  However, network access to the outskirts of the network could be problematic
  because the access network could be lossy, unstable, slow and insecure.

  These desires and constraints fuel further development of the remote management
  technology.

Bare metal at the Edge
======================

Why?

* Build, repair and re-purpose the cloud remotely

Trends:

* Converged infrastructure management e.g. servers, switches, storage, power
* Reliable and secure management protocols

.. Things to talk about ^

  Ultimately, every workload is handled by the bare metal hardware - servers,
  switches and storage systems. Setting up the infrastructure is not a one-time
  affair, rather the operators may need to respin their cloud to repurpose the
  hardware, phase out the broken one, lend the hardware to some other user.

  Not specifically driven by the edge effort, rather for simplification
  and cutting costs, hardware management tech tends to converge onto
  common protocols and data models. Now days Redfish (incorporting
  NETCONF) serves as such a common ground for everything hardware
  e.g. computers, switches and storage devices.

  The introduction of the Redfish hardware management protocol
  greatly improved the reliability and security of remote access
  to the BMC and therefore to the hardware fleet.

The Ironic project
==================

* Official OpenStack bare metal hypervisor since the *Kilo* cycle
* Lively upstream community
* Established relationships with hardware vendors

.. Things to talk about ^

  Ironic is the OpenStack project that implements a nova-manageable
  hypervisor targeting bare metal servers. The goal here is to
  to treat bare metal machines as VMs from the user perspective.

  Ironic has been conceived as a fork of nova baremetal driver since
  OpenStack *Icehouse* cycle, by the *Kilo* cycle ironic has become
  the officially integrated OpenStack project.

  Ironic is already a relatively large project with quite active and
  diverse community of users and contributors.

  Targeting hardware management, ironic has managed to attract a
  handful of high-profile hardware vendors thus creating and maintaining
  vendor-specific *drivers* (AKA *hardware types*) interfacing ironic
  with specific family of computers.

Ironic in OpenStack
===================

.. image:: conceptual_architecture.png
   :align: center
   :scale: 70%

.. Things to talk about ^

   Perhaps we can tell that Ironic acts on BM boxen in the same way as
   Nova manages VMs.

Current ironic architecture
===========================

.. image:: deployment_architecture_2.png
   :align: center

.. Things to talk about ^

   Ironic is a service driven by REST API. Hardware access is mediated
   through drivers.

Ironic in action
================

.. image:: ironic-sequence-pxe-deploy.png
   :align: center
   :scale: 70%

.. Things to talk about ^

   Perhaps we should explain the workflow e.g. inspect, deploy, clean.

Ironic at the Edge
==================

Challenges:

* PXE for boot management is unreliable
* DHCP over WAN unreliable and insecure
* Low bandwidth

.. Things to talk about ^

Ironic at the Edge
==================

Solutions:

* DHCP over virtual media
* Booting via virtual media or UEFI HTTP boot
* Direct deploy with image streaming
  * Potential: bit-torrent deploy
* Federated Ironic

.. Things to talk about ^

Federated architecture
======================

.. Things to talk about ^

   The system is quite centralized, for Edge we need changes...

Redfish for better management
=============================

Features:

* Converged, aggregated management
* Remote access over TCP
* Ubiquitous TLS
* Virtual Media boot
* Composable hardware

.. Things to talk about ^

  Redfish is trying to solve many shortcomings that exist in the hardware
  management sphere. Luckily, many Redfish features play well in the
  edge context.

  In the following slides we are going to look into the relevant
  Redfish feature and how they are being leveraged to solve the
  edge use-case.

Redfish: aggregated management
==============================

* Redfish models servers, switches, storage, everything
* One BMC can manage the whole rack (or the whole DC)

.. Things to talk about ^

  Redfish is a REST service implemented inside the BMC. The service is
  designed to be able to model various hardware devices such as
  computers, switches, storage systems.

  The ability to utilize common hardware management technology for
  all manageable components reduces the complexity and resource footprint.

  On top of that, Redfish promotes the arrangement when one BMC manages
  multiple pieces of hardware (possibly of different types). For instance
  one BMC can manage the whole rack housing servers, switches, power
  supplies etc.

  That potentially slims down the entire installation on the edge.

Redfish: reliable communication
===============================

* IPMI is lightweight, but unreliable
* Redfish runs HTTP over TCP

.. Things to talk about ^

  If we extend the link to the control plane over the unreliable and
  lossy network, we can't use unreliable protocols for hardware
  management.

  In the past, the protocol of choice for hardware management used to
  be IPMI which has been desined 20 years ago with a small and
  resource-constrained controller in mind. Redfish uses reliable
  network protocol (TCP) what makes it better suited for operations over
  a congested network.

Redfish: TLS is common
======================

* REST API through TLS
* Well-understood, strong crypto
* Many authentication and encryption options

.. Things to talk about ^

  Following a handful of sensitive CVEs on IPMI, hardware
  security has been improved. With Redfish the well-understood
  TLS is being used for authentication and encryption needs.

System boot management
======================

Involves many fragile pieces:

* Network discovery and autoconfiguration
* Boot image transfer
* System console access

.. Things to talk about ^

  The most common thing one may want to do with a server is to boot it up.
  Apparently, booting a computer can be a multi-stage, complicated and
  fragile undertaking.

  Typically, upon circuits initialization, computer system performs network
  discovery and its network stack configuration. Then the boot image gets
  transfered from the network server up to system memory where it receives
  control.

  Any malfunction along the way leads to boot failure which is hard to
  analyze unless one has console access to the system.

The history of network booting
==============================

* PXE: BOOTP/DHCP -> TFTP
* iPXE: BOOTP/DHCP -> HTTP/iSCSI
* UEFI: BOOTP/DHCP -> HTTP/iSCSI
* Virtual Media: HTTP

.. Things to talk about ^

  The problem of network booting has been approached long ago.

  The first well-defined and established procedure to perform the booting
  is known as *PXE*. It relies on a suite of Internet procotols of the time.
  PXE has been designed for LANs, resource-constrained NICs and smaller-scale
  installations. These were probably the reasons to use UDP for all the involved
  protocols.

  Over time, the choice of UDP has become a nuisance so that the *PXE*
  successor - *iPXE* (and later *UEFI* boot loader) introduced HTTP boot
  effectively replacing less reliable and less scalable *TFTP* for boot image
  transfer purposes.

  Still, the initial network configuration phase needs to rely on UDP-based
  DHCP protocol. With introduction of the virtual media boot technology,
  this last fragile piece in the boot sequence has been replaced making
  virtual media boot nearly ideal way to boot distant computers.

Redfish: virtual media
======================

Features:

* Layer-3 based deployment possible
* Ensures authentic boot image
* Ability to cache boot images

.. Things to talk about ^

  With virtual media, the boot image is pulled by the BMC rather than
  the booting system itself. Then BMC emulates a local CD drive using
  the downloaded image. The system gets booted from this virtual CD
  for one or more times.

  It is generally more reliable and secure to let BMC pulling specific
  boot image because BMC does not need to perform network bootstrapping.
  With BMC it's easier to ensure boot image authenticity and consistency.

  On top of that, BMC has the potential to cache and reuse boot images
  for one or many systems what is important considering the sizes of the
  boot images and potential connectivity constraints at the edge.

  Redfish fully supports virtual media operations so it fits well with
  the edge use-case.

Virtual media Layer-3 deployment
================================

* Ironic deploy image still requires DHCP
* Virtual Media offers virtual floppy \o/

.. Things to talk about ^

  There is still one step in the ironic bare metal instance deployment
  process which requires network configuration step over DHCP. The
  so-called deploy image (the one which pulls the installation image
  and writes it down to the local system drive) needs DHCP thus
  requiring either DHCP server in the broadcast domain or some form of
  tunelling or proxying.

  There has been a fairly new ironic specification proposed to use
  virtual media floppy to pass static network configuration information
  for the deploy image to consume.

Summary: Ironic has an Edge
===========================

The upcoming features:

* Federated architecture
* Redfish virtual media boot, OOB, BIOS management etc.

.. Things to talk about ^

  Ironic is being shaped up for edge deployments.

  Specifically, the new federated architecture and self-provisioning
  ironic ....

  The upcoming virtual media boot support will leverage the virtual media
  feature of the newer BMCs.

  Redfish-based out-of-band inspection and BIOS management features
  positions Ironic as a capable bare metal provisioning tool for
  edge clouds.
