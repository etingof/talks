
Hello and beware! Things are coming and humanity is in danger! I'd like to share
with you the frightening observations of the risks that massive adoption of IoT
devices bring us.

We will look at the technology behind IoT and services it offers
through the eyes of security researcher.

The Things
==========

The term IoT is used to refer to hugely different devices -- from children's
toys to industrial automation. In the context of this talk, we will be mostly
looking at consumer devices which are very common and risky. And are in charge
to use them wisely.

Those things are typically:

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

Home automation is a hot topic for quite some time. We are already beyond the
features that Bradbury was thinking about -- we already have automatic lighting,
heating and irrigation.

Nowdays one can have a personal home assistant that understands human speech. You
can instruct it to dim the lights and control the thermostat, maintain shopping list
and set alarms. You can tell it to tune into specific radio station or play the
music of your choice.

If you are not in mood to talk to your personal assistant, just press an
Amazon Dash Button and get stuff shipped to your doorstep. Possibly by a
delivery drone.

Then there are medical applications. Automatic drug infusion pumps and
pacemakers are already widely used by the patients.

And then the arguably weird stuff - computers are finding their ways into
traditionally low-tech things like this smart brush (which analyses the
health of your hair) or smart mattress (which sends you SMS when something
is hapening on your bad while you are away) or this doggy phone or a
poor man's way of adding Internet connection to an old-style, off-line
things.

Now, things can get creepy. Look at this kiss messenger! The telepresence
technology is frightening and amazing! Security vulnerabilities in that
area might be hilarious and tragic in equal measure.

I won't go any further down this topic. For whoever is interested, I can
refer you to this awesome book.

Things we buy
=============

These gadgets look sleek and appealing indeed. But in reality, the joys comes
together with risks.

Many highly motivated people are working around the clock to
harness the power of billions of Things and leverage it in their interests.

In many cases there is not much you can do about it.

The story of Hajime
===================

You may remember a day in October last year when many high-profile web sites
like Twitter, Amazon, PayPal went down for some time. Apparently, a network
of enslaved and harnessed Things, primarily DVRs and web cameras, stood behind
that attack.

The attacking software is dubbed Mirai, its code was open sourced and is
available at Github. This story is about a slightly improved version of
Mirai caught in the wild by security researchers and called Hajime.

Here is how it works.

The ultimate goal of a botnet breeder is to implant their software into as
many computers as possible and then instruct them to carry out certain
operations like DDoS attacks or spam.

The infection process starts from a single attacking node scanning the Internet
in search for an open telnet port. Once it hits one, the attacker tries to
brute-force the login credentials using dozens of factory-default passwords.

If login succeeded and attacking node drops into shell, it searches for
a writable filesystem (like /var) and echos hex-escaped machine codes
into a local file. That gives attacker a small executable which, once run,
opens up a tcp connection back to the attacking node and downloads a large
binary. That binary is an actual malware which does two things: first
it starts its own propagation process (as just described) and secondly
it joins a BitTorrent network and starts listening for further
instructions.

Over time the infection process makes up a huge, self-propagating and
remotely controlled network of bots. Security researchers reported,
that at the peak of the Mirai epidemy, mean time to compromise of a
vulnerable IoT device is 10 minutes or less. That explains why
rebooting infected device does not really help.

Once its master decided to mount an attack of specific kind, they
send a "plugin" module along with a configuration into the P2P
network. The bots pick that up from P2P and run whatever code
their master wants them to.

The attacks that Mirai was capable to carry out includes HTTP, TCP, UDP and
DNS floods. Considering hundreds of thousands of nodes flooding a single
target simultaneously, it is no wonder that consequences were devastating.

Mirai attack is thought to be the largest in history - at various
points of the Internet, network engineers observed hundreds thousands
of individual IPs and traffic rate spikes to terabits per second.

Attack post-mortem
==================

Clearly, Mirai attack wouldn't be successful if telnet service would not
be running or credentials would not be that easy to brute force.

Fun facts
=========

Interestingly, researchers have observed many implementations of Linux
worms like Hajime in the wild. The worms naturally compete for hosts,
sometimes they become hostile to each other and try to kill or enslave
the competing worms.

Among those worms, the one that stands out is `Linux.Wifatch`. Its is
relatively harmless to its hosts, the only thing it does is that it
changes default root password and shuts down telnet daemon to prevent
infection.

The Mirai attack was more against a general purpose Linux computer. Before
we analyze a more IoT specific attack, let's take a closer look what's
inside an IoT system.

What's inside an IoT system?
============================

There is currently no established standards or architecture in regards
to IoT. Yet, many implementations are aligned to the following layered
design.

At the very bottom of the stack reside sensors and actuators. The sensors
are typically hardwired into the next component of the stack which is an
"embedded system".

The embedded system could be more or less powerful (like RAspberry Pi or
Arduino). They are joint into a network along with the next component
which is a gateway.

IoT gateway, if present, provides data storage and Internet connectivity for
the rest of the IoT network.

