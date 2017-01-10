

Horror stories of IoT security
==============================

*by Ilya Etingof, Red Hat Product Security*

Agenda
======

* IoT today and tomorrow
* Components and supply chain
* Security challenges and attack surfaces
* Attacks analysis
* Lessons learnt

The Things
==========

* **Small, inexpensive computers**

.. nextslide::

* Small, inexpensive computers
* **With sensors/actuators**

.. nextslide::

* Small, inexpensive computers
* With sensors/actuators
* **Communicating over network**

The new dangers
===============

* **Not just data loss**

.. nextslide::

* Not just data loss
* **Things are embedded into physical world**

.. nextslide::

* Not just data loss
* Things are embedded into physical world
* **We may not notice them**

.. nextslide::

* Not just data loss
* Things are embedded into physical world
* We may not notice them
* **But they are designed to watch us**

.. nextslide::

* Not just data loss
* Things are embedded into physical world
* We may not notice them
* But they are designed to watch us
* **And they are massively insecure**

Dreams come true
================

* **Envisioned by Sci-Fi authors**

.. nextslide::

* Envisioned by Sci-Fi authors
* **Smart phones by Arthur C. Clarke in 1974**

.. nextslide::

* Envisioned by Sci-Fi authors
* Smart phones by Arthur C. Clarke in 1974
* **Smart homes by Ray Bradbury in 1950**

.. nextslide::

* Envisioned by Sci-Fi authors
* Smart phones by Arthur C. Clarke in 1974
* **Smart homes by Ray Bradbury in 1950**

  * *There Will Come Soft Rains*

Today's Things
==============

* **RFID**

.. figure:: rfid.jpg
   :scale: 90 %
   :align: center

.. nextslide::

* **Wearable computers**

.. figure:: nike-fuel-band.jpg
   :scale: 50 %
   :align: center

.. nextslide::

* **Wearable computers**

.. figure:: google-glass.jpg
   :scale: 50 %
   :align: center

.. nextslide::

* Smart homes: **Smart bulb**

.. figure:: smart-bulb.jpg
   :scale: 60 %
   :align: center

.. nextslide::

* Smart homes: **Smart fridge**

.. figure:: smart-refrigerator.jpg
   :scale: 70 %
   :align: center

.. nextslide::

* Smart homes: **Smart thermostat**

.. figure:: nest-learning-thermostat.jpg
   :scale: 50 %
   :align: center

.. nextslide::

* Smart homes: **Personal assistant**

.. figure:: amazon-echo.jpg
   :scale: 80 %
   :align: center

.. nextslide::

* Smart homes: **Dash button**

.. figure:: amazon-button.png
   :scale: 90 %
   :align: center

.. nextslide::

* **Flying robots**

.. figure:: amazon-delivery-drone.jpg
   :scale: 15 %
   :align: center

.. nextslide::

* **Flying robots**

  * **Autonomous GPS navigation**

.. nextslide::

* **Flying robots**

  * Autonomous GPS navigation
  * **Obstacle avoidance by sonars and cameras**

.. figure:: drone-flying.jpg
   :scale: 70 %
   :align: center

.. nextslide::

* **Flying robots**

  * Obstacle avoidance by sonars and cameras
  * Autonomous GPS navigation
  * **Air traffic control**

.. nextslide::

* **Medical**

  * **Insulin pump**

.. nextslide::

* **Medical**

  * Insulin pump
  * **Pacemaker**

.. nextslide::

* **Personal**

  * **Smart brush**

.. figure:: smart-brush.jpg
   :scale: 100 %
   :align: center

.. nextslide::

* **Personal**

  * **Smart mattress**

.. figure:: smart-mattress.png
   :scale: 70 %
   :align: center

.. nextslide::

* **Relationships**

.. nextslide::

* **Relationships**

  * **Big technology driver**

.. figure:: kissenger.jpg
   :scale: 70 %
   :align: center

.. nextslide::

* **Relationships**

  * **Would you marry a robot?**

.. figure:: love-and-sex-with-robots-book.jpg
   :scale: 80 %
   :align: center

Future IoT
==========

