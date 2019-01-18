

Bare Metal In The Cloud: Isn’t it Ironic?
=========================================

*by Dmitry Tantsur and Ilya Etingof, Red Hat*

In this talk
------------

* Why allocating bare metal machines
* Ironic introduction and work flows
* Present and upcoming features

Why bare metal allocation
-------------------------

* Raw computing power
* Hard-to-virtualize hardware e.g. GPU
* Perfect isolation e.g. tenant security

What's ironic
-------------

* OpenStack bare metal provisioning service
* + OpenStack Nova driver
* + Deployment Agent

Machine deployment workflow
---------------------------

* Set up the stage
* Configure the hardware
* Install user image

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
