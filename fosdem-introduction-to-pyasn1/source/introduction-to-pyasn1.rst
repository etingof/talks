
Introduction to pyasn1
======================

Why serialization?
==================

.. figure:: serialization-too-much-data.svg

.. nextslide::

.. figure:: serialization-conversion.svg

Challenge: compact transfer format
==================================

.. figure:: serialization-bandwidth.svg

Challenge: low processing overhead
==================================

.. figure:: serialization-processing.svg

Challenge: constant space
=========================

.. figure:: serialization-storage.svg

Challenge: human readability
============================

.. figure:: serialization-readability.svg

Serialization: the art of compromise
====================================

.. figure:: serialization-compromise.svg

ASN.1 workflow
==============

.. figure:: asn1-workflow.svg

pyasn1 workflow
===============

.. figure:: pyasn1-workflow.svg

Use case: SSH keys
==================

* Grab ASN.1 schema for RSA key, compile it into pyasn1 classes
* Read SSH keys from `~/.ssh/id_rsa`
* Deserialize into Python data structures
* Inspect the contents
* Optionally, modify and store in file

Step 1: grab ASN.1 (from RFC2437)
=================================

.. code-block:: python

    $ cat pkcs-1.asn

    PKCS-1 {iso(1) member(2) us(840) rsadsi(113549) pkcs(1) pkcs-1(1) modules(0) pkcs-1(1)}

    DEFINITIONS EXPLICIT TAGS ::= BEGIN
        RSAPrivateKey ::= SEQUENCE {
             version Version,
             modulus INTEGER,
             publicExponent INTEGER,
             privateExponent INTEGER,
             prime1 INTEGER,
             prime2 INTEGER,
             exponent1 INTEGER,
             exponent2 INTEGER,
             coefficient INTEGER
        }
        Version ::= INTEGER
    END

Step 2: compile ASN.1 into Python
=================================

.. code-block:: bash

    $ pyasn1gen.py pkcs-1.asn > rsakey.py

You can also import a pre-compiled module from *pyasn1-modules*.

.. code-block:: bash

    $ pip install pyasn1-modules

Followed by *from rfc2437 import RSAPrivateKey*

.. nextslide::

Declarative syntax resembling original ASN.1 syntax.

.. code-block:: python

    $ cat rsakey.py
    class Version(Integer):
        pass

    class RSAPrivateKey(Sequence):
        componentType = NamedTypes(
            NamedType('version', Version()),
            NamedType('modulus', Integer()),
            NamedType('publicExponent', Integer()),
            NamedType('privateExponent', Integer()),
            NamedType('prime1', Integer()),
            NamedType('prime2', Integer()),
            NamedType('exponent1', Integer()),
            NamedType('exponent2', Integer()),
            NamedType('coefficient', Integer())
        )

Step 3: read your ~/.ssh/id_rsa
===============================

.. code-block:: python

    from base64 import b64decode
    from pyasn1.codec.der.decoder import decode as der_decoder
    from rsakey import RSAPrivateKey

    # Read SSH key from file (assuming no passphrase)
    with open open('.ssh/id_rsa') as key_file:
        b64_serialization = ''.join(key_file.readlines()[1:-1])

    # Undo BASE64 serialization
    der_serialization = b64decode(b64_serialization)

    # Undo DER serialization, reconstruct SSH key structure
    private_key, rest_of_input = der_decoder(der_serialization, asn1Spec=RSAPrivateKey())

.. nextslide::

    >>> print(private_key.prettyPrint())
    RSAPrivateKey:
     version=0
     modulus=280789907761334970323210643584308373...
     publicExponent=65537
     privateExponent=1704567874679144879123080924...
     prime1=1780178536719561265324798296279384073...
     prime2=1577313184995269616049017780493740138...
     exponent1=1193974819720845247396384239609024...
     exponent2=9240965721817961178848297404494811...
     coefficient=10207364473358910343346707141115...

Play with the keys
==================

.. code-block:: python

    >>> pk = private_key
    >>>
    >>> pk['prime1'] * pk['prime2'] == pk['modulus']
    True
    >>> pk['prime1'] == pk['modulus'] // pk['prime2']
    True
    >>> pk['exponent1'] == pk['privateExponent'] % (pk['prime1'] - 1)
    True
    >>> pk['exponent2'] == pk['privateExponent'] % (pk['prime2'] - 1)
    True

