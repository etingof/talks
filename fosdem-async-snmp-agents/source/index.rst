

Building Asynchronous SNMP Agents
=================================

Presented by Ilya Etingof <etingof@gmail.com>

In this lightening talk
-----------------------

* Why SNMP
* The new tool: *snmpresponder*
* Demo workflow

.. Things to talk about ^

   In this talk I am going to argue why SNMP is still relevant today.

   I will present a new tool - snmpresponder - to serve user data
   over SNMP followed by an example workflow.

Why SNMP
--------

* SNMP is old, complicated and has many competitors
* SNMP is still ubiquitous in monitoring
* SNMP is well-understood by many
* We have accumulated over 10,000 MIBs [1]

1. http://mibs.snmplabs.com/asn1/

.. Things to talk about ^

  Despite its failure to become the single network management protocol of
  choice, SNMP still heavily used in monitoring applications.

  Besides being well-understood by many network engineers, another
  pillar of its popularity is the availability and great numerosity
  of MIBs - structured, machine and human readable descriptions of what's
  being managed.

Consider the use-case
---------------------

* Your network is SNMP-monitored
* New hardware arrives
* Being new, it offers just REST API...

How'd your NMS reach it?

.. Things to talk about ^

  Consider this situation (quite typical, it seems). You have a network being
  monitored by SNMP.

  But you also got some newer equipment that does not support SNMP (or any
  network management protocol at all).

  Let's say it's a bare metal server having Redfish-manageable BMC. But it
  can be just anything. How would NMS reach it?

Standing up a mediation proxy
-----------------------------

1. Pick a MIB or come up with your own
2. Turn MIB into Python code
3. Add glue code
4. Fire up the SNMP agent - *snmpresponder*

.. Things to talk about ^

   The solution being offered looks like this. You pick a MIB (or come up
   with your own), turn the MIB into a Python snippet containing necessary
   hooks, add some custom code to obtain the information from the ultimate
   data source.

   Finally, let the `snmpresponderd` tool to load and execute your
   Pythonized MIB.

Workflow: REST API as a data source
-----------------------------------

  * Let's serve the "HostName" field

.. code-block:: bash

   $ curl http://demo.snmplabs.com/redfish/v1/Systems/437XR1138R2
   ...
   {
    "Id": "437XR1138R2",
    "Name": "WebFrontEnd483",
    "AssetTag": "Chicago-45Z-2381",
    "Manufacturer": "Contoso",
    "Model": "3500",
    "SubModel": "RX",
    "SKU": "8675309",
    "SerialNumber": "437XR1138R2",
    "PartNumber": "224071-J23",
    "Description": "Web Front End node",
    "HostName": "web483",
    ...

.. Things to talk about ^

  For this presentation I picked the bare metal management protocol known as
  Redfish. It serves many details on the hardware over REST API.

  The item of interest here is the `HostName` element...

Workflow: Pick SNMP MIB
-----------------------

  * Expose as "SNMPv2-MIB::sysName"

.. code-block:: bash

   $ ls -l SNMPv2-MIB.txt
   -rw-r--r--   1 ietingof  staff     29305 Jul 24 07:54 SNMPv2-MIB.txt
   $ cat SNMPv2-MIB.txt
   ...
   sysName OBJECT-TYPE
        SYNTAX      DisplayString (SIZE (0..255))
        MAX-ACCESS  read-write
        STATUS      current
        DESCRIPTION
                "An administratively-assigned name for this managed
                node.  By convention, this is the node's fully-qualified
                domain name.  If the name is unknown, the value is
                the zero-length string."
        ::= { system 5 }
   ...

.. Things to talk about ^

  The `SNMPv2-MIB`, I am going to use for the example purposes, captures some
  basic information of the system. Let's pick the `sysName` object for the sake
  of simplicity. This object just reports system name, as assigned by the
  administrator.

Workflow: compile MIB into Python
---------------------------------

.. code-block:: bash

   $ mibdump --destination-format pysnmp --destination-template \
       pysnmp/mib-instrumentation/managed-objects-instances.j2 SNMPv2-MIB
   $ ls -l SNMPv2-MIB.py
   -rw-r--r--   1 ietingof  staff     16839 Jul 24 07:54 SNMPv2-MIB.py

Looking inside the `SNMPv2-MIB.py`:

.. code-block:: python

   ...
   class SysnameObjectInstance(MibScalarInstance):
       def readTest(self, varBind, **context):
           # Put your code here
           MibScalarInstance.readTest(self, varBind, **context)

       def readGet(self, varBind, **context):
           # Put your code here
           MibScalarInstance.readGet(self, varBind, **context)
   ...

.. Things to talk about ^

  So the task is to serve Redfish `HostName` as SNMP `sysName`. The first step
  toward this is to compile SNMP MIB into Python boilerplate code.

  Compiled MIB has all the managed objects each exposing a bunch of hooks
  reflecting MIB instrumentation workflow.

  For the task we are currently at, we are only interested in the *read* hooks.

Workflow: add glue code
-----------------------

.. code-block:: python

    REST_API_URL = 'http://demo.snmplabs.com/redfish/v1/Systems/437XR1138R2'

    executor = concurrent.futures.ThreadPoolExecutor()

    def readGet(self, (name, value), **context):
        cbFun = context['cbFun']

        def done_callback(future):
            rsp = future.result()
            value = self.syntax.clone(rsp['HostName'])
            cbFun((name, value), **context)

        future = executor.submit(load_url, REST_API_URL)

        future.add_done_callback(done_callback)

.. Things to talk about ^

  To obtain Redfish `HostName` we can just call `requests` or any other HTTP client
  from a thread pool to ensure non-blocking behaviour.

  Once the read value comes from the REST API call, we pass it to the SNMP agent's
  callback function.

  This allows for highly concurrent operation, what can be crucial considering
  potentially heavy and slow REST API calls and typically short SNMP manager
  timeout.

Workflow: stand up SNMP agent
-----------------------------

Configure SNMP Command Responder:

.. code-block:: bash

   $ pip install snmpresponder
   $ cp SNMPv2-MIB::sysName.py /etc/snmpresponder/managed-objects/
   $ snmpresponderd

And query it:

.. code-block:: bash

   $ snmpget -v2c -c public localhost SNMPv2-MIB::sysName.0
   SNMPv2-MIB::sysName.0 = STRING: web483

.. Things to talk about ^

  The SNMP Command Responder tool can consume such Pythonized MIBs and readily
  serve the data they produce over SNMPv1/v2c and SNMPv3 including all encryption
  features.

  MIB deployment is simple: just place your MIB implementation into
  a directory where SNMP Command Responder could reach it.

  Or you could pack your MIB implementation into a pip-installable
  package for easier distribution.

Why it all matters
------------------

* SNMP is still widely used in monitoring
* The "snmpresponder" tool as a universal mediation
* Highly concurrent due to asynchronous design

.. Things to talk about ^

  Despite many shortcomings and many attempt to displace SNMP, it's still in
  wide use.

  The tool set I am presenting here aims at quick and easy mediation between
  practically any data source and existing SNMP management software.

  Running asynchronously, the SNMP Command Responder tool should be able to
  scale reasonably well especially on slow data sources and/or highly concurrent
  SNMP queries.

Thank you
---------

* http://snmplabs.com/snmpresponder
* https://github.com/etingof/snmpresponder