* **Autonomous devices**

.. nextslide::

* **Autonomous devices**

  * **Context awareness**

.. nextslide::

* **Autonomous devices**

  * Context awareness
  * **Independent reasoning**

.. nextslide::

* **Autonomous devices**

  * Context awareness
  * Independent reasoning
  * **Interoperability**

IoT components
==============

* **Sensors / actuators**

.. nextslide::

* **Sensors / actuators**

  * **Motors, valves...**

.. nextslide::

* **Sensors / actuators**

  * Motors, valves...
  * **Temperature, light, magnetic...**

.. nextslide::

* **Sensors / actuators**

.. figure:: iot-sensors.png
   :scale: 90 %
   :align: center

.. nextslide::

* Sensors / actuators
* **Boards**

  * **Low-power SoC on a PCB**

.. nextslide::

* Sensors / actuators
* **Boards**

  * **MCU (Arduino, Pinoccio, CubieBoard)**

.. figure:: arduino-uno-pcb.jpg
   :scale: 50 %
   :align: center

.. nextslide::

* Sensors / actuators
* **Boards**

  * **Single-board computers**

    * *Raspberry Pi, Beagle Board, Electric Imp, Gumstix*

.. nextslide::

* Sensors / actuators
* **Boards**

  * **Single-board computers**

.. figure:: raspberry-pi-pcb.jpg
   :scale: 70 %
   :align: center

.. nextslide::

* Sensors / actuators
* Boards
* **IoT gateways**

.. figure:: dell-edge-gateway-5000.png
   :scale: 50 %
   :align: center

.. nextslide::

* Sensors / actuators
* Boards
* **IoT gateways**

  * **Protocols adaptation**

.. nextslide::

* Sensors / actuators
* Boards
* **IoT gateways**

  * Protocols adaptation
  * **Data aggregation**

.. nextslide::

* Sensors / actuators
* Boards
* Protocol gateways / data aggregators
* **IoT platforms**

.. nextslide::

* Sensors / actuators
* Boards
* Protocol gateways / data aggregators
* **IoT platforms**

  * **Cloud Service Providers**

.. nextslide::

* Sensors / actuators
* Boards
* Protocol gateways / data aggregators
* **IoT platforms**

  * **Cloud Service Providers**

    *Amazon, Azure and many others*

.. nextslide::

* Sensors / actuators
* Boards
* Protocol gateways / data aggregators
* **IoT platforms**

  * Cloud Service Providers
  * **Support data feed and control protocols**

.. nextslide::

* Sensors / actuators
* Boards
* Protocol gateways / data aggregators
* **IoT platforms**

  * Cloud Service Providers
  * Support data feed and control protocols
  * **Offer data storage and analytics**

.. nextslide::

* Sensors / actuators
* Boards
* Protocol gateways / data aggregators
* **IoT platforms**

  * Cloud Service Providers
  * Support data feed and control protocols
  * Offer data storage and analytics
  * **Facilitate data consumption (REST API, Web UI)**

IoT supply chain
================

* **Chips manufacturers**

.. nextslide::

* Chips manufacturers
* **Boards manufacturers**

  * **PCB manufactured by 4-5 companies**

.. nextslide::

* Chips manufacturers
* **Boards manufacturers**

  * PCB manufactured by 4-5 companies
  * **Shipped with Board Support Packages (SDK)**

.. nextslide::

* Chips manufacturers
* Boards manufacturers
* **Original Design manufacturers**

  * **Design and manufacture the product**

.. nextslide::

* Chips manufacturers
* Boards manufacturers
* **Original Design manufacturers**

  * Design and manufacture the product
  * **Crowdsourced startups**

.. nextslide::

* Chips manufacturers
* Boards manufacturers
* **Original Design manufacturers**

  * Design and manufacture the product
  * Crowdsourced startups
  * **Buy/own cloud infrastructure**

.. nextslide::

* Chips manufacturers
* Boards manufacturers
* **Original Design manufacturers**

  * Design and manufacture the product
  * Crowdsourced startups
  * Buy/own cloud infrastructure
  * **Provide SDKs, Web UI, mobile apps**

