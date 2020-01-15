

Bare Metal At The Edge
======================

*by Ilya Etingof, Red Hat*


In this talk
------------

* Edge Cloud vs Centralized Cloud
* Booting at the Edge
* Baremetal deployment demo

.. Things to talk about ^

    In this talk we will look into how the Edge cloud is different from the
    conventional, centralized cloud from the bare metal management
    perspective.

    We will be considering the challenges that bare metal machine management
    might run into when deploying machines at the edge of the cloud and ways
    to overcome these problems.

    Finally, I will play a short demo of a bare metal deployment with a OpenStack
    ironic as a stand-alone deployment tool.

Edge cloud
----------

.. image:: edge-cloud.png
   :align: center
   :scale: 90%

.. Things to talk about ^

    It seems that now days, some of originally centralized cloud
    deployments transform into a more distributed layout.

    The reasons that drive this change are many. Just to mention a few:

    * Growth of IoT devices deployments pushes data collection and
      processing facilities closer to the data sources, i.e. IoT swarms.

    * The emergence of broadband content delivery services (such as 4k/8k
      video) pushes data storage facilities closer to the households.

    Stretching originally centralized infrastructure across slower, lossy and
    unreliable network affects some of hardware management procedures.

    Most importantly, that affects BMC access and node booting.

BMC access over unreliable network
----------------------------------

.. image:: bmc-access.png
   :align: center
   :scale: 90%

.. Things to talk about ^

    BMC is a small satellite computer running its own OS. It’s
    always up and running and has intricate access to the components of the
    main system. For example, BMC can turn on/off power, change boot order,
    BIOS settings and many other things.

    Stretching control plane, including BMC access, worsens reliability and
    widens attach surface what raises security concerns.

Boot protocols are fragile
--------------------------

.. image:: edge-booting.png
   :align: center
   :scale: 90%

.. Things to talk about ^

    The most basic operation of the cloud is instance allocation AKA scheduling.
    That also applies to the baremetal machines.

    Scheduling process typically runs a baremetal machine through one or
    more reboots and booting at the Edge may be risky.

PXE-boot work flow
------------------

.. image:: pxe-workflow.png
   :align: center
   :scale: 90%

.. Things to talk about ^

    Traditional way of booting a machine in the cloud is to rely on PXE suite
    of protocols. The typical process goes like this:

    * BMC sets node boot mode & boot device, then issues the power ON command.
      If this is done over IPMI, packet loss can fail or slow down any of
      these steps.

    * The node (or its NIC) broadcasts in search of a DHCP server on the local
      network. If successful, L3 connectivity is established. If not, the node
      fails booting.

    * The node pulls boot image over TFTP. If this fails, the node won't come
      up.

    Of course, there have been some improvements to the original PXE boot
    work flow (e.g. iPXE), however the weak point - reliance on DHCP is still
    there.

Why PXE-boot is unreliable?
---------------------------

* IPMI, DHCP & PXE over long, lossy network
* DHCP requires L2 connectivity by design
* Boot image transfer over TFTP is unreliable
* Security: image & node identification is hard to implement

.. Things to talk about ^

    IPMI and PXE suite of technologies has been designed decades ago targeting
    smaller, LAN-based networks. The original assumption seems to be that LAN
    is fast, reliable and reasonably secure.

    Some of LAN properties have been hardcoded into protocol design e.g. DHCP
    requires L2 broadcast functionality.

    PXE way of boot image transfer over network -- TFTP is optimized for smaller
    images, lossless network and heavily resource constraint client - network
    interface card. None of these assumptions hold with the edge cloud scenario.

    Finally, with PXE suite it is not easy for the infrastructure to reliably
    identify the node being booted to boot it in some specific way. Also, once
    the node is up and running, it is hard to tell one from the other because
    there is no reliable way to distinguish them.

A new way of booting
--------------------

* Redfish to replace IPMI and vendor-specific protocols
* Virtual media can replace PXE/TFTP and DHCP
* Machine config can be embedded into boot image

.. Things to talk about ^

    The industry and cloud software development communities are trying to
    improve things addressing the most of these weak points.

    Specifically, Redfish has been designed and being adopted by large
    hardware vendors.

    Implemented within Redfish framework, virtual media boot is to replace
    PXE/TFTP phases.

    Leveraging the secure OOB channel of boot information delivery, node
    network configuration and security materials can be passed to the
    node being booted solving DHCP dependency problem.

Redfish architecture
--------------------

.. image:: redfish-arch.png
   :align: center
   :scale: 90%

.. Things to talk about ^

