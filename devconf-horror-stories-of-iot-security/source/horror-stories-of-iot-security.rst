
Horror stories of IoT security
==============================

*by Ilya Etingof, Red Hat Product Security*

Agenda
======

* **Look at IoT phenomena**

.. nextslide::

* Look at IoT phenomena
* **Through the eyes of security researcher**

.. nextslide::

* Look at IoT phenomena
* Through the eyes of security researcher
* **To understand the risks and take action**

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

.. nextslide::

* Not just data loss
* Things are embedded into physical world
* We may not notice them
* But they are designed to watch us
* And they are massively insecure

  * *Let's see how...*

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

.. nextslide::

* Envisioned by Sci-Fi authors
* Smart phones by Arthur C. Clarke in 1974
* Smart homes by Ray Bradbury in 1950
* **Self-replicating robots by Karel Čapek in 1920**

Things [we think] we buy
========================

* Smart homes: **Smart bulb**

.. figure:: smart-bulb.jpg
   :scale: 60 %
   :align: center

.. nextslide::

* Smart homes: **Smart thermostat**

.. figure:: nest-learning-thermostat.jpg
   :scale: 50 %
   :align: center

.. nextslide::

* Smart homes: **Smart pot**

.. figure:: smart-pot.jpg
   :scale: 70 %
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

* **Medical things**

  * Insulin pumps
  * Pacemakers

.. nextslide::

* **Weird things**

  * **Smart brush**

.. figure:: smart-brush.jpg
   :scale: 100 %
   :align: center

.. nextslide::

* **Weird things**

  * **Smart mattress**

.. figure:: smart-mattress.png
   :scale: 70 %
   :align: center

.. nextslide::

* **Weird things**

  * **Doggy phone**

.. figure:: doggy-phone.jpg
   :scale: 90 %
   :align: center

.. nextslide::

* **Creepy things**

  * **Kissenger**

.. figure:: kissenger.jpg
   :scale: 70 %
   :align: center

.. nextslide::

* **Creepy things**

  * **Would you marry a robot?**

.. figure:: love-and-sex-with-robots-book.jpg
   :scale: 80 %
   :align: center

Things we buy
=============

.. figure:: hacked-appliances.jpg
   :scale: 80 %
   :align: center

The story of Hajime
===================

Hajime lives in here:

.. figure:: dahua-ip-camera.png
   :scale: 99 %
   :align: center

.. nextslide::

* On 21.10.2016 Amazon, Twitter, PayPal went down...
* Hajime: Mirai successor
* Analysed by Sam Edwards and Ioannis Profetis

Breeding a botnet
=================

* **Implant malicious software into many Things**

.. nextslide::

* Implant malicious software into many Things
* **To carry out distributed attacks**

Find victim and break in
========================

* Scan public Internet for port 23/tcp
* Brute-force login/password

Upload file-transfer tool
=========================

.. code-block:: bash

   $ echo "\x7f\x45\x4c\x46\x0" >> /var/tmp/.loader
   ...
   $ exec /var/tmp/.loader

Download malware
================

* **Connects back to attacking node**

.. nextslide::

* Connects back to attacking node
* **Downloads P2P program**

.. nextslide::

* Connects back to attacking node
* Downloads P2P program
* **Joins P2P network**

.. nextslide::

* Connects back to attacking node
* Downloads P2P program
* Joins P2P network
* **Keeps propagating**

Live botnet
===========

.. figure:: botnet-architecture.gif
   :scale: 90 %
   :align: center

Image by `JeroenT96 <https://commons.wikimedia.org/w/index.php?curid=47443899>`_

Mounting an attack
==================

* **Receive code updates**

.. nextslide::

* Receive code updates
* **Receive C&C directions**

DDoS attack
===========

* **Flood of**

  * *HTTP requests*
  * *TCP SYN/ACK packets*
  * *DNS, UDP packets*

.. nextslide::

.. figure:: mirai-botnet-attack.gif
   :scale: 80 %
   :align: center

Image by `Joey Devilla <http://www.globalnerdy.com/2016/10/25/last-fridays-iot-botnet-attack-and-internet-outages-explained-for-non-techies/>`_

Mirai DDoS scale
================

* Infected 380K+ devices
* From 164 countries

Fun fact
========

* The `Linux.Wifatch` malware is known to:

  * *Infect home routers*
  * *Shutdown telnet service*
  * *Change default password*