.. nextslide::

* Chips manufacturers
* Boards manufacturers
* Original Design manufacturers
* **Cloud Service Providers**

  * **Large, established businesses**

.. nextslide::

* Chips manufacturers
* Boards manufacturers
* Original Design manufacturers
* **Cloud Service Providers**

  * Large, established businesses
  * **Analytics, automation, reporting, Web UI**

.. nextslide::

* Chips manufacturers
* Boards manufacturers
* Original Design manufacturers
* Cloud Service Providers
* **Original Equipment Manufacturers**

  * **Brand, marketing, sales**

.. nextslide::

* Chips manufacturers
* Boards manufacturers
* Original Design manufacturers
* Cloud Service Providers
* **Original Equipment Manufacturers**

  * **Brand, marketing, sales**

    * *Belkin, SmartThings, WeMo, Linksys*

.. nextslide::

* Chips manufacturers
* Boards manufacturers
* Original Design manufacturers
* Cloud Service Providers
* **Original Equipment Manufacturers**

  * Brand, marketing, sales
  * **Warranty, customer support**

Insecurity factors
==================

* **IoT is hot**

  * **Low-barrier entry for ODM**

.. nextslide::

* **IoT is hot**

  * Low-barrier entry for ODM
  * **Many industries suddenly enter software development**

.. nextslide::

* **IoT is hot**

  * Low-barrier entry for ODM
  * Many industries suddenly enter software development
  * **Originally off-line products become networked**

.. nextslide::

* **IoT is hot**

  * Low-barrier entry for ODM
  * Many industries suddenly enter software development
  * Originally off-line products become networked
  * **Competition presses ODM/OEM to release fast**

.. nextslide::

* IoT is hot
* **IoT is cool**

  * **High demand for cool stuff**

.. nextslide::

* IoT is hot
* **IoT is cool**

  * High demand for cool stuff
  * **Customers are unaware of security risks**

.. nextslide::

* IoT is hot
* IoT is cool
* **IoT is personal**

  * **Massive amount of private data**

.. nextslide::

* IoT is hot
* IoT is cool
* **IoT is personal**

  * Massive amount of private data
  * **Direct impact on humans**

.. nextslide::

* IoT is hot
* IoT is cool
* IoT is personal
* **IoT is messy**

  * **No experience in IT security**

.. nextslide::

* IoT is hot
* IoT is cool
* IoT is personal
* **IoT is messy**

  * No experience in IT security
  * **Software touched by many teams**

.. nextslide::

* IoT is hot
* IoT is cool
* IoT is personal
* IoT is messy
* **IoT is vulnerable**

  * **MCU is weak for public key crypto**

.. nextslide::

* IoT is hot
* IoT is cool
* IoT is personal
* IoT is messy
* **IoT is vulnerable**

  * MCU is weak for public key crypto
  * **Physical access may be easy**

.. nextslide::

* IoT is hot
* IoT is cool
* IoT is personal
* IoT is messy
* **IoT is vulnerable**

  * MCU is weak for public key crypto
  * Physical access may be easy
  * **Widespread use of outdated software**

.. nextslide::

* IoT is hot
* IoT is cool
* IoT is personal
* IoT is messy
* IoT is vulnerable
* **Mitigation is hard**

  * **Hard to regulate import of insecure appliances**

.. nextslide::

* IoT is hot
* IoT is cool
* IoT is personal
* IoT is messy
* IoT is vulnerable
* **Mitigation is hard**

  * Hard to regulate import of insecure appliances
  * **Hard to get infected devices off the network**

.. nextslide::

* IoT is hot
* IoT is cool
* IoT is personal
* IoT is messy
* IoT is vulnerable
* **Mitigation is hard**

  * Hard to regulate import of insecure appliances
  * Hard to get infected devices off the network
  * **Hard to get owners upgrading firmware**

.. nextslide::

* IoT is hot
* IoT is cool
* IoT is personal
* IoT is messy
* IoT is vulnerable
* **Mitigation is hard**

  * Hard to regulate import of insecure appliances
  * Hard to get infected devices off the network
  * Hard to get owners upgrading firmware
  * **Hard to recover from device takeover**

