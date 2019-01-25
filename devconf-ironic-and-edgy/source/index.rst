
Ironic and Edgy
===============

*by Dmitry Tantsur and Ilya Etingof, Red Hat*

In this talk...
===============

* Why Edge Cloud?
* Bare Metal provisioning at the Edge
* Ironic at the Edge: now and in the future

.. Things to talk about ^ (ietingof)

  In this talk we are going to explain what this Edge effort means,
  why it is important and generally desired by OpenStack operators.

  We will go on explaining the bare metal management, challenges and
  possibly solutions in the Edge context.

  At ironic, we seem to have multiple areas to address and improve for
  the Edge cloud purposes. We will share with you the news on the
  anticipated and ongoing work in that regard.

Why Edge Cloud
==============

* Low-latency, data-hungry applications:

  * IoT and smart homes
  * 8k video delivery

* Economically viable
* AI-managed data centres
* Autonomous or self-driving data centres

.. Things to talk about ^ (ietingof)

  There seems to be many factors that fuel the edge effort. Just to
  name a few:

  Growth of IoT devices deployments pushes data collection and processing
  facilities closer to the data sources, i.e. IoT swarms.

  The emergence of broadband content delivery services (such as 8k video)
  pushes data storage facilities closer to the households.

  Probably trying to cut costs and make the business more profitable,
  DC operators move parts of their DC infrastructure to the areas
  with cheaper electricity and cooler climate (to save on cooling).

  Such decentralized infrastructure calls for making the data centres
  more autonomous and automated.

  BTW, the desire for better automation aligns well with the other, otherwise
  unrelated, trends in data processing business e.g. applying machine learning
  technologies and AI on DC management tasks.

Challenges at the Edge
======================

* No living soul to "turn it off and on again"
* Remote management over slow, lossy and unreliable network
* Low footprint: limited space for management hardware
* Security concerns: larger control plane, unguarded locations

.. Things to talk about ^ (ietingof)

  Stretching originally centralized infrastructure makes physical
  attendance challenging if at all possible.

  Network becomes the only practical way of dealing with the
  infrastructure. However, being distant, network access becomes
  slow, lossy and unreliable.

  Smaller points of presence impose space and power constraints on the
  remote management equipment.

  Stretching the control plane network increases attach surface what
  raises security concerns.

  These considerations make versatile remote management even more relevant.

Bare metal on the raise
=======================

Why?

* Build, repair and re-purpose the cloud remotely

Trends:

* Converged infrastructure management e.g. servers, switches, storage, power
* Reliable and secure management protocols

.. Things to talk about ^ (ietingof)

  Ultimately, every workload is carried out by the bare metal hardware - servers,
  switches and storage systems.

  For cloud operators, setting up the infrastructure is not a one-time
  affair, rather the operators may need to respin their cloud to repurpose the
  hardware, phase out the broken one, lend the hardware to some other user.

  Perhaps not driven only by the edge effort, rather for simplification
  and cutting costs, hardware management tech tends to converge onto
  common protocols and data models.

  The introduction of the Redfish hardware management protocol
  greatly improved the reliability and security of remote access
  to the BMC and therefore to the hardware fleet.

The Ironic project
==================

* Official OpenStack bare metal project since the *Kilo* cycle

  * Plugs into the Compute service (Nova)

* Lively upstream community:

  * *Rocky*: 359 commits, 81 contributors, 24 companies.

* Established relationships with hardware vendors (Dell, HPE, Fujitsu, Lenovo,
  Cisco).

* Support for old and new industry standards (IPMI, PXE, iPXE, Redfish, SNMP,
  UEFI).

.. Things to talk about ^ (dtantsur)

  Ironic is the OpenStack project that implements provisioning and life cycle
  API for bare metal machines. It can be used in the Compute service as a
  hypervisor targeting bare metal servers with the goal of treaing
  bare metal machines as VMs from the user perspective.

  Ironic is already a relatively large project with quite active and
  diverse community of users and contributors. The last release codenamed Rocky
  has 359 commits from 81 contributors from 24 companies.

  Targeting hardware management, ironic has managed to attract a
  handful of high-profile hardware vendors thus creating and maintaining
  vendor-specific *drivers* (AKA *hardware types*) interfacing ironic
  with specific family of computers.

  Ironic has good support for both established and modern industry standards,
  protocols and technologies, such as IPMI, PXE, iPXE, Redfish, SNMP, UEFI.

Ironic in OpenStack
===================

.. image:: conceptual_architecture.png
   :align: center
   :scale: 70%

.. Things to talk about ^ (dtantsur)

   Perhaps we can tell that Ironic acts on BM boxen in the same way as
   Nova manages VMs.

Current ironic architecture
===========================

.. image:: deployment_architecture_2.png
   :align: center

.. Things to talk about ^ (dtantsur)

   Ironic is a service driven by REST API. Hardware access is mediated
   through drivers.

Ironic in action
================

.. image:: ironic-sequence-pxe-deploy.png
   :align: center
   :scale: 70%

.. Things to talk about ^ (dtantsur)

   Perhaps we should explain the workflow e.g. inspect, deploy, clean.

