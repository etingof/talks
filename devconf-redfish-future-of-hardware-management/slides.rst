
Redfish - future of hardware management
=======================================

*by Dmitry Tantsur and Ilya Etingof, Red Hat*

.

.. image:: redfish.png
   :align: center

Why hardware management?
========================

Late night, you are in your bed:

* 4:00am - night shift calls - app is down
* 4:05am - reasons are still not clear
* 4:10am - your boss gives you 10 more minutes...

What do you do now?

Hardware management to the rescue
=================================

* Get the console
* Boot from network
* Fix the problem

Management of scale
===================

* Large fleet of servers
* Mass deployment
* Frequent re-purposing
* Automation

How it works
============

* An independent satellite computer (BMC, Enclosure manager)
* Out-of-band access to the main system
* Many protocols, standard and proprietary

How it works
============

.. image:: bmc.svg

What is Redfish
===============

* Just a new hardware management protocol
* ...to eventually obsolete all others

Before the Redfish
==================

* IPMI (Intelligent Platform Management Interface)
* iLO (Integrated Lights Out Manager)
* iDRAC (Integrated Dell Remote Access Controller)
* AMT (Intel Active Management Technology)
* iRMC, CIMC, UCSM, and many more

Even earlier
============

* Remote KVM switches
* Console servers
* Circuit breakers
* In-band remote access: VNC, RDS

When it all started
===================

* Night shifts at the DC

Redfish design
==============

* REST API service
* The oData schema
* A/synchronous operation
* Extensibility

Redfish benefits
================

* Universal adoption
* Human readable and self documented
* Tools readily available
* Standard way for OEM extensions

Redfish core components
=======================

.. image:: redfish-components.svg

Redfish resources
=================

* Systems (server, CPU, memory, devices, etc.)
* Chassis (Racks, Enclosures, Blades, etc.)
* Managers (BMC, Enclosure Manager, etc.)

.. image:: redfish-resources.svg

Redfish operations
==================

.. image:: redfish-components-2.svg

List systems
============

By HTTP GET'ing the resource:

.. code-block:: bash

   $ curl http://enclosure-A/redfish/v1/Systems
   {
      "Name": "Computer System Collection",
      "Members@odata.count": 4,
      "Members": [
         { "@odata.id": "/redfish/v1/Systems/blade-0" },
         { "@odata.id": "/redfish/v1/Systems/blade-1" },
         { "@odata.id": "/redfish/v1/Systems/blade-2" },
         { "@odata.id": "/redfish/v1/Systems/blade-3" }
      ]
   }

Read system resource
====================

Inventory branch:

.. code-block:: bash

   $ curl http://enclosure-A/redfish/v1/Systems/blade-0
   {
      "Model": "3500RX",
      "SerialNumber": "437XR1138R2",
      "PartNumber": "224071-J23",
      "Description": "Web Front End node",
      "HostName": "web483",
      "Status": {
         "State": "Enabled",
         "Health": "OK",
      }
      ...

Read system resource
====================

Hardware branch:

.. code-block:: bash

      ...
      "ProcessorSummary": {
         "Count": 2,
         "ProcessorFamily": "Multi-Core Intel(R) Xeon(R) processor 7xxx Series",
         "Status": {
            "State": "Enabled",
            "Health": "OK"
         }
      },
      "MemorySummary": {
         "TotalSystemMemoryGiB": 2,
         "Status": {
            "State": "Enabled",
            "Health": "OK"
         }
      },

Read system resource
====================

System boot branch:

.. code-block:: bash

   ...
   "IndicatorLED": "Off",
   "PowerState": "Off",
   "Boot": {
       "BootSourceOverrideEnabled": "Continuous",
       "BootSourceOverrideTarget": "Hdd",
       "BootSourceOverrideTarget@Redfish.AllowableValues": [
           "Pxe",
           "Cd",
           "Hdd"
       ],
       "BootSourceOverrideMode": "UEFI",
   },

Change boot sequence
====================

By HTTP PATCH'ing the resource:

.. code-block:: bash

   $ curl -d '{
           "Boot": {
               "BootSourceOverrideEnabled": "Once",
               "BootSourceOverrideTarget": "Pxe"
           }
       }'
       -H "Content-Type: application/json"
       -X PATCH
       http://enclosure-A/redfish/v1/Systems/blade-0

Power-on the machine
====================

By calling Action on the machine:

.. code-block:: bash

   $ curl -d '{
            "ResetType": "On"
        }'
       -H "Content-Type: application/json"
       -X POST
        http://enclosure-A/redfish/v1/Systems/blade-0/Actions/ComputerSystem.Reset

Redfish services
================

* Tasks (asynchronous operations)
* Sessions (web authentication)
* AccountService (service for managing users)
* EventService (alerting clients)

Redfish OEM extensions
======================

Swordfish: storage extension
============================

Redfish + YANG: networking
==========================