Attack post-mortem
==================

* Manufacturer's failure
* Upcoming attacks against 80/tcp

.. nextslide::

* This was an attack against a Linux box
* Let's take closer look at IoT

What's inside an IoT system?
============================

* **No rigid architecture**

.. nextslide::

* **Sensors / actuators**

.. figure:: iot-sensors.png
   :scale: 90 %
   :align: center

.. nextslide::

* Sensors / actuators
* **Embedded system**

  * **Single-board computers**

    * *Raspberry Pi*
    * *Beagle Board*
    * *Electric Imp*
    * *Gumstix*

.. nextslide::

* Sensors / actuators
* **Embedded systems**

  * **Single-board computers**

.. figure:: raspberry-pi-pcb.jpg
   :scale: 70 %
   :align: center

.. nextslide::

* Sensors / actuators
* **Embedded systems**

  * **Microcontrollers**
   * *Arduino*
   * *Pinoccio*
   * *CubieBoard*
   * ...

.. nextslide::

* Sensors / actuators
* **Embedded systems**

.. figure:: arduino-uno-pcb.jpg
   :scale: 50 %
   :align: center

.. nextslide::

* Sensors / actuators
* Embedded systems
* **Gateways**

.. figure:: dell-edge-gateway-5000.png
   :scale: 50 %
   :align: center

.. nextslide::

* Sensors / actuators
* Embedded systems
* Gateways
* **Data platform**

.. nextslide::

* Sensors / actuators
* Embedded systems
* Gateways
* **Data platform**

  * **Cloud Service Providers**

.. nextslide::

* Sensors / actuators
* Embedded systems
* Gateways
* **Data platform**

  * **Cloud Service Providers**

      * *AWS IOT*
      * *Google Cloud IOT*
      * *Microsoft Azure IoT Suite*
      * *...*

.. nextslide::

* Let's look at another attack
* That involves the cloud

The story of a plug
===================

.. figure:: kankun-smart-plug.jpg
   :scale: 30 %
   :align: center

*Security research by Matthew Garrett and others*

.. nextslide::

* **Just a wall socket**

.. nextslide::

* Just a wall socket
* **You can turn power on/off from a smartphone**

.. nextslide::

* Just a wall socket
* You can turn power on/off from a smartphone
* **May be not only you...? ;-)**

Peek at network traffic
=======================

* UDP broadcast traffic on Wi-Fi network
* Payload looks like AES blobs

What's inside the app?
======================

* Decompiled Android app with `apktool`
* Recovered the protocol

.. code-block:: bash

    lan_phone%MAC%PASSWORD%open%request
    lan_device%MAC%PASSWORD%confirm#CHALLENGE%rack
    lan_phone%MAC%PASSWORD%confirm#CHALLENGE%request
    lan_device%MAC%PASSWORD%open%rack

Let's peek at crypto
====================

* App calls `libNDK_03.so`
* Let's run `strings` on `libNDK_03.so`
* Could one of these strings be an encryption key?

