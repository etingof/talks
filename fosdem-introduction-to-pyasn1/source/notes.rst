
ASN.1 and JSON aren't strictly comparable. JSON is a data format.
ASN.1 is a schema language plus multiple sets of encoding rules, each of
which produces different data formats for a given schema.
So, the original question somewhat parallels the question "XML Schema vs. XML:
when is it appropriate to use them?" A fairer comparison would be between ASN.1
 and JSON Schema.

That said, a few points to consider:

ASN.1 has binary encoding rules. Consider whether binary or text encoding is
preferable for your application. ASN.1 also has XML encoding rules. You can
opt to go with a text-based encoding using ASN.1, if you like.
ASN.1 allows other encoding rules to be developed.
As with XML Schema, tools exist for compiling ASN.1. These are commonly referred
to as data binding tools. The compiler output consists of data structures to
hold your data, and code for encoding/decoding to/from the various encodings
(binary, XML, or, if using our tool, JSON).
I am not sure what, if any, data binding tools exist for JSON Schema. I am also
not sure how mature/stable JSON Schema is, whereas ASN.1 is quite mature and stable.
Choosing between JSON Schema and ASN.1, note that JSON Schema is bound to JSON,
whereas ASN.1 is not bound to any particular representation.

You can use ASN.1 regardless of whether you need to serialize messages that might go
to a recipient using C, C++, C#, Java, or any other programming language with ASN.1
encoder/decoder engine. ASN.1 also provides multiple encoding rules which have benefits
under different circumstances. For example, DER is used when a canonical encoding is
crucial, such as in digital certificates, while PER is used when bandwidth is critical
such as in cellular protocols, and E-XER is used when you don't care about bandwidth
and would like to display an encoding in XML for maniplulation in a browser or exchange
messages with an XML Schema engine.

Note that with a good ASN.1 tool, you don't have to change you application code to
switch between these ASN.1 encoding rules. A simple function call can select the
encoding rules you would like to use.

http://ttsiodras.github.io/asn1.html
https://news.ycombinator.com/item?id=8871453

ASN.1 usage

Air-ground and ground-ground protocols employed by the Federal Aviation Administration and International Civil Aviation Organization are described in ASN.1 and are encoded in PER. The Aeronautical Telecommunication Network (ATN), which has been operational in Europe since 2007, is specified with ASN.1 and uses the compact PER encoding. ASN.1 encoders/decoders are now installed on American Airlines B767 aircraft in the certified ATN compliant avionics from Rockwell Collins

Radio-Frequency Identification (or RFID) is implemented in numerous industrial sectors (person or vehicle identification, stock management, etc.). The electronic tags are actually miniaturized radio emitters that can be read from a few centimeters to several meters off, even through obstacles that would prevent the use of barcodes, for instance.

Spaceflight: The Consultative Committee for Space Data Systems (CCSDS) is a multinational forum for the development of communications and data systems standards for spaceflight. The Space Link Extension Services (SLE) are a set of communication services developed by CCSDS. SLE services are used between the tracking stations or ground data handling systems of various organizations and the mission-specific components of a mission ground system. SLE services are applicable to routine, contingency and emergency operations, and their messages are specified in ASN.1.

Manufacturing: Manufacturing Message Specification (MMS) is an international standard (ISO 9506) dealing with messaging system for transferring real time process data and supervisory control information between networked devices and/or computer applications. MMS supports the remote control and monitoring of industrial devices such as programmable logic controllers and robots, and has been used in many different applications such as material handling, energy management, electrical power distribution control, and inventory control. MMS messages are specified in ASN.1. MMS is poised to play a significant role in the context of the Smart Grid. IEC 61850, a widely used standard for electricity generation automation that is among the foundational standards selected by the Smart Grid Interoperability Panel, specifies abstract data models while relying on concrete protocols such as MMS for the exchange of information across the communication network.

Telecom: cell, voip
