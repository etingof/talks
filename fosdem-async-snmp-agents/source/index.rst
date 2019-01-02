

Building Asynchronous SNMP Agents
=================================

Presented by Ilya Etingof <etingof@gmail.com>

Why SNMP
--------

* SNMP is old and complicated
* On the other hand, SNMP is still ubiquitous in network management
* SNMP offers structured and widely understood management information (MIB)
* We have accumulated tens of thousands of MIBs over these years

Consider the use-case
---------------------

* Your network is universally SNMP-managed (e.g. NMS, CMDB etc)
* You got a new gadget (e.g. coffee pot) on the network to keep an eye on
* The coffee pot provides some health indicators through REST API. Now, how'd your NMS reach it?

Standing up an SNMP agent
-------------------------

1. Pick a standard MIB (e.g. `COFFEE-POT-MIB` from RFC2325) or come up with your own
2. Turn the `COFFEE-POT-MIB` into Python code with hooks
3. Add some code to interface MIB hooks with your RESTful coffee pot
4. Run the SNMP agent from pysnmp examples or adapt it to your needs

Demo: COFFEE-POT-MIB
--------------------

.. code-block:: bash

   $ ls -l COFFEE-POT-MIB.txt
   -rw-r--r--   1 ietingof  staff     1169 Jul 24 07:54 COFFEE-POT-MIB.txt
   $ cat COFFEE-POT-MIB.txt
   ...

    potTemperature OBJECT-TYPE
       SYNTAX     Integer32
       UNITS      "degrees Centigrade"
       MAX-ACCESS read-only
       STATUS     current
       DESCRIPTION
               "The ambient temperature of the coffee within the pot"

      ::= { potMonitor 6 }
   ...

Demo: Pythonize COFFEE-POT-MIB
------------------------------

.. code-block:: bash

   $ mibdump --destination-format pysnmp --destination-template \
       pysnmp/mib-instrumentation/managed-objects-hooks COFFEE-POT-MIB
   $ ls -l COFFEE-POT-MIB.py
   -rw-r--r--   1 ietingof  staff     2264 Jul 24 07:54 COFFEE-POT-MIB.py

Looking inside the `COFFEE-POT-MIB.py`:

.. code-block:: python

   ...
   class _PottemperatureObject(MibScalar):
       def readTest(self, varBind, **context):
           # Put your code here
           MibScalar.readTest(self, varBind, **context)

       def readGet(self, varBind, **context):
           # Put your code here
           MibScalar.readGet(self, varBind, **context)
   ...

Demo: simple synchronous call
-----------------------------

.. code-block:: python

   class _PottemperatureObject(MibScalar):

       def readGet(self, varBind, **context):
           oid, value = varBind
           value = requests.get('http://coffee-pot.local/api/v1/temperature/')

           cbFun = context['cbFun']
           cbFun((name, value), **context)

Demo: run generic SNMP agent
----------------------------

.. code-block:: bash

   $ python snmp-agent.py --load-mib COFFEE-POT-MIB
   $ snmpget -v3 -u nms localhost COFFEE-POT-MIB::potTemperature.0
   COFFEE-POT-MIB::potTemperature.0 = 85 degrees Centigrade

Why asynchronous
----------------

* Highly concurrent, do not block on computationally slow coffee pots
* Scales well - can manage a large fleet of coffee pots

Demo: asynchronous call
-----------------------

.. code-block:: python

   class _PottemperatureObject(MibScalar):

       def readGet(self, varBind, **context):
           oid, value = varBind

           def _cbFun(value):
              cbFun = context['cbFun']
              cbFun((name, value), **context)

           value = requests.get('http://coffee-pot.local/api/v1/temperature/', cbFun=_cbFun)
