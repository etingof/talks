

Bare Metal In The Cloud: Isn’t it Ironic?
=========================================

*by Dmitry Tantsur and Ilya Etingof, Red Hat*

In this talk
------------

* Why allocating bare metal machines
* Ironic introduction, architecture and workflows
* Future features

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

What's inside ironic
--------------------

* Conductor Service - work flow engine
* API Service
* Drivers

.. image:: conceptual_architecture.png
   :align: center
   :scale: 70%

Machine deployment workflow
---------------------------

* Power ON
* PXE boot deploy image
* Write user image
* Reboot

.. image:: ironic-sequence-pxe-deploy.png
   :align: center
   :scale: 70%

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