Finally, the gateways maintain a connection with servers on the Internet
which are collectively called "cloud". The cloud accumulates and processes
the data coming from IoT and sends out commands.

Armed with a knowledge of a typical IoT architecture, we are approaching
the next attack story...

The story of a plug
===================

Multiple security researchers run into this kind of IoT device. It's
essentially a remotely controlled power outlet. You can turn it on/off
from your mobile phone whilst in the room or anywhere on the Internet.

The researchers started their analysis from looking at the mobile
application for Android. They decompiled it and studied the code. They
figured that smartphone and plug communicate over a simple text
protocol. Each message contains plug's MAC address and an optional
password that owner may set (or leave it empty).

Protocol messages are AES encrypted. So the researched looked into
the encryption subsystem. Turns out that the app is bundled with a
Linux shared library. Running `strings` over the library reveals a few
strings that look promising.

Then researchers tried candidate keys by capturing a packet produced
by mobile phone and trying to AES decipher it with a key. Ultimately,
they found the right one which is common for all plugs!

Now, the plug in advertised as remotely controlled. Researchers looked
what's on the network and found that plug maintains a persistent TCP
connection with a server in China. Wireshark reveals that plug uses the
same protocol for server communication. So they connected to server
and found many plugs connected to that server by trying adjacent
MAC addresses.

By this point security researcher can manipulate other people's plugs around the
globe. By manipulate I mean not just turning them on and off at random times.
Who knows what can happen to the appliance connected to this plug if it starts
switching many times per second. Could it break down an appliance or even
catch fire?

Other researchers reported that certain firmware versions has a code injection
vulnerability which lets you embed UNIX shell commands to protocol commands.
By this point they could can completely own the plug my running their code
on them. That would let them attack hosts on plug's network, attack others
on the Internet, send spam.

Attack post-mortem
==================

Here it's again the case of manufacturer's failure to provide reasonable
security. Specifically,  hardcoding key, not enforcing password change
and making it easy to identify other plugs on the network.

Apparently, that is a very common vulnerability with today's devices.
Now, I'm offering you a quick look on IoT supply chain to understand the
reason why.

IoT supply chain
================

First thing to realize is that modern IoT is a pile of complicated
pieces of technology duct-typed together by many loosely coordinated
companies.

Here's a stack of businesses taking part in building a single IoT
product.

Who builds Things
=================

Among them, the ones that actually create the device (AKA Original
Design Manufacturers) frequently cause grief to security people.

Those guys come up with a gadget idea, then they build the actual product
out of board and the software they add over. The technology they rely
on has become incredibly accessible. Practically a single-person
enterprise can build an IoT device out of, for example, Raspberry Pi.
No wonder that ODMs are really numerous. The majority if ODMs are coming
from China. Some are startups, some are crowd funded.

Their business model is - the fastest, cheapest and most feature-rich wins.
No wonder that ODMs do not have proper resources and expertise for proper
security.

Who sells Things
================

We, consumers, only deal with the companies at the very top layer. Those
guys market the product, maintain a brand, offer warranty and customer
support, handle legal affairs.

They are also a point of contact for security researchers reporting
discovered vulnerabilities. Trouble is that, oftentimes, they can't
do much about security. They may not have the code to tackle or
expertise to understand the problem at the very technical level.

Sometimes, instead of fixing the vulnerablity, they use their PR powers
to downplay the severity of a flaw. Sometimes they even turn hostile to
security researchers threatening to sue them.

Things are...
=============

IoT is huge! Many actors are interplaying there pursuing their interests
and goals.

IoT is hot
----------

From business perspective, IoT is a hot thing. To stay competitive, businesses
are being pressed to make their originally offline products "connected".

IoT is cool
-----------

We love gadgets! They are designed to be desirable.

We poke fun at smart devices...yet, happily buy them.

IoT is easy
-----------

For vendors, adding a $5 computer to their existing product is seemingly
very doable, though the consequences of a security breach is not apparent.

The engineers who are used to work with their offline products
may not realize that once they get their product online,
millions of hackers suddenly get interested in its weaknesses.

Coupled with their inexperience with IT security, that explains
why in IoT we encounter naive, almost forgotten vulnerabilities
like guessable passwords or code injections.

IoT is hard
-----------

Things are generally harder to engineer properly.

They are harder to patch: owners may not know
and/or care, updates for embedded platform often requires
full reflashing which is risky.

IoT is weak
-----------

Embedded computers might not have sufficient power to
run a strong crypto. It takes extra efforts for system
designers to provide a high-entropy source on the embeddedd
platform.

Additionally, devices are easier for attacker to get a hold on
compared to conventional computers locked down in office
buildings.

IoT is powerful
---------------

Yet, combining billions of weak computers sums up to teraflops
of computing power and terabits of network bandwidth.

IoT is messy
------------

A deep stack of interplaying software layers make up an IoT device.
That software goes through a long supply chain being touched by
many uncoordinated teams.

IoT is misunderstood
--------------------

It might not occur to you that you need to apply software
update to this smart pillow. It's a pillow, right?