Write it back
=============

* You can serialize modified ASN.1 object

.. code-block:: python

    from pyasn1.codec.der.encoder import encode as der_encoder

    # Serialize SSH key data structure into DER stream
    der_serialization = der_encoder(private_key)

    # Serialize DER stream into BASE64 stream
    b64_serialization = '-----BEGIN RSA PRIVATE KEY-----\n'
    b64_serialization += b64encode(der_serialization)
    b64_serialization += '-----END RSA PRIVATE KEY-----\n'

    with open('.ssh/id_rsa.new', 'w') as key_file:
        key_file.write(b64_serialization)

Alternative: XML
================

* XML schema

.. code-block:: xml

    <xs:element name="beer" type="xs:string" />
    <xs:element name="bitterness" type="xs:int" />

* Serialization: text or binary

  * 49 bytes
  * Optionally typed & named fields

.. code-block:: xml

    <beer>Stone API</beer>
    <bitterness>77</bitterness>

Alternative: [uBJ]SON
=====================

* JSON schema

.. code-block:: python

    { "$schema": "http://json-schema.org/schema#",
      "type": "object",
      "required": ["beer", "bitterness"],
      "properties": {
        "beer": {"type": "string"},
        "bitterness": {"type": "number"}
      }
    }

* Serialization: text or binary

  * 38+ bytes
  * Optionally typed & named fields

.. code-block:: python

    {"beer": "Stone IPA",
     "bitterness": 77}

Alternative: Google ProtoBuffers
================================

* Schema

.. code-block:: python

    // beer.proto
    message BeerData {
      required string name = 1;
      required int32 bitterness = 2;
    }

* Serialization: binary

  * 13 bytes
  * Strongly typed & unnamed fields
  * Compiler to generate stubs

Alternative: Cap'n'Proto
========================

* Schema

.. code-block:: python

    struct BeerData {
      name @0 :Text;
      bitterness @1 :UInt8;
    }

* Serialization: binary

  * Strongly typed & unnamed fields
  * Memory efficient (no copying)
  * Low computation (no parsing)

Alternative: Google FlatBuffers
===============================

* Schema

.. code-block:: python

    struct BeerData {
      name:string;
      bitterness:byte;
    }

* Serialization: binary

  * Strongly typed & unnamed fields
  * Memory efficient (no copying)
  * Low computation (no parsing)

How different is ASN.1
======================

* Schema

.. code-block:: python

    SEQUENCE {
      beer VisibleString (SIZE (3..50)),
      bitterness INTEGER (0..90)
    }

* Serialization: binary or XML

  * 16 bytes (BER), 10 bytes (UPER)
  * Strongly typed & unnamed fields
  * Bandwidth efficient (bit alignment e.g. UPER)
  * Lower computation (octet alignment e.g. OER)
  * Streaming transfer

.. nextslide::

* Supported by virtually any language / protocol analyzer
* Including embedded applications
* Can create SQL DB schema from ASN.1
* Can generate test cases from ASN.1

ASN.1 gotchas
=============

* ASN.1 is over-engineered and complicated
* Lack of high-quality ASN.1 tools in FOSS
* Ad-hoc codecs are numerous, but frequently insecure
* CVE search by ASN.1 gives over thousand of hits

Attacks on serializers
======================

* Memory exhaustion by unbounded data or deep nesting
* Causing loops by cycled references
* Causing data corruption and/or code execution by buffer overflow
* Code execution by injecting malicious commands into serialized data

Is ASN.1 still relevant?
========================

* Heavily used in:

  * Spaceflight, aviation and automotive
  * Industrial robotics and controllers
  * Finance (smart cards, ATM, POS etc)
  * Mobile and fixed telephony
  * Crypto applications and Internet protocols
  * RFID

When I may need ASN.1?
======================

* Interface with existing ASN.1-based systems
* Crypto apps and Internet protocols
* Build protocol to talk to resource-constrained devices

Where ASN.1 came from?
======================

* Remnants of OSI model (part of e-mail suite)
* ASN.1 seems haunted by its OSI past
* OSI lost to Internet in 1990
* Though later protocols struggle with the same problems

Summary
=======

* Do not be scared off by ASN.1
* Reuse existing de/serializers
