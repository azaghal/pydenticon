Usage
=====

Pydenticon provides simple and straightforward interface for setting-up the
identicon generator, and for generating the identicons.

Instantiating a generator
-------------------------

The starting point is to create a generator instance. Generator implements
interface that can be used for generating the identicons.

In its simplest form, the generator instances needs to be passed only the size
of identicon in blocks (first parameter is width, second is height)::

  # Import the library.
  import pydenticon

  # Instantiate a generator that will create 5x5 block identicons.
  generator = pydenticon.Generator(5, 5)

The above example will instantiate a generator that can be used for producing
identicons which are 5x5 blocks in size, using the default values for digest
(*MD5*), foreground colour (*black*), and background colour (*white*).

Alternatively, you may choose to pass in a different digest algorithm, and
foreground and background colours::

  # Import the libraries.
  import pydenticon
  import hashlib

  # Set-up a list of foreground colours (taken from Sigil).
  foreground = [ "rgb(45,79,255)",
                 "rgb(254,180,44)",
                 "rgb(226,121,234)",
                 "rgb(30,179,253)",
                 "rgb(232,77,65)",
                 "rgb(49,203,115)",
                 "rgb(141,69,170)" ] 

  # Set-up a background colour (taken from Sigil).
  background = "rgb(224,224,224)"

  # Instantiate a generator that will create 5x5 block identicons using SHA1
  # digest.
  generator = pydenticon.Generator(5, 5, digest=hashlib.sha1,
                                   foreground=foreground, background=background)

Generating identicons
---------------------

With generator initialised, it's now possible to use it to create the
identicons.

The most basic example would be creating an identicon using default padding (no
padding) and output format ("png"), without inverting the colours (which is also
the default)::

  # Generate a 240x240 PNG identicon.
  identicon = generator.generate("john.doe@example.com", 240, 240)

The result of the ``generate()`` method will be a raw representation of an
identicon image in requested format that can be written-out to file, sent back
as an HTTP response etc.

Usually it can be nice to have some padding around the generated identicon in
order to make it stand-out better, or maybe to invert the colours. This can be
done with::

  # Set-up the padding (top, bottom, left, right) in pixels.
  padding = (20, 20, 20, 20)

  # Generate a 200x200 identicon with padding around it, and invert the
  # background/foreground colours.
  identicon = generator.generate("john.doe@example.com", 200, 200,
                                 padding=padding, inverted=True)

Finally, the resulting identicons can be in different formats::

  # Create identicon in PNG format.
  identicon_png = generator.generate("john.doe@example.com", 200, 200,
                                     output_format="png")
  # Create identicon in ASCII format.
  identicon_ascii = generator.generate("john.doe@example.com", 200, 200,
                                       output_format="ascii")

Supported output formats are dependant on the local Pillow installation. For
exact list of available formats, have a look at `Pillow documentation
<https://pillow.readthedocs.io/>`_. The ``ascii`` format is the only format
explicitly handled by the *Pydenticon* library itself (mainly useful for
debugging purposes).

Using the generated identicons
------------------------------

Of course, just generating the identicons is not that fun. They usually need
either to be stored somewhere on disk, or maybe streamed back to the user via
HTTP response. Since the generate function returns raw data, this is quite easy
to achieve::

  # Generate same identicon in three different formats.
  identicon_png = generator.generate("john.doe@example.com", 200, 200,
                                     output_format="png")
  identicon_gif = generator.generate("john.doe@example.com", 200, 200,
                                     output_format="gif")
  identicon_ascii = generator.generate("john.doe@example.com", 200, 200,
                                       output_format="ascii")

  # Identicon can be easily saved to a file.
  f = open("sample.png", "wb")
  f.write(identicon_png)
  f.close()

  f = open("sample.gif", "wb")
  f.write(identicon_gif)
  f.close()

  # ASCII identicon can be printed-out to console directly.
  print identicon_ascii


Working with transparency
-------------------------

.. note::
   New in version ``0.3``.

.. warning::
   The only output format that properly supports transparency at the moment is
   ``PNG``. If you are using anything else, transparency will not work.

If you ever find yourself in need of having a transparent background or
foreground, you can easily do this using the syntax
``rgba(224,224,224,0)``. All this does is effectively adding alpha channel to
selected colour.

The alpha channel value ranges from ``0`` to ``255``, letting you specify how
much transparency/opaqueness you want. For example, to have it at roughly 50%
(more like at ``50.2%`` since you can't use fractions), you would simply specify
value as ``rgba(224,224,224,128)``.


Full example
------------

Finally, here is a full example that will create a number of identicons and
output them in PNG format to local directory::

  #!/usr/bin/env python

  # Import the libraries.
  import pydenticon
  import hashlib

  # Set-up some test data.
  users = ["alice", "bob", "eve", "dave"]

  # Set-up a list of foreground colours (taken from Sigil).
  foreground = [ "rgb(45,79,255)",
                 "rgb(254,180,44)",
                 "rgb(226,121,234)",
                 "rgb(30,179,253)",
                 "rgb(232,77,65)",
                 "rgb(49,203,115)",
                 "rgb(141,69,170)" ] 

  # Set-up a background colour (taken from Sigil).
  background = "rgb(224,224,224)"

  # Set-up the padding (top, bottom, left, right) in pixels.
  padding = (20, 20, 20, 20)

  # Instantiate a generator that will create 5x5 block identicons using SHA1
  # digest.
  generator = pydenticon.Generator(5, 5, foreground=foreground,
                                   background=background)

  for user in users:
    identicon = generator.generate(user, 200, 200, padding=padding,
                                   output_format="png")

    filename = user + ".png"
    with open(filename, "wb") as f:
        f.write(identicon)

