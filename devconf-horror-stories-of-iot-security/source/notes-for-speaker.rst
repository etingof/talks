
Things are coming and humanity is in danger! In this talk I will
share the frightening vision of what awaits us in the coming years.

The structure of this talk is as follows.

The Things
==========

When we talk of IoT we typically refer to:

* small, inexpensive, low-power computers
* equipped with sensors and/or actuators
* being able to communicate with each other and with the Internet

The dangers
===========

We are already highly dependent on the computers, but IoT brings
this dependency to a new level. If we look at the history of computing
we will notice that we:

* more and more of critical infrastructure is handled by computers
* computers becomes smaller
* greater in numbers
* closer to the humans

We are literally getting surrounded by the computers! Being dependent
is always risky.

Before the IoT era, computer glitches and cyber crime tended
to revolve around data - loss or leaks or modification. With the IoT
emerging, we are getting exposed to fundamentally new risks:

* Things have direct contact with and impact to the physical world, including humans
* We may not notice them, however they are numerous
* The Things are designed to help us what also means they have to watch us (by collecting
  huge amount of data)
* Things, as they stand now, are massively insecure

By way of this talk we will examine how Things work and how we learnt of some of them
being compromised.

Dreams come true
================

The idea behind IoT is not new. Smart homes, for example, was envisioned by sci-fi many
years ago.

For example, in "There Will Come Soft Rains" story written by Ray Bradbury in 1950,
the reader is introduced to a computer-controlled house that cooks, cleans, and takes
care of virtually every need that a well-to-do US family could possibly have. The story
unfolds in 2026, that is in nine years from now.

Interestingly, Bradbury's smart home was quite reliable as it withstood a nuclear strike
and kept running its duties while standing in the midst of a ruined and lifeless town.

Today's Things
==============

The technology, especially electronics, has developed sufficiently well to make
scaled down and cheap computers possible.

RFID is frequently considered as the first mass-production IoT device. Initially,
it was the only IoT technology implemented. But as radio networks and electronics
progress, more sophisticated sensors shaded RFIDs.

Today we widely use RFID tags for identification purposes -- goods in shops and stocks
(which supersedes bar codes), domestic animals, authenticating humans at door locks...

In just a few years, the technology of wearable computers advanced to the point
where one could have a computer built into their running shoes that won't require any
maintenance (including charge) for one year!

Home automation is a hot topic for a long time. We are already beyond the features that
Bradbury was thinking about -- automatic lighting, heating, irrigation and monitoring is
here. But human imagination and (desire for comfort) proves to have no limits!

Nowdays one can have a personal home assistant that understands human speech. You
can instruct it to dim the lights and control the thermostat, maintain shopping list
and set alarms. You can tell it to tune into specific radio station or play the
music of your choice.

If you are not in mood to talk to your personal assistant, just press an Amazon Dash Button
and get stuff shipped to your home. Possibly by an Amazon PrimeAir delivery drone.

The drone technology is hitting new heights. Modern consumer drones have on-board
GPS navigation so you can plan dron's mission on a map, then it will follow a
pre-programmed flight plan.

To avoid obstacles and crashing, modern drones start carrying sonars and cameras
along with a high-performance on-board computer running image recognition and AI
programs.

Some can maintain an Internet connection with their pilot's console streaming
video and telemetry information there and receive flight orders.

A research is ongoing to introduce automated and centralized air-traffic control
for drones. Drone owners will file their flight plans to the system which will
do the computation in real time, peer with each drone in flight and guide them
all simultaneously to share the airspace efficiently and safe.

Then there are medical applications. Automatic insulin pumps and pacemakers are
already widely used.

And the personal stuff - computers are finding their ways into traditionally
low-tech things like hygiene items and sleeping gear.

It is no secret that relationships and sex are among the big technology drivers.
Of course IoT businesses address that demand. Look at this remote kissing gadget!
The telepresence technology is frightening and amazing! And it opens up Pandora's
box of ethical questions.

In this talk I won't go any further down this topic. If you are interested, I
can refer you to this book and same-named international conference held in UK.

IoT future
==========

Speaking of further IoT development, the major research trend is about making
Things more autonomous and less deterministic. Major ingredients to this are:

* context awareness through more sophisticated sensors
* independent reasoning through massive data processing and analysis
* interoperability for the purpose of auto-organising, ad-hoc systems

IoT components
==============

There is currently no established standards or reference architecture in regards
to IoT. Yet, many implementations are aligned to the following layered design.

At the very bottom of the stack reside actuators (such as motors, valves ...) and
sensors.

In terms of sensor types in the IoT, we can encounter temperature sensors,
accelerometers, gas, emission, proximity, moisture, vibration and many other
kinds of sensors.

The sensors are frequently hardwired into the next component of the stack which
is a "control unit".

Broadly speaking, there is a spectrum of control units. At the lower end
we would find devices optimized for low power consumption at the expense
of being slower and cheaper. These are known as. Examples from consumer land
include Arduino, Pinoccio, ESP8266 and others.

At the other end we have a fully fledged computers featuring multi-code CPUs,
gigabytes of RAM and writable flash storage.

Either way, control unit reads measurements from one or many sensors and/or
powers actuators.

Now, control units, especially MCUs may not be powerful enough to keep/pre-process
moderate amount of data or run full TCP/IP stack to communicate with upper layers.

For the latter reason there exist alternative, simplified wireless network stacks
optimized for low power operations. Frequently, control units are joint into
so-called sensors network and talk to each others.

To cache/aggregate data and adapt WSNs to TCP/IP for further Internet connectivity,
at the third layer of the stack we may encounter so-called IoT gateways.

Finally, either IoT gateways or powerful control units (that can talk to Internet
directly) talk to a server on the Internet, push data and receive commands. Those
servers are collectively called "cloud".

Many cloud computing companies offer specialized IoT solutions geared towards
IoT use cases.

Most importantly, CSPs support the data feed and control protocols that are native
to IoT (CoAP, MQTT, REST API) and also offer large data storage and analytics engines.
Some offer Web-UIs or REST APIs to ease data consumption.

IoT supply chain
================


