

Bare Metal In The Cloud: Isn’t it Ironic?
=========================================

*by Dmitry Tantsur and Ilya Etingof, Red Hat*

.. image:: Ironic_mascot_color.png
   :align: center
   :scale: 25%

In this talk
------------

* What's bare metal provisioning
* Ironic introduction and work flows
* The future of ironic

.. Things to talk about ^ (ietingof)

  In this talk we are going to explain bare metal management and
  why it is becoming increasingly important.

  We will go on introducing the ironic project, it's place on the cloud
  landscape and typical bare metal management work flow.

  In the end we will give you an idea what future holds for ironic.

Why bare metal allocation
-------------------------

* Raw computing power
* Hard-to-virtualize hardware e.g. GPU, FPGA
* Perfect isolation e.g. tenant security
* Cloud software deployment

.. Things to talk about ^ (ietingof)

  The original idea behind bare metal provisioning is to allow
  bare metal node allocation in the very similar was as a VM is
  allocated in the cloud.

  The reasons for bare metal allocation are many:

  * the workload may require the full power of bare metal
  * the workload may rely on special, non-virtualized hardware e.g. GPU
  * the workload operates on a sensitive data requiring perfect
    tenant isolation

  Over time another use-case has become quite dominant - the cloud
  infrastructure itself, especially in large clouds, needs to be managed
  including container orchestration systems.

Why ironic
----------

* Fully API driven, CLI and GUI available
* Mature and battle-tested
* Active and diverse upstream
* Good vendor support

  * HPE, Dell EMC, Fujitsu, Cisco, Lenovo, Huawei
  * 3-rd party CI is mandatory

.. Things to talk about ^ (ietingof)

  Ironic is a web service orchestrating bare metal provisioning.
  It's driven by REST API and is shipped with a CLI and GUI tools.

  Ironic is being used in production by many large and well-known
  OpenStack operators for five years now.

  That probably explains quite active upstream community and significant
  hardware vendor support.

Two faces of ironic
-------------------

* Stand-alone bare metal provisioning service

  + RESTful API
  + Ironic Conductor
  + Deployment Agent

* OpenStack bare metal provisioning service

  + OpenStack Nova driver

.. Things to talk about ^ (ietingof)

  Ironic project has been started as a fork of OpenStack Nova bare metal
  driver. It has become the mainstream bare metal provisioning service
  for OpenStack and has grown in functionality a great deal since then.

  Now days ironic has two faces: one is a general-purpose bare metal
  provisioning service that can be used stand-alone for whatever purpose
  and that consists of three parts:

  * The RESTful API service
  * The ironic service which orchestrates bare metal machines
  * The IPA which sometimes runs inside the bare metal machine
    being deployed to handle local tasks

 The other is the OpenStack Bare Metal service that also requires an OpenStack
 Compute (Nova) driver to schedule bare metal machines alongside VMs.

Hardware management harness
---------------------------

* Baseboard Management Controller (BMC)
* Hardware management protocols (IPMI, Redfish etc)

.. Things to talk about ^ (ietingof)

  More often than not, now days' computers, switches and storage devices
  that are designed for data centre use carry a small satellite computer
  which is always ON, connected to the network and, most importantly, has
  direct and quite intricate access to the main system's internals. This
  computer is known as BMC and it's heavily relied upon by ironic.

  The BMCs talk a specially designed protocol known as hardware management
  protocol. The contemporary mainstream protocol of this kind as known as
  Redfish, and it is rapidly replacing the IPMI protocol as well as many
  different vendor-specific protocols.

  Ironic supports many hardware management protocols via the abstraction
  layer called 'hardware type'.

What BMC can do
---------------

* System power management
* Boot device configuration
* System BIOS management
* Hardware RAID configuration
* Virtual media boot
* ... and many others

.. Things to talk about ^ (ietingof)

  Probably the most important operation on a bare metal machine is
  its power control. Meaning the ability to flip system power on/off
  and read current power state. All via BMC calls.

  Besides power, it is no less important to be able to change boot
  device and boot mode.

  More sophisticated and sort of optional features include the ability
  to manage BIOS settings, assemble hardware RAIDs, perform system
  boot from virtual local CD drive and many others

Machine lifecycle
-----------------

