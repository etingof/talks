
Things are coming and humanity is in danger! In this talk I will
share the frightening observations of the risks that massive
adoption of IoT devices bring us.

We will look at the technology behind IoT and services it offers
through the eyes of security researcher.

The Things
==========

The term IoT is used to refer to hugely different devices -- from children's
toys to industrial automation. In the context of this talk, we will be mostly
looking at consumer devices which are very common and risky. Those things are
typically:

* small, inexpensive, low-power computers
* equipped with sensors and/or actuators
* being able to communicate with each other and with the Internet

The dangers
===========

Before the IoT era, computer glitches and cyber crime tended
to revolve around data - loss or leaks or modification. With the IoT
emerging, we are getting exposed to fundamentally new risks:

* Things have direct contact with and impact to the physical world, including humans
* We may not notice them, however they are numerous
* The Things are designed to help us what also means they have to watch us (by collecting
  huge amount of data)
* Things, as they stand now, are massively insecure

By way of this talk we will examine how Things work and how the manufacturing
process looks like what hopefully will give us more understanding why
modern Things are so insecure.

Dreams come true
================

The idea behind IoT is not new. Smart, computerized environment was
envisioned by sci-fi many years ago.

For example, in "There Will Come Soft Rains" story written by Ray Bradbury in 1950,
the reader is introduced to a computer-controlled house that cooks, cleans, and takes
care of virtually every need that a well-to-do US family could possibly have. The story
unfolds in 2026, that is in nine years from now.

Interestingly, Bradbury's smart home was quite reliable as it withstood a nuclear strike
and kept running its duties while standing in the midst of a ruined and lifeless town.

Almost a century ago, in his play recursively named "R.U.R", Karel Čapek scared the
public with a story of smart, self-replicating machines revolted against human masters.
He called them "robots", effectively coining the term first in popular culture
then to science and technology. So CR is a land of robots!

Things [we think] we buy
========================

Home automation is a hot topic for a long time. We are already beyond the features that
Bradbury was thinking about -- automatic lighting, heating, irrigation and monitoring is
here. But human imagination and (desire for comfort) proves to have no limits!

Nowdays one can have a personal home assistant that understands human speech. You
can instruct it to dim the lights and control the thermostat, maintain shopping list
and set alarms. You can tell it to tune into specific radio station or play the
music of your choice.

If you are not in mood to talk to your personal assistant, just press an Amazon Dash Button
and get stuff shipped to your home. Possibly by an Amazon PrimeAir delivery drone.

Then there are medical applications. Automatic insulin pumps and pacemakers are
already widely used.

And the weird stuff - computers are finding their ways into traditionally
low-tech things like hygiene items and sleeping gear.

Now, it can get creepy. It is no secret that relationships and sex are among
the big technology drivers. Of course IoT businesses address that demand.
Look at this remote kissing gadget!

The telepresence technology is frightening and amazing! Security vulnerabilities
in that area might be hilarious and tragic in equal measure.

In this talk I won't go any further down this topic. If you are interested, I
can refer you to this book and same-named international conference held in UK.

Things we buy
=============

These gadgets look sleek and appealing indeed. But the reality is frequently
different. Many highly motivated people are working around the clock to
harness the power of billions of Things and leverage it in their interests.

In many cases there is not much you can do about it.

The story of Hajime
===================

You may remember a day in October last year when many high-profile web sites
like Twitter, Amazon, PayPal went down for some time. Apparently, a network
of enslaved and harnessed Things, primarily DVRs and web cameras, stand behind
that attack.

The attacking software is dubbed Mirai, its code was open sourced and is
available at github. This story is about a slightly improved version of
Mirai caught in the wild and called Hajime.

Here is how it works.

The ultimate goal of attacker is to implant their software into as many
IoT devices as possible and be able to instruct them to carry out certain
operations, mostly DoS attacks.

The infection process starts from the attacking node scanned the Internet
in search for an open telnet port. Once it hit one, the attacker tried
to log in under dozens of factory default passwords.

If login succeeded and attacking node dropped into shell, it searched for
a writable filesystem (like /var) and echo'ed hex-escaped machine codes
into a local file. That gave attacker a small executable which, once run,
opened tcp connection back to attacking node and downloaded a large P2P
client binary. Then it joint a P2P network and started listening for further
instructions.

At the same time, infected node started scanning the Internet for the
purpose of further propagation.

Over time the described infection process helps building a huge,
self-propagating and remote controlled network of bots.

Once its master decided to mount an attack of specific kind, they
injected a "plugin" module along with a configuration into the P2P
network. The bots picked that up from P2P and run whatever code
their master wants to.

The attacks that Mirai was capable to carry out include HTTP, TCP, UDP and
DNS floods. Considering hundreds of thousands of nodes flooding a single target
simultaneously, it is no wonder that even high-profile sides went down.

Interestingly, researchers have observed many implementations of Linux
worms like Hajime in the wild. The worms naturally compete for hosts,
sometimes they become hostile to each other and try to kill or enslave
the competing worms.