Yet, it is a general purpose computer disguised as a pillow.
That fools consumers and, surprisingly, manufacturers.

What can possibly go wrong with a pillow? Yet, the risks are
not that it miscalculate your sleep patterns, but that it may,
for example, tell a burglar that you are not at home.

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
supporting ZigBee stack.

The bulbs, switches and IoT gateway form a ZigBee mesh network.
The gateway also participates in Wi-Fi network, supports REST API
(for each bulb) and can also be accessible from the Internet via
a cloud proxy.

ZigBee vulnerability
====================

ZigBee is a proprietary network stack designed for low power, short
range wireless networks. Network traffic is encrypted with a key shared
among all nodes in local network.

When a new node joins network, a neighbour node sends it network key encrypted
with a single, static "master" key. That master key is supposed to be
only available to vendors affiliated with the ZigBee alliance.

Needless to say that master key was leaked in 2015 and is now publicly available.
Hence every time a node joins network, it leaks the network key.

As a way to mitigate that, the ZigBee Light Link protocol has a proximity
check so that network will only give out its shared key to new nodes
emitting weak signal which is an indication of being in close proximity.

Defeating proximity check
=========================

Despite that measure, researchers were able to find a bug in open source
Atmel's BitCloud library which lets them to reset the bulb to factory default
tricking it to try different key exchange protocol skipping the proximity check.

By that point researchers were able to join any ZigBee network
from a distance of hundred meters.

Firmware compromise
===================

Next goal for researchers was to plant their code into the bulb.
The only way is to reflash the bulb via software update. Trouble is
that firmware images are signed and checked on bulb boot up.

Researchers performed side channel attack on the bootloader which
computes firmware signature with its AES module. They did that my
running a analysis technique known as differential or correlation
power analysis.

Turned out that making bootloader computing many different
(incorrect) signatures while watching bulb's power consumption patterns
reveals the key.

By this point researchers were able to build compromised firmware
and plant it into their bulb.

Unleashing worm
===============

Then they mounted their infected bulb on a drone and flew by
a ZigBee network of bulbs uploading malicious firmware into them.

Once a single bulb in a ZigBee network is compromised, work starts
spreading quickly. It's virtually impossible to stop its propagation
for as long as a single infected bulb is running on the network.

Exploit potential
=================

This attack could be used to make bulbs misbehaving or brick them.
Also, bulb's on-board radio could be used for jamming other 2.4GHz
radios.

Attack post-mortem
==================

Though the root cause is again hardcoded encryption keys which is a
design flaw of the ZigBee protocol. Security through obscurity never
works!

This attack also demonstrates how hard it is to design and produce
a secure system even if it is major product of a large, established
company.

Major attack vectors
====================

Looking at the hacks discovered in a couple of past years, the major
cause seems to be attributed to leaked passwords, encryption and API keys.

When vendors take a stock Linux distribution and use it unmodified
in their products, that inevitable results in unnecessary services
kept running and ultimately exploited.

When remote attack is not feasible, attackers may approach the
system through an unsecured hardware interface. Most commonly
serial console and JTAG.

Then all sorts of code injection vulnerabilities ranging from UNIX
shell injections up to good-old XSS.

IoT future
==========

Speaking of further IoT development, the major research trend is about making
Things more autonomous and less deterministic. Major ingredients to this are:

* context awareness through more sophisticated sensors
* independent reasoning through massive data processing and analysis
* interoperability for the purpose of auto-organising, ad-hoc systems

Advice for developers
=====================

If you are getting involved in coding for an IoT project, realize that
once your software or product is out, it will be looked at thoroughly
without you knowing.

There are black markets for personal data, so if your system keep anything
of that kind, it will be probed sooner or later. Thus, it's better not
to take and store personal data.

If you have to, encrypt data in motion and at rest aggressively and in a way
that can be reversed easily.

In the nutshell, there is a great web-site maintained by field experts
where they have a checklist to follow when it comes to building IoT
devices and software.

Finally, you could pentest your code by employing hackers.

Advice for users
================

I know that it is easier to tell then do, yet, restrain from owning
consumer IoT devices. The security situation might improve over time,
but as we have them now, they are scary.

If you can't resist the desire to have a Thing, research the vendor to
see what's their track record -- did they have security problems in the past,
how they reacted, do they ship the updates, for how long.

Once you are a happy owner of an IoT gadget, put it (along with other Things)
on a dedicated Wi-Fi network, firewall and disable uPnP.

If you realised that was a wrong decision and decided to sell it, be aware
that the Thing still may hold you personal secrets. Resetting it may not help!

Similar concern applies to second-hand gadgets -- they may be sold infected
so they may do not quite the things you expect them to.

Summary
=======

The technology is blooming fueling our amazement and tricking
us into buying Things. My hope is that this talk makes you cautious and
better prepared for the Things invasion.

To summarize:

* Be conscious that Things nearby may be watching you.
* Keep your expectations low when it comes to Things
  security.
* Be reluctant giving out any data, even if it does not look valuable at the moment.
* Struggle not to let Things into your home!

Be suspicious and keep safe!