Preparation:

* Hardware introspection
* Node cleaning (BIOS, RAID etc)

Deployment:

* Network configuration
* Boot configuration
* Image deployment
* Custom OS configuration

Tear down:

* Network unconfiguration
* Node cleaning (wipe disks, reset BIOS, etc)

.. Things to talk about ^ (ietingof)

  Let's follow ironic deploying typical bare metal machine. We will
  assume that the machine has a pretty functional BMC talking Redfish
  protocol.

  With this workflow we start with blank or previously used bare metal
  machine and end up with fully configured user OS running on the machine.

Preparation: Inspection
-----------------------

Out-of-band:

* Hardware capabilities
* Inventory information
* ...

In-band:

* All the above
* Benchmarks
* Allocated ports at the switch
* ...

.. Things to talk about ^ (ietingof)

  Once ironic becomes aware of a node (meaning BMC network address,
  credentials) hardware inspection could be performed.

  During inspection multiple steps could be performed on the node
  in the form of in-band and out-of-band inspection.

  Out-of-band inspection helps gathering:

  * node hardware capabilities (can be used for scheduling)
  * inventory information

  In-band inspection runs ironic agent inside the system being inspected
  where it learns about on-board NICs, its MACs and pretty much anything
  the user want to run on the system.

  On top of that, IPA can snoop on the network leaning to which port
  on the switch the NIC is attached to.

  This information can be used at the subsequent steps of the deployment
  work flow.

Preparation: Cleaning
---------------------

Out-of-band:

* Apply BIOS settings
* Reassemble hardware RAID
* Update firmware
* ...

In-band:

* Wipe out local drives
* Reassemble RAID
* ...

.. Things to talk about ^ (ietingof)

  Automated cleaning is performed to ensure consistent and clean
  system.

  Much like inspection, during cleaning multiple steps could be performed
  on the node in the form of in-band and out-of-band cleaning.

  Out-of-band cleaning steps use BMC to set BIOS settings, assemble
  RAID, etc.

  In-band cleaning involves booting IPA ramdisk to wipe out local
  drives, assemble RAID and possibly many other things that can be done
  from within the system itself.

Deployment: Workflow
--------------------

* Choose a bare metal machine to deploy
* Connect to the deployment network
* Configure boot of the deployment ramdisk
* Partition the device and flash the image
* Disconnect the deployment network, connect the instance networks
* Configure the final instance booting
* Reboot into the final instance

.. Things to talk about ^ (dtantsur)

   Quick recap of the workflow from 3 slides ago to separate ready-state
   preparation from deployment itself.

Deployment: Networking
----------------------

Two kinds of networks:

* Service (cleaning, provisioning, rescue)
* Tenant (for end users)

Three network management models:

* Using existing network infrastructure
* Using OpenStack Networking with shared network
* Using OpenStack Networking with switch management

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

* Boot from network: PXE, iPXE
* Virtual Media: HTTP, CIFS, NFS
* Legacy boot vs UEFI

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

* From conductor over iSCSI
* From the agent over HTTP

  * In-memory conversion
  * Streaming raw images

* Potential: BitTorrent

.. Things to talk about ^ (dtantsur)

  Most common image writing technique in the past has been over iSCSI
  where IPA exposes node's local drive as iSCSI target and ironic conductor
  writes desired image onto it.

  Faster and more reliable approach is to stream image from ironic conductor
  to IPA which immediately writes image on local drive.

  Finally, in the situation when many nodes being installed simultaneously,
  the image can be seeded by ironic conductor initially, them the nodes
  can help distribute it across the emerging fleet of bare metal nodes.

Other features
-----------------

Current:

* Firmware Updates
* Serial Console
* Rescue Mode
* Port Groups

Future:

* Deploy Templates
* Graphical Console

.. Things to talk about ^ (dtantsur)

   Just list the features that were not covered.

Future use-cases
----------------

* Hyper-converged, containers
* Edge cloud, federation

.. Things to talk about ^ (dtantsur)

Thank you!
----------

Learn more

* https://docs.openstack.org/ironic/latest/

Talk to us:

* openstack-discuss@lists.openstack.org
* #openstack-ironic @freenode

.. Things to talk about ^ (dtantsur)