Major attack vectors
====================

* **Device**

  * **Hardcoded passwords / API keys**

.. nextslide::

* **Device**

  * Hardcoded passwords / API keys
  * **Forgotten services / vendor backdoors**

.. nextslide::

* **Device**

  * Hardcoded passwords / API keys
  * Forgotten services / vendor backdoors
  * **Code injection vulnerabilities**

.. nextslide::

* **Device**

  * Hardcoded passwords / API keys
  * Forgotten services / backdoors
  * Code injection vulnerabilities
  * **Wireless networks vulnerabilities**

.. nextslide::

* **Device**

  * Hardcoded passwords / API keys
  * Forgotten services / backdoors
  * Code injection vulnerabilities
  * Wireless networks vulnerabilities
  * **Unsecured hardware interfaces**

.. nextslide::

* Device
* **Platform**

  * **Web UI and mobile apps vulnerabilities**

.. nextslide::

* Device
* **Platform**

  * Web UI and mobile apps vulnerabilities
  * **Insecure network communication**

.. nextslide::

* Device
* **Platform**

  * Web UI and mobile apps vulnerabilities
  * Insecure network communication
  * **Data submission and control API vulnerabilities**

.. nextslide::

* Device
* **Platform**

  * Web UI and mobile apps vulnerabilities
  * Insecure network communication
  * Data submission and control API vulnerabilities
  * **Unsecured data at rest**

Attacks analysis
================

* Smart plug
* IoT botnet
* Connected car
* Smart lights

Attack analysis: smart plug
===========================

.. figure:: kankun-smart-plug.png
   :scale: 60 %
   :align: center

Features
========

* Wall socket
* Connects to your Wi-Fi network
* You can turn it on/off from a smartphone

Smartphone app
==============

.. figure:: kankun-mobile-app.png
   :scale: 60 %
   :align: center

First look
==========

* `nmap` reports Linux
* Open telnet and ssh ports
* ESP8266 SoC inside

Traffic analysis
================

* UDP broadcast traffic on WiFi
* Payload structure looks like AES blobs

Protocol analysis
=================

* Decompile Android app with `apktool`
* Recover the protocol

.. code-block:: bash

    lan_phone%MAC%PASSWORD%open%request
    lan_device%MAC%PASSWORD%confirm#CHALLENGE%rack
    lan_phone%MAC%PASSWORD%confirm#CHALLENGE%request
    lan_device%MAC%PASSWORD%open%rack

Crypto key recovery
===================

* App calls `libNDK_03.so`
* Running `strings` over `libNDK_03.so` reveals encryption key