Among those worms, the one that stands out is `Linux.Wifatch`. Its is
relatively harmless to its hosts, the only thing it does is that it
changes default root password and shuts down telnet daemon to prevent
infection.

Attack post-mortem
==================

Clearly, that attack won't be that successful if [unnecessary] telnet
service won't be running or credentials won't be that easy to brute force.
So this is where the manufacturer failed to provide even minimal security
to its product.

What's worth noting is that, unlike 80/tcp, port 23/tcp is not usually
port-forwarded on the firewalls, yet 380K+ devices were conscripted.
We may expect upcoming attacks against built-in web servers have higher
success rate.

This attack was more against a general purpose Linux computer. Let's
take closer look at IoT technology.

What's inside an IoT system?
============================

There is currently no established standards or reference architecture in regards
to IoT. Yet, many implementations are aligned to the following layered design.

At the very bottom of the stack reside actuators (such as motors, valves ...) and
sensors.

In terms of sensor types in the IoT, we can encounter light, sound, temperature,
accelerometers, gas, emission, proximity, moisture, vibration and many other
kinds of sensors.

The sensors are frequently hardwired into the next component of the stack which
is an "embedded system".

Broadly speaking, there is a spectrum of embedded systems. At the higher end
we have a fully fledged computers featuring multi-code CPUs, gigabytes of RAM
and writable flash storage.

At the lower end we would find devices optimized for low power consumption
at the expense of being slower and cheaper. Examples from consumer land
include Arduino, Pinoccio, ESP8266 and others.

Either way, embedded system reads measurements from one or many sensors and/or
powers actuators.

Now, embedded systems, especially MCUs may not be powerful enough to keep/pre-process
moderate amount of data or run full TCP/IP stack to communicate with upper layers.

For the latter reason there exist alternative, simplified wireless network stacks
optimized for low power operations. Frequently, embedded systems are joint into
so-called sensors network and talk to each others.

To cache/aggregate data and adapt WSNs to TCP/IP for further Internet connectivity,
at the third layer of the stack we may encounter so-called IoT gateways.

Finally, either IoT gateways or powerful embedded systems (that can talk to Internet
directly) talk to a server on the Internet, push data and receive commands. Those
servers are collectively called "cloud".

Many cloud computing companies offer specialized IoT solutions geared towards
IoT use cases.

Most importantly, CSPs support the data feed and control protocols that are native
to IoT (CoAP, MQTT, REST API), offer large data storage and purpose-built
analytics engines. They also offer Web-UIs or REST APIs to ease
data consumption.

Armed with a knowledge of a typical IoT architecture, let's look at the other attack...

The story of a plug
===================

Multiple security researchers run into this kind of IoT device. It's essentially
a remotely controlled power outlet. You can turn it on/off from your mobile
phone whilst in the room or anywhere on the Internet. Or may be not just you?

Let's see...

First thing first -- what is on the network? Apparently, when manipulating the plug
at local network, mobile phone sends UDP broadcasts. With blobs resembling
AES encrypted data. No luck here so far.

Let's look at the app. Android apps are easier to decompose and analyze. From
analyzing the app it turns out that phone and plug communicate over a simple text
protocol. But messages are indeed AES encrypted. With a symmetric key.

App is bundled with a Linux shared library. Running `strings` over the library
reveals a few strings that look promising. Let's try them out!

By capturing a packet from mobile phone and trying to AES decipher it with
a candidate key. Once a clear text protocol message shows up -- we get
the key! This key is common for all plugs!

At the protocol level, each plug is addressed my its MAC address and
is password protected.

But how remote control works? Wireshark reveals a persistent TCP connection.
To some server in China.

When turning smart plug through cell Internet, similar AES blobs come over TCP
connection.

Let's search for other plugs in the cloud! For that we need to connect to the cloud
as mobile up does and send protocol messages. But we need two things: plug's MAC and
password. Turns out that MACs are generally adjustent to each other so brute forcing
is easy. Secondly, many users leave default password.

By this point security researcher can manipulate other people's plugs around the
globe. By manipulate I mean not just turning them on and off at random times.
Who knows what can happen to the appliance connected to this plug if it starts
switching many times per second. Could it break down or even catch fire?

Other researchers reported that certain firmware versions has a code injection
vulnerability which lets you embed UNIX shell commands to protocol commands.
By this point you can completely own the plug, run your own apps on it to attack
others on the Internet and locally, send spam.

Here it's again the case of manufacturer's failure to provide reasonable
security. Specifically, not hardcoding key, enforcing password change
and possibly making it harder to identify other plugs on the network.

Default password again! Is not this is a kind of security problem
from the very early Internet?

Let's see who cares for IoT security manufacturing chain...

IoT supply chain
================

First thing to realize is that modern IoT is a pile of complicated
pieces of technology quickly put together by many loosely coordinated
companies. That might be a fertile soil for bugs of all kinds.

