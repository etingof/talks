
Python on the bare metal
========================

Agenda
======

This is talk is about running Python on small computer systems.

Specifically, we will check out the MicroPython implementation which is designed
with very modest hardware in mind.

We will look into the popular hardware platforms where we can run Python, their
capabilities, performance and price.

Then we will focus on the Micro Python development work flow and that way move
to the live demo.

Why small computer?
===================

One of the major reasons that drives the manufacturing of these single-board computers
is IoT. The degree of automation and embedding computers into our living environment
is enormous.

From the utility meters, towards smart bulbs, automatic heating and irrigation,
smart toys and price tags. Computers surround us quite uncontrollably.

IoT is dangerous
================

A quick word of caution for people engaging in IoT development.

Along with the comfort and convenience, IoT brings significant security risks
for multiple reasons:

* These small computers are typically equipped with sensors, cameras, servos etc.
  So they can meter and influence the real world.
* The economy of these small computers does not allow for proper security
* They are too numerous to keep an eye on each meaning timely updates
* The users tend to underestimate the risks

But this is what we have. The best we (as programmer) can do is to keep that
in mind and be mindful about the risks.

The microcontrollers
====================

Let's look at a typical microcontroller or MCU. Due to size and cost considerations,
it's usually based on a single chip (SoC) which has all computer components
inside. Sometimes even including Wi-Fi radio and anthena!

Depending on the performance and cost of the board, it can have more or less
RAM and flash. This is important from software point of view as we will see
down the line.

Virtually all boards of that kind have a selection of hardware ports designed
to communicate with sensors, servos and other digital systems.

Some board have Wi-Fi or Bluetooth radios, USB or Ethernet interfaces.

Depending on the performance, the board can be more or less power efficient.

Programming for MCUs
====================

The traditional work flow of software development for an embedded platform
is to code in C or sometimes in C++, then cross-compile your program into
machine code native to your MCU and upload the binary to the board.

While this is a perfectly viable way to deal with MCU, it can be slow. Especially
if you are prototyping and experimenting.

The Micro Python way
====================

The Micro Python approach is to let you code in Python right on the MCU.
You can upload your Python script to the board or code interactively, at
the REPL prompt.

This helps both experienced programmers to speed up the development and
to lowers the entry barrier to the newbies.

What is MicroPython?
====================

Micro Python is a completely new implementation of Python 3.4 heavily optimized
for low memory footprint.

Micro Python can run right on the bare metal hardware as opposed to running
as an application on top of the OS.