.. code-block:: bash

    $ strings libNDK_03.so
    ...
    UUPx((
    Zw–
    fdsl;mewrjope456fds4fbvfnjwaugfo
    java/lang/String
    ...

Hijacking the plug
==================

* Wait for broadcast `27431/udp`
* AES decode payload with the key
* Figure out `MAC` and `PASSWORD`
* Communicate with the plug and own it!

Server analysis
===============

* `tcpdump` shows outgoing TCP connection
* To some server in China
* Protocol is the same

Hijacking more plugs
====================

* `MAC` is easily guessable
* Majority of users leave default `PASSWORD`
* Own plugs all over the globe!

Shell injection
===============

* Control agent runs as root
* Invokes `system()`
* Not sanitizing protocol payload
* Run your code on plugs

Exploit potential
=================

* DDoS targets on Internet
* Attack targets on Wi-Fi network
* Distributed spam
* Disrupt/destroy appliances by flipping power on/off

Lessons learnt
==============

* Never hardcode crypto keys
* Enforce setting password
* Be paranoid about interpreting input

Attack analysis: IoT worms
==========================

* Many known: BASHLITE, Linux.Darlloz, Remaiten
* Hajime: Mirai successor
* Analysed by Sam Edwards and Ioannis Profetis

Botnet architecture
===================

.. figure:: botnet-architecture.gif
   :scale: 90 %
   :align: center

Image by `JeroenT96 <https://commons.wikimedia.org/w/index.php?curid=47443899>`_

Staged infection
================

0. Find victim and break in
1. Download P2P program from attacker
2. Join P2P network and wait for instructions

Find victim and break in
========================

* Scan public Internet for port 23/tcp
* Brute-force login/password

Upload file-transfer tool
=========================

.. code-block:: bash

   $ echo "\x7f\x45\x4c\x46\x0" >> /var/tmp/.~
   ...
   $ exec /var/tmp/.~

Download malware
================

* Connect back to attacker
* Download P2P program
* Join P2P network

Mounting an attack
==================

* Receive code updates
* Receive C&C directions

DDoS attack
===========

* HTTP requests
* TCP SYN/ACK floods
* DNS, UDP floods

.. nextslide::

.. figure:: mirai-botnet-attack.gif
   :scale: 80 %
   :align: center

Image by `Joey Devilla <http://www.globalnerdy.com/2016/10/25/last-fridays-iot-botnet-attack-and-internet-outages-explained-for-non-techies/>`_

Mirai DDoS scale
================

* Mirai infected 380K+ devices
* From 164 countries
* On 21.10.2016 took down Amazon, Twitter, PayPal and others

Hosts
======

* Web cameras
* Baby monitors
* Home routers

Lessons learnt
==============

* Enforce non-default password
* Disallow Internet access
* Disable insecure services

Fun fact
========

The `Linux.Wifatch` malware is known to:

* Infect home routers
* Shutdown telnet service
* Change default password

Attack analysis: connected car
==============================

Car connections
===============

* Vehicle to vehicle (802.11p)
* Vehicle to road (802.11p)
* Vehicle to device (NFC, Wi-Fi, USB, BT)

Car attack vectors
==================

* Infotainment systems
* Mobile apps
* OBDC2 port



Attack analysis: smart lights
=============================

* Philips Hue LED bulbs
* Most popular smart light
* Millions sold

.. figure:: philips-hue-bulbs.png
   :scale: 60 %
   :align: center

* By  Eyal Ronen, Colin O’Flynn, Adi Shamir and Achi-Or Weingarten (http://iotworm.eyalro.net/)

Features
========

* LED bulbs, switches and bridge join PAN
* Can turn on/off, change luminocity, color
* Also through a smartphone app over Internet

Bulb's hardware
===============

* The Atmel ATmega2564RFR2 SoC
* MCU, flash, RAM, AES accellerator, 802.15.4 tranciever
* Anti debug fuses to disallow flash read

ZigBee stack
============

* Components reside in ZigBee PAN

.. figure:: zigbee-protocol-stack.png
   :scale: 100 %
   :align: center

ZigBee Touchlink vuln
=====================

* ZigBee packets are encrypted with a unique PAN key
* To share PAN key with new nodes, master key is used
* Single master key is hardcoded into all ZigBee prodicts
* Master key was leaked in 2015

ZigBee Light Link vuln
======================

* Additional proximity check (< 1m)
* By measuring RSSI

.. nextslide::

* Bug in Atmel's BitCloud library
* Allows factory reset at any distance (50-150m)

.. nextslide::

* Bulb in factory configuration
* Tries to join any ZLL or non-ZLL PAN
* Non-ZLL profile does not require proximity test

ZigBee OTA update
=================

* Bulb supports over-the-air firmware upgrade
* Boot and upgrade images are encrypted with symmetric keys

Bootloader side channel attack
==============================

* Brute forced bootloader over sample signatures
* Collected power consumption patterns (DPA/CPA)
* Recovered encryption keys, build compromised firmware

Warflying
=========

* Mounted infecting hardware on a drone
* Flyed by running bulbs, uploading malicious firmware
* Infected bulb spreads the worm

Exploit potential
=================

* Worm propagation is unstoppable
* Bricking attack
* 2.4GHz network jamming

Lessons learnt
==============

* Never hardcode encryption keys
* Security through obscurity does not work





Attacks on hardware
===================

* UART/USB console
* Read flash data
* Differential Power analysis
* Correlation Power analysis




Advice for developers
=====================

Advice for users
================

