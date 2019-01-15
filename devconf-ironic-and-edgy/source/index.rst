
Ironic and Edgy
===============

*by Dmitry Tantsur and Ilya Etingof, Red Hat*

In this talk...
===============

* Why Edge Cloud?
* Bare Metal provisioning at the Edge
* Ironic at the Edge: now and in the future

.. Things to talk about ^

  In this talk we are going to explain what this Edge effort means,
  why it is important and generally desired by OpenStack operators.

  We will go on explaining the bare metal management, challenges and
  possibly solutions in the Edge context.

  At ironic, we seem to have multiple areas to address and improve for
  the Edge cloud purposes. We are planning to explain the anticipated and
  ongoing work in that regard.

Why Edge Cloud
==============

* Low-latency, data-hungry applications:

  * IoT and smart homes
  * 8k video delivery

* Economically viable or untrusted locations
* AI-managed data centres
* Autonomous or self-driving data centres

.. Things to talk about ^

  The IoT boom evokes the need to gather, aggregate and process the
  data not far from the IoT swarm.

  Broadband media streaming pushes the distribution centers closer to
  the end users.

  Cheaper (hydro) power sources in Scandinavia (near the Arctic Circle)
  combined with good Internet connectivity and cooler climate makes it
  economically viable to build DCs in such distant and not densely populated
  areas.

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

  Once you place your computing facility far away from your networking HQ,
  immediately make physical attendance for power cycling or repair challenging.

  Network access to the outskirts of the network could be problematic
  because the access network could be lossy, unstable, slow and insecure.

  Smaller points of presence may not allow much of the management overhead
  in terms of power, cooling and rack space.

  Having to do everything over untrusted network impose stronger security
  requirements on the management protocols.

  These considerations make versatile remote management even more relevant.

Bare metal on the raise
=======================

Why?

* Build, repair and re-purpose the cloud remotely

Trends:

* Converged infrastructure management e.g. servers, switches, storage, power
* Reliable and secure management protocols

.. Things to talk about ^

  Ultimately, every workload is carried out by the bare metal hardware - servers,
  switches and storage systems. Setting up the infrastructure is not a one-time
  affair, rather the operators may need to respin their cloud to repurpose the
  hardware, phase out the broken one, lend the hardware to some other user.

  Not specifically driven by the edge effort, rather for simplification
  and cutting costs, hardware management tech tends to converge onto
  common protocols and data models.

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

Reshaping Ironic for the Edge
=============================

Challenges:

  * PXE for boot management is unreliable
  * DHCP over WAN unreliable and insecure
  * Low bandwidth

Solutions:

  * Federated Ironic
  * Booting via virtual media or UEFI HTTP boot
  * DHCP-less boot over virtual media
  * Deploy image streaming
  * Deploy image over BitTorrent

.. Things to talk about ^

   Reiterate on the Edge challenges e.g. long network leg, reduced deployment
   infrastructure (virtual media).

Federated architecture
======================

To decentralize and distribute ironic, yet maintaining joint view on nodes:

* API proxy
* IPMI-to-Redfish proxy

.. Things to talk about ^

   Present day ironic is quite centralized meaning that we run central ironic
   managing all nodes.

   For the Edge we are looking into making ironic distributed e.g. having
   many ironic instances distributed around the globe, each managing its own
   (local) set of nodes, but offering a single view on all nodes.

   As of this moment the ironic developers are poking at two ideas:

   * Standing up an API proxy service talking to satellite ironic instances
     and that way joining them into a single view

   * Still having a single, certralized ironic instance managing Edge nodes
     over Redfish via a Redfish-to-IPMI proxy running at the Edge.

Redfish: aggregated management
==============================

* Redfish models servers, switches, storage, everything
* One BMC can manage the whole rack (or the whole DC)

.. Things to talk about ^

  Redfish is a REST service running inside the BMC. The service is
  designed to model various hardware devices such as computers, switches,
  storage systems.

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
* Redfish runs HTTP over TCP and employs TLS

.. Things to talk about ^

  If we extend the link to the control plane over the unreliable and
  lossy network, we can't use unreliable protocols for hardware
  management.

  In the past, the protocol of choice for hardware management used to
  be IPMI which has been desined 20 years ago with a small and
  resource-constrained controller in mind. Redfish uses reliable
  network protocol (TCP) what makes it better suited for operations over
  a congested network.

  Following a handful of sensitive CVEs on IPMI, hardware
  security has been improved. With Redfish the well-understood
  TLS is being used for authentication and encryption needs.

Booting is fragile
==================

Boot strapping can be complicated and unreliable

* Network discovery and autoconfiguration
* Boot image transfer
* System console access

.. Things to talk about ^

  The most common thing one may want to do with a server is to boot it up.
  Apparently, booting a computer can be a multi-stage, complicated and
  fragile undertaking.

  Typically, upon circuits initialization, computer system performs network
  discovery and its network stack configuration. Then the boot image gets
  transferred from the network server up to system memory where it receives
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
  is known as *PXE*. It relies on a suite of Internet protocols of the time.
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

DHCP-less boot over virtual media
=================================

* Ironic deploy image still requires DHCP
* Virtual Media offers virtual floppy \o/

.. Things to talk about ^

  There is still one step in the ironic bare metal instance deployment
  process which requires network configuration step over DHCP. The
  so-called deploy image (the one which pulls the installation image
  and writes it down to the local system drive) needs DHCP thus
  requiring either DHCP server in the broadcast domain or some form of
  tunneling or proxying.

  There has been a fairly new ironic specification proposed to use
  virtual media floppy to pass static network configuration information
  for the deploy image to consume.

Deploy image streaming
======================

* Ironic implements on-the-fly image provisioning
* Images pulled over HTTP can be be cached

.. Things to talk about ^

One of the existing methods of ironic image deployment involves pulling
OS image over HTTP and writing it down on the fly e.g. avoiding
intermediate caching (what's probably the most resource-efficient and
suites well baremetal nodes with lesser RAM).

On top of that, HTTP-based images could be efficiently cached at the
Edge for repeated deployments.

Deploy image over BitTorrent
============================

* Offloads image provisioning to local nodes
* Efficient for large images and simultaneous deployment

.. Things to talk about ^

Another, still experimental, provisioning method in ironic utilizes the
BitTorrent protocol. It's serves torrent files from Glance, seeds images from
Swift and most efficient in situations of mass concurrent nodes deployment.

In the Edge situation, image provisioning through neighbouring nodes can
save bandwidth and improve reliability.

Summary: Ironic has an Edge
===========================

The upcoming features:

* Federated architecture
* Reliable deploy image propagation

.. Things to talk about ^

  Ironic is being shaped up for edge deployments.

  The new federated architecture and self-provisioning ironic ....

  The upcoming virtual media boot support combined with DHCP-less
  boot will improve boot reliability and simplify the infrastructure
  for Edge installations.

  The new ways, more reliable ways to deliver boot image to the node
  will improve deploy times.