How Redfish is better than IPMI
-------------------------------

* IPMI is old and less understood
* Redfish is as versatile and secure as today’s Web is
* Redfish operates over REST API endpoints

.. Things to talk about ^

    Prior to Redfish, the only standard and mainstream OOB hardware management
    protocol used to be IPMI. The protocol dates back to late 90’s and shares
    similar weaknesses as PXE suite does.

    IPMI is not well-suited to manage baremetal machines over congested and
    lossy network. IPMI learning curve is quite steep, failure analysis
    requires protocol knowledge.

    With Redfish, everything is different. This new protocol has been
    designed around well-established protocols and tools widely used in
    everything web.

    That automatically ensures review scrutiny and timely maintenance.
    On top of that, people tend to understand how web works in the first
    place compared to less niche technologies.

    Technically, Redfish is a client-server system where the parties talk
    HTTP/S, exchange schema-guarded JSON documents over REST API.

What's virtual media
--------------------

On BMC side:

* Emulates removable media devices
* Pulls user-specified boot image off the network
* “Inserts” boot image into virtual media device
* Configures BIOS to boot from virtual media device

On machine side:

* Boot from a local removable media device

.. Things to talk about ^

    Virtual media boot is a function of BMC. BMC can emulate a large
    number of virtual media devices of various types (it's all
    imaginary!) and make them visible to the main system as local
    hardware.

    BMC then can be instructed to obtain a specific boot image one way
    or the other (HTTPS, NFS, SMB etc), and “insert” it into the imaginary
    virtual media device just like we (humans) slid a diskette and later
    CD disk into a PC.

    Finally, BMC can configure system BIOS to boot from the virtual media
    device of choice.

    All BMC communication is running over authenticated and encrypted
    HTTP/S connections. That includes controlling BMC and obtaining
    images.

Redfish virtual media boot
--------------------------

The virtual media way:

* Prepares boot image with static network config
* Inserts boot image into virtual media and powers on the node (Redfish)
* Orchestrates agent to prepare/deploy the node
* Reboots the node (Redfish) into deployed image

.. Things to talk about ^

    With virtual media, deployment workflow differs. Most importantly, it has
    no dependency on unreliable old-school protocols.

    Ironic prepares a boot image with its agent inside. Besides the software,
    full network configuration for the ramdisk OS is burnt into the boot
    image.

    Ironic inserts boot image into a virtual media device and powers on
    the node - all over Redfish.

    Running IPA registers itself with ironic, ironic orchestrates IPA to
    perform node cleaning and user image flashing.

    Finally, ironic power cycles the node (over Redfish again) to boot deployed
    image from local disk (which one of many options).

In the demo
-----------

* Machine fully managed over Redfish
* Booted from virtual media DVD
* Ironic ramdisk image configures itself from ISO-based config drive
* Deployed image runs cloud-init against ISO-based config drive

.. Things to talk about ^

    In the upcoming demo:

    The user provides ironic with network configuration settings for both
    ironic agent and user instance OS in form of Nova network config metadata
    (network_data.json).

    Ironic writes network configuration as part of OpenStack config-drive onto
    boot ISO.

    Ironic sets the node to boot from virtual CD and powers on the node.

    Booting operating system initialization harness (e.g. cloud-init) discovers
    network configuration and applies it to the OS.

    This way no IPMI/PXE is ever involved.

What's ironic
-------------

* Baremetal hypervisor for OpenStack
* And for container management platform (Metal3)
* And just a stand-alone REST API managed tool

.. Things to talk about ^

    Ironic is a software that implements baremetal hypervisor for OpenStack.
    Originally, the goal has been to allocate baremetal machines along the
    same lines as cloud instances.

    Later on, ironic has also become a stand-alone machine provisioning
    tool. In the context of this presentation, we will not consider
    OpenStack at all.

Demo deployment
---------------

.. video:: /ironic-ramdisk-static-config.mkv

.. Things to talk about ^

Summary
-------

* Edge cloud is raising
* Better hardware management protocol
* Better cloud software support

.. Things to talk about ^

    Distributed cloud implementation becomes a new norm. Moving hardware
    to the outskirts of the infrastructure poses many difficulties and
    risks.

    In effort to mitigate the risks the industry comes up with a better
    suited hardware management protocol - Redfish.

    Open source community supports its use from their end by implementing
    it in free cloud software such as OpenStack.

Thank you!
----------

Learn more

* https://docs.openstack.org/ironic/latest/

Talk to us:

* openstack-discuss@lists.openstack.org
* #openstack-ironic @freenode