.. code-block:: bash

    $ strings libNDK_03.so
    ...
    UUPx((
    Zw–
    fdsl;mewrjope456fds4fbvfnjwaugfo
    java/lang/String
    ...

Brute force key
===============

* Capture a broadcast packet to `27431/udp`
* Try to AES decode with a candidate key
* Clear text reveals? This is the key indeed!

Remote control feature
======================

* `tcpdump` shows outgoing TCP connection
* To some server in China

Hijack plugs
============

* `MAC` is easily brute-forcible
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

Attack post-mortem
==================

* Hardcoded key
* Plugs enumeration flaw
* Default password

Who cares about security?
=========================

* Let's see...

IoT supply chain
================

* **IoT is a sophisticated high-tech**

.. nextslide::

* IoT is a sophisticated high-tech
* **Duct-taped together**

.. nextslide::

* IoT is a sophisticated high-tech
* Duct-taped together
* **ASAP**

.. nextslide::

* IoT is a sophisticated high-tech
* Duct-taped together
* ASAP
* **Fertile soil for bug breeding...**

.. nextslide::

* Chips manufacturers
* Boards manufacturers
* Original Design manufacturers
* Cloud Service Providers
* Original Equipment Manufacturers

The weakest link
================

* **Original Design manufacturers**

  * **Design and manufacture the product**

.. nextslide::

* **Original Design manufacturers**

  * Design and manufacture the product
  * **Many small companies from China**

.. nextslide::

* **Original Design manufacturers**

  * Design and manufacture the product
  * Many small companies from China
  * **Produce [insecure] software fast**

Who cares about security?
=========================

* **OEMs may [not] do security**

  * **Just a checkbox**

.. nextslide::

* **OEMs may [not] do security**

  * Just a checkbox
  * **No code to work with**

.. nextslide::

* **OEMs may [not] do security**

  * Just a checkbox
  * No code to work with
  * **Forward disclosures to a vendor**

.. nextslide::

* **OEMs may [not] do security**

  * Just a checkbox
  * No code to work with
  * Forward disclosures to a vendor
  * **Or sue security researcher**

Factors of insecurity
=====================

* **IoT is hot**

  * *Modern forks must have mobile apps!*

.. figure:: smart-fork.jpg
   :scale: 90 %
   :align: center

.. nextslide::

* **IoT is cool**

  * *What a gadget! I must have it NOW!*

.. figure:: egg-counter.jpg
   :scale: 80 %
   :align: center

.. nextslide::

* **IoT is paradoxical**

  * **We poke fun at smart devices...**

.. nextslide::

* **IoT is paradoxical**

  * We poke fun at smart devices...
  * **...and happily buy them**

.. nextslide::

* **IoT is easy**

  * *Just add a $5 Arduino to a coffee maker*

.. nextslide::

* **IoT is easy**

  * Just add a $5 Arduino to a coffee maker
  * *...and we are in IoT business!*

.. nextslide::

* **IoT is easy**

  * Just add a $5 Arduino to a coffee maker
  * ...and we are in IoT business!
  * *Hmm, our coffee maker demands a ransom...*

.. nextslide::

* **IoT is easy**

  * Just add a $5 Arduino to a coffee maker
  * ...and we are in IoT business!
  * Hmm, our coffee maker demands a ransom...
  * *What does "security engineering" mean?*

.. nextslide::

* **IoT is messy**

  * **Layers of software**

.. figure:: spaghetti-monster.jpg
   :scale: 100 %
   :align: center

.. nextslide::

* **IoT is messy**

  * Layers of software
  * **From uncoordinated teams**

.. nextslide::

* **IoT is messy**

  * Layers of software
  * From uncoordinated teams
  * **Went through a long supply chain**

.. nextslide::

* **IoT is misunderstood**

  * **It is a general purpose computer**

.. nextslide::

* **IoT is misunderstood**

  * It is a general purpose computer
  * **Disguised as an appliance**

.. nextslide::

* **IoT is misunderstood**

  * It is a general purpose computer
  * Disguised as an appliance
  * **Manufactured as an appliance, not software**

.. nextslide::

* **IoT is vulnerable**

  * **No CPU power for public key crypto**
  * Physical access may be easy

.. nextslide::

* **IoT is vulnerable**

  * No CPU power for public key crypto
  * **Physical access may be easy**

.. nextslide::

* **IoT is vulnerable**

  * No CPU power for public key crypto
  * Physical access may be easy
  * **Low-entropy system**

.. nextslide::

* **IoT is powerful**

  * **Billions of devices**

.. nextslide::

* **IoT is powerful**

  * Billions of devices
  * **Teraflops of processing power if harnessed**

.. nextslide::

* **Mitigation is hard**

  * **Owners misunderstand risks and do not care**

.. nextslide::

* **Mitigation is hard**

  * Owners misunderstand risks and do not care
  * **Hard for vendors to ship patches**

.. nextslide::

* **Mitigation is hard**

  * Owners misunderstand risks and do not care
  * Hard for vendors to ship patches
  * **Hard to regain control over taken over device**

.. nextslide::

* **Mitigation is hard**

  * Owners misunderstand risks and do not care
  * Hard for vendors to ship patches
  * Hard to regain control over taken over system
  * **Hard to get infected devices off the network**

.. nextslide::

* **Mitigation is hard**

  * Owners misunderstand risks and do not care
  * Hard for vendors to ship patches
  * Hard to regain control over taken over system
  * **Hard to get infected devices off the network**

    * *http://www.shodan.io*

Who cares about security?
=========================

Let's look at premium gadgets...

The story of smart lights
=========================

* **Philips Hue LED bulbs**

.. figure:: philips-hue-bulbs.png
   :scale: 70 %
   :align: center

*Researched by Eyal Ronen, Colin O’Flynn, Adi Shamir and Achi-Or Weingarten (http://iotworm.eyalro.net/)*

.. nextslide::

* Philips Hue LED bulbs
* **Most popular smart light**

.. nextslide::

* Philips Hue LED bulbs
* Most popular smart light
* **Millions sold**

Features
========

* **Can turn on/off, change luminosity, color**

.. nextslide::

* Can turn on/off, change luminosity, color
* **Through local switches, smartphone app over Internet**

Inside the bulb
===============

* Armel SoC

  * *Microprocessor, RAM, flash*
  * *Hardware AES accelerator*
  * *Zigbee network*

The lighting system
===================

* **Bulbs, switches, gateway in ZigBee network**

.. nextslide::

* Bulbs, switches, gateway in ZigBee network
* **Gateway**

  * *Also in Wi-Fi network*
  * *Supports REST API for each bulb*
  * *Connects to cloud*

ZigBee vulnerability
====================

* **Network traffic encrypted with PAN key**

.. nextslide::

* Network traffic encrypted with PAN key
* **PAN key is send to new nodes encrypted with master key**

.. nextslide::

* Network traffic encrypted with PAN key
* PAN key is send to new nodes encrypted with master key
* **Master key is leaked in 2015**

Light Link vulnerability
========================

* **Additional proximity check**

  * *By measuring RSSI*

.. nextslide::

* Additional proximity check
* **A bug makes bulb resetting**

.. nextslide::

* Additional proximity check
* A bug makes bulb resetting
* **And skipping proximity check**

On-bulb code execution
======================

* **Only possible via firmware reflash**

.. nextslide::

* Only possible via firmware reflash
* **But firmware images are signed**

Side-channel attack
===================

* **Feed bootloader fake images**

.. nextslide::

* Feed bootloader fake images
* **While watching power consumption spikes**

.. nextslide::

* Feed bootloader fake images
* While watching power consumption spikes
* **Reveals firmware signing key**

Ultimate attack
===============

* **Built compromised firmware with a worm**

.. nextslide::

* Built compromised firmware with a worm
* **Flew a drone with infected bulb near ZigBee networks**

.. nextslide::

* Built compromised firmware with a worm
* Flew a drone with infected bulb near ZigBee networks
* **Uploading malicious firmware**

Exploit potential
=================

* **Taking over or bricking bulbs**

.. nextslide::

* Taking over or bricking bulbs
* **2.4GHz network jamming**

.. nextslide::

* Taking over or bricking bulbs
* 2.4GHz network jamming
* **Worm propagation is hard to stop**

Who cares about security?
=========================

* Hardcoded encryption key
* Security through obscurity never works

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
  * **Unsecured hardware interfaces**

.. nextslide::

* **Device**

  * Hardcoded passwords / API keys
  * Forgotten services / vendor backdoors
  * **Unsecured hardware interfaces**

    * *UART, SPI, I2O, JTAG*

.. nextslide::

* **Device**

  * Hardcoded passwords / API keys
  * Forgotten services / vendor backdoors
  * Unsecured hardware interfaces
  * **Code injection vulnerabilities**

.. nextslide::

* **Device**

  * Hardcoded passwords / API keys
  * Forgotten services / backdoors
  * Unsecured hardware interfaces
  * Code injection vulnerabilities
  * **Wireless networks vulnerabilities**

.. nextslide::

* Device
* **Platform**

  **Good old Web vulns**

    * *CSRF, XSS, SQL injection*
    * *SSL misconfiguration*

Advice for users
================

* Do not own IoT
* Research before you buy
* Prefer cloudless devices
* Research cloud data privacy policy
* Change passwords
* Apply updates
* Firewall, disable uPnP
* Setup a dedicated network for your IoT
* Disable unused features
* Be cautious when selling used IoT

Advice for developers
=====================

* Realize that you are not alone!
* Restrain from taking private data
* Force users to change password
* Never hardcode keys/passwords
* Encrypt data in motion and at rest
* Clean up before you ship (backdoors, debugging hooks)
* Follow secure IoT development practices (https://builditsecure.ly)
* Employ hackers on demand (http://bugcrowd.com)

Future IoT
==========

* **Things to become smarter**

  * **Learn and behave intelligently**

.. nextslide::

* **Things to become smarter**

  * Learn and behave intelligently
  * **Join brains**