Challenges at the Edge
======================

Challenges:

  * PXE for boot management is unreliable
  * DHCP over WAN unreliable and insecure
  * IPMI is unreliable and insecure

    * Quiz: do you know about Cipher 0?

  * AMQP for RPC
  * Low bandwidth

.. Things to talk about ^ (dtantsur)

   In general, provisioning a server has a couple of weak points that get
   amplified if we extend the provisioning network across WAN. Technologies
   like PXE, DHCP and IPMI are not reliable, and sometimes insecure, when used
   over WAN. Using VPN solves the security aspect, but not reliability.

   Quiz: do you know what IPMI Cipher zero is? It's essentially an
   authentication mode without authentication. You heard me right.

   Our use of AMQP for RPC, which is standard for OpenStack, poses a challenge
   of scaling a reliable AMQP implementation across locations.

   Finally, low bandwidth requires careful approach when distributing images to
   nodes.

Reshaping Ironic for the Edge
=============================

Solutions:

  * Federated Ironic
  * Booting via virtual media or UEFI HTTP boot
  * DHCP-less boot over virtual media
  * Direct image streaming
  * HTTP-based protocols instead of IPMI

.. Things to talk about ^ (dtantsur)

   Therefore the focus of the ironic team is to adapt system architecture
   to mitigate those weak points. In the following slides we are going
   to discuss the major ideas:

   * Federation for Ironic API
   * Booting with virtual media or UEFI HTTP boot instead of PXE
   * Booting with virtual media without a DHCP server
   * Streaming images directly to the disk, potentiall with Bit-Torrent
   * HTTP-based protocols (e.g. Redfish) instead of IPMI

Federated architecture
======================

To decentralize and distribute ironic, yet maintaining joint view on nodes:

* Conductors groups
* Lightweight RPC
* Federating API proxy

  * prototype: `github.com/dtantsur/ironic-proxy
    <https://github.com/dtantsur/ironic-proxy>`_

.. Things to talk about ^ (dtantsur)

   For the Edge we are looking into making ironic distributed e.g. having
   many ironic instances distributed around the globe, each managing its own
   (local) set of nodes, but offering a single view on all nodes.

   As of the time being, two approaches are being researched:

   * Split conductors in conductor groups co-located with the nodes they
     manage, while still keeping the central API.

   * Use a direct RPC approach (JSON-RPC or gRPC) instead of RPC via a
     messaging queue.

   * Standing up an API proxy service talking to satellite ironic instances
     and that way joining them into a single view.

Booting is fragile
==================

Network boot is complicated and unreliable

* Network stack initialization
* Boot image transfer

.. Things to talk about ^ (ietingof)

  The most common thing one may want to do with a server is to boot it up.

  Typically, upon circuits initialization, computer system performs network
  discovery and its network stack configuration. Then the boot image gets
  transferred from the network server up to system memory where it receives
  control.

  A packet loss along the way leads to boot failure which is hard to
  analyze remotely unless one has console access to the system.

  Why is it so fragile?

The history of network booting
==============================

* PXE: BOOTP/DHCP -> TFTP
* iPXE: BOOTP/DHCP -> HTTP/iSCSI
* UEFI: BOOTP/DHCP -> HTTP/iSCSI
* Virtual Media: HTTP, SMB, NFS

.. Things to talk about ^ (ietingof)

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

BMC pulls image and serves it to the system

Features:

* Layer-3 based deployment possible
* Ensures authentic boot image
* Ability to cache boot images

.. Things to talk about ^ (ietingof)

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

Non-network boot over virtual media
===================================

* Ironic deploy image still requires DHCP
* Virtual Media offers virtual floppy \o/

.. Things to talk about ^ (ietingof)

  There is still one step in the ironic bare metal instance deployment
  process which requires network configuration step over DHCP. The
  so-called deploy image (the one which pulls the installation image
  and writes it down to the local system drive) needs DHCP thus
  requiring either DHCP server in the broadcast domain or some form of
  tunneling or proxying.

  There has been a fairly new ironic specification proposed to use
  virtual media floppy to pass static network configuration information
  for the deploy image to consume.

Image streaming
===============

* Streaming images directly to the block device
* Idea: distributing images via Bit-Torrent

.. Things to talk about ^ (dtantsur)

   One of the existing methods of ironic image deployment involves pulling
   OS image over HTTP and writing it down on the fly avoiding
   intermediate caching (what's probably the most resource-efficient and
   suites well baremetal nodes with lesser RAM).

   Another proposed approach to tackle this problem in ironic utilizes the
   BitTorrent protocol.

Summary: Ironic has an Edge
===========================

The upcoming features:

* Federated architecture
* Reliable boot methods
* Efficient image delivery

.. Things to talk about ^ (dtantsur)

  Ironic is being shaped up for the edge deployments.

  The main challenge ironic team is currently focusing on is to make
  bare metal node boot and image delivery quick and reliable at the edge
  situation.

  That will hopefully make ironic one of the best tools for bare metal
  provisioning in the edge cloud.