Quickly looking at the business taking part in IoT manufacturing,
ODMs is the main source of grief for security researchers.

The weakest link
================

Those guys come up with a gadget idea, then they build the actual product
out of board and the software they add over. The technology they rely
on has become incredibly accessible. Practically a single-person
enterprise can build an IoT device out of, for example, Raspberry Pi.
No wonder that ODMs are really numerous. The majority if ODMs are coming
from China. Some are startups, some are crowdfunded.

Their business model is - the fastest, cheapest and most feature-rich wins.
No wonder that ODMs do not have proper resources and expertise for proper
security.

Technically, the software ODMs produce tops the vulns statistics. Not
only they program the device application, sometimes they also take the
CSP role by hosting their own servers, building their own web and mobile
apps.

So ODMs contribute one or more layers of software.

Who cares about security?
=========================


Factors of insecurity
=====================

Let's see what makes present day's IoT massively insecure.

IoT is hot
----------

IoT is the new hot thing. To stay competitive, businesses have to
get into that bandwagon. And it is not that hard, given the
crucial electronic components are readily available and businesses
are masters of their products.

That extends to traditionally offline businesses. The simplest
thing for them is to just bring their offline product online.

IoT is cool
-----------

People want cool stuff! That creates demand that businesses
naturally want to meet.

IoT is paradoxical
------------------

IoT is easy
-----------

IoT is messy
------------

We have seen how complicated IoT software can get. It is touched
by many teams

IoT is misunderstood
--------------------

IoT is vulnerable
-----------------

The engineers who are used to work with their offline products
may not realize that once they get their product online,
millions of hackers might try getting a profit from its vulns.

Coupled with their inexperience with IT security, that explains
why in IoT we encounter naive, almost forgotten vulnerabilities
like guessable passwords or code injections.

Additionally, devices are easier for attacker to get a hold on
compared to conventional computers locked down in office
buildings.

IoT is powerful
---------------

IoT is hard to mitigate
-----------------------


The story of smart lights
=========================

So far we looked at a relatively simple attacks. Probably because
targets were not sufficiently guarded. Let's look at the high-end
IoT -- Philips Hue smart lights.

These are probably the most popular and quality lighting solutions.
The system lets you turn lights, change luminosity and color. All from
your smartphone or proprietary switches, timers or other home automation
systems like Amazon Echo.

From technical perspective, bulb is built on an Atmel SoC. The SoC
contains an MCU, AES accelerator and a wireless networking module
supporting Zigbee stack.

The bulbs, switches and IoT gateway form a PAN over Zigbee network.
The gateway also participates in Wi-Fi network, supports REST API
(for each bulb) and can also be accessible from the Internet via
a cloud proxy.

The attack
----------

ZigBee is a proprietary network protocol designed for low power, short
range wireless networks. Network traffic is encrypted with a key shared
among all nodes in local network.

When a new node enters network, a neighbour node sends it network key encrypted
with a single, static "master" key. That master key is supposed to be
only available to vendors affiliated with the ZigBee alliance.

Needless to say that master key was leaked in 2015 and is now publicly available.
Hence node joining network leaks network key.

As a way to mitigate that, the ZigBee Light Link protocol adds proximity
check so that network will only give out its shared key to new nodes
emitting weak signal which is an indication of being close.

Despite that measure, researchers were able to find a bug in open source
Atmel's BitCloud library which lets them to reset the bulb to factory default
and trick it to skip the proximity check.

By that point researchers were able to join any ZigBee network
from a distance of hundred meters.

Next goal for researchers was to plant their code into the bulb.
The only way is to reflash the bulb via software update. Trouble is
that firmware images are signed and checked on bulb boot up.

Researchers performed side channel attack on the bootloader which
computes firmware signature with its AES module. Turned out that
making bootloader computing many different (incorrect) signatures
while watching bulb's power consumption patterns reveals the key.

By this point researchers were able to build compromised firmware
and plant it into a single bulb by flying a drone carrying a compromised
bulb near a network of bulbs uploading malicious firmware.

Once a single bulb in a ZigBee network is compromised, work starts
spreading quickly. It's virtually impossible to stop its propagation
for as long as a single infected bulb is running on the network.

This attack could be used to make bulbs misbehaving or brick them.
Also, bulb's on-board radio could be used for jamming other 2.4GHz
radios.

Who cares about security
========================

In their report, security researchers mentioned Philips being extremely
responsive and helpful. They quickly fixed the immediate cause of the vulnerability
which is ability to reset bulb and make it skipping proximity check.

Though the root cause is again hardcoded encryption keys which is a
design flaw of the ZigBee protocol. Security through obscurity never
works!

Major attack vectors
====================




IoT future
==========

Speaking of further IoT development, the major research trend is about making
Things more autonomous and less deterministic. Major ingredients to this are:

* context awareness through more sophisticated sensors
* independent reasoning through massive data processing and analysis
* interoperability for the purpose of auto-organising, ad-hoc systems
