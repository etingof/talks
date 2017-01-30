
Hello and welcome!

This talk is going to be all about data serialization! Before I introduce you
to the solutions, let me first explain the problem...

Serialization is a very pervasive process whenever it comes to data
exchange. Unless you are running a stand-alone program that does not
talk to other programs and does not read files, you might soon
fase the need for serialization.

So, imagine we have an object in memory and we want to send it over network
to some program running on some other computer. Easy? Except that given
sufficiently large object, you just can't send it over all at once. The
fundamental problem here is that communication link has a finite bandwidth.
So you got to separate your object onto pieces and send them one by one.

Easy? Except that once the other computer assembles the pieces in their
original order, the object that reveals may mean something completely different.
That's because of the architectural differences between computers (meaning
word size, alignment rules, byte order etc.). Then you realize that either
of you or your remote peer have to adapt serialized data to some common
grounds to make sure its meaning does not change.

There are obviously many ways to divide an object onto pieces (1-st task)
and many possible common data formats (2-nd task).

So, which is better? That depends on your priorities. For example, if
your peer programs communicate over slow, low bandwidth link, then
the size of serialized data plays important role.

If one computer is significantly more performant than the other, you
might want computationally easy transformation between serialized and
in-memory forms.

Another possible consideration would be that one of your computers
is short of memory, so that it can't load the whole message at once.
It can only load a portion of it, process and discard it before loading
the next piece.

Finally, we, programmers, are generally lazy. In the context of
data serialization, we prefer it to be human readable as opposed to
cryptic and therefore requiring some special tool to peek at the
serialized data.

Turns out, that some of these priorities tend to conflict with
others. Consider readability -- for data to be readable to us,
humans, it might have to be represented as English text. But that
immediately grows the data.

Whenever we compress data before pushing it into wire, the
compression process might require CPU cycles. While we are generally
quite relaxed about wasting CPU cycles, thing of low-power or
real-time applications. In these areas compression may not be
a good fit.

ASN.1 is a schema language plus multiple sets of encoding rules, each of
which produces different data formats for a given schema. Why different?
To better match your situation.

Typical workflow for ASN.1 is to take a schema describing data structures
of the application, compile it into language-specific code (or stubs), then
populate the data structures and call encoder to send it over. Or the other
way around -- let decoder populating your data structures from encoded contents.

With pyasn1, I've tried to stick to this basic procedure. There is a third-party
compiler (called asn1ate) that may be able to take ASN.1 schema on input and
produce Python code implementing the data structures that scheme describes.

Let's try it out on something well known -- SSH keys. The game plan is as
follows:

* Grab ASN.1 schema for RSA key (as defined in IETF RFC)
* Compile it into pyasn1 classes
* Read SSH keys from `~/.ssh/id_rsa`
* Deserialize into Python data structures
* Inspect the contents
* Optionally, modify and store in file

But there are many alternatives! I'd like to take a quick peek at
them.

Most known and obvious way to serialize data would be XML. It is human
readable (unless it is not binary XML or it grows too large), and it's in
fact more that just a serialization format -- XML is a powerful and complicated
programming language (XPATH, XSL, namespaces).

Its power sometimes play against it -- it is hard to learn, parsers tend to be slow and
memory hungry. Its complexity make is vulnerable to bugs in parsers (which are numerous
and sometimes devastating).

Now, JSON. The format was more of discovered (by a JS programmer) then designed. It was
not started its life as a standard, rather a grassroots movement. Yes, JSON
has taken over the web world.

It is readable, generally more compact than XML. There are many variation
of JSON that optimize it for different use cases. Processing JSON can take
cycles, also it is not well suitable for data streaming.

Google's Protobuffers are quite close to ASN.1 in many respects. The schema for
describing data, the compiler to turn it into language stubs, the codecs to take
care of serialization.

Though, it lacks universal adoption and has limits on message size. So far
Protobuffers are mostly used inside Google.

Next, two close competitors: Cap'n'Proto and Google FlatBuffers. These
are interesting binary protocols! Besides offering the same services as ProtoBuffers,
these systems optimize for processing time. For that purpose they exchange
messages that are optimized for pointer access. No processing is
required on serialization/deserialization phase, though some transformation
may be invoked lazily.

That property make these systems extremely fast to access and low on
CPU resources. Though, the messages are not compressed and even aligned,
what makes them larger in wire and in memory.

Looking at the internals of these serialization systems have something in common
with file systems.

Considering what ASN.1 has to offer us, it does not look weak. The schema language
is quite functional (though sometimes too complicated, but those parts are
optional). Among the enclosed codecs, some are designed to produce stable
messages (which is important for crypto applications), other produces extremely
condense encoding. Finally, there is a codec in the suite that minimizes processing
time. So you are free to chose or switch the serialization protocol at any moment,
depending on circumstances.

You could compile ASN.1 schema into virtually any language ever existed.
ASN.1 is ubiquous in embedded systems.

Besides language-specific stubs, some ASN.1 compilers could produce SQL schemas
or test cases to run against an application being built.




