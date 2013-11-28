Algorithm
=========

A generated identicon can be described as one big rectangle divided into ``rows
x columns`` rectangle blocks of equal size, where each block can be filled with
the foreground colour or the background colour. Additionally, the whole
identicon is symmetrical to the central vertical axis, making it much more
aesthetically pleasing.

The algorithm used for generating the identicon is fairly simple. The input
arguments that determine what the identicon will look like are:

* Size of identicon in blocks (``rows x columns``).
* Algorithm used to create digests out of user-provided data.
* List of colours used for foreground fill (foreground colours). This list will
  be referred to as ``foreground_list``.
* Single colour used for background fill (background colour). This colour wil be
  referred to as ``background``.
* Whether the foreground and background colours should be inverted (swapped) or
  not.
* Data passed to be used for digest.

The first step is to generate a *digest* out of the passed data using the
selected digest algorithm. This digest is then split into two parts:

* The first byte of digest (``f``, for foreground) is used for determining the
  foreground colour.
* The remaining portion of digest (``l``, for layout) is used for determining
  which blocks of identicon will be filled using foreground and background
  colours.

In order to select a ``foreground`` colour, the algorithm will try to determine
the index of the colour in the ``foreground_list`` by doing modulo division of
the first byte's integer value with number of colours in
``foreground_list``::

  foreground = foreground_list[int(f) % len(foreground_list)]

The layout of blocks (which block gets filled with foreground colour, and which
block gets filled with background colour) is determined by the bit values of
remaining portion of digest (``l``). This remaining portion of digest can also
be seen as a list of bits. The bit positions would range from ``0`` to ``b``
(where the size of ``b`` would depend on the digest algoirthm that was picked).

Since the identicon needs to be symmetrical, the number of blocks for which the
fill colour needs to be calculated is equal to ``rows * (columns / 2 + columns %
2)``. I.e. the block matrix is split in half vertically (if number of columns is
odd, the middle column is included as well).

Those blocks can then be marked with whole numbers from ``0`` to ``c`` (where
``c`` would be equal to the above formula - ``rows * (columns / 2 + columns %
2)``). Number ``0`` would correspond to first block of the first half-row, ``1``
to the first block of the second row, ``2`` to the first block of the third row,
and so on to the first block of the last half-row. Then the blocks in the next
column would be indexed with numbers in a similar (incremental) way.

With these two numbering methods in place (for digest bits and blocks of
half-matrix), every block is assigned a bit that has the same position number.

If no inversion of foreground and background colours was requested, bit value of
``1`` for a cell would mean the block should be filled with foreground colour,
while value of ``0`` would mean the block should be filled with background
colour.

If an inverted identicon was requested, then ``1`` would correspond to
background colour fill, and ``0`` would correspond to foreground colour fill.

Examples
--------

An identicon should be created with the following parameters:

* Size of identicon in blocks is ``5 x 5`` (a square).
* Digest algorithm is *MD5*.
* Five colours are used for identicon foreground (``0`` through ``4``).
* Some background colour is selected (marked as ``b``).
* Foreground and background colours are not to be inverted (swapped).
* Data used for digest is ``branko``.

MD5 digest for data (``branko``) would be (reperesented as hex value) equal to
``d41c0e80c44173dcf7575745bdddb704``.

In other words, 16 bytes would be present with the following hex values::

  d4 1c 0e 80 c4 41 73 dc f7 57 57 45 bd dd b7 04

Following the algorithm, the first byte (``d4``) is used to determine which
foreground colour to use. ``d4`` is equal to ``212`` in decimal format. Divided
by modulo ``5`` (number of foreground colours), the resulting index of
foreground colour is ``2`` (third colour in the foreground list).

The remaining 15 bytes will be used for figuring out the layout. The
representation of those bytes in binary format would look like this (5 bytes per
row)::

  00011100 00001110 10000000 11000100 01000001
  01110011 11011100 11110111 01010111 01010111
  01000101 10111101 11011101 10110111 00000100

Since identicon consits out of 5 columns and 5 rows, the number of bits that's
needed from ``l`` for the layout would be ``5 * (5 / 2 + 5 % 2) == 15``. This
means that the following bits will determine the layout of identicon (whole
first byte, and 7 bits of the second byte)::

  00011100 0000111

The half-matrix would therefore end-up looking like this (5 bits per column for
5 blocks per column)::

  010
  000
  001
  101
  101

The requested identicon is supposed to have 5 block columns, so a reflection
will be applied to the first and second column, with third column as center of
the symmetry. This would result in the following ideticon matrix::

  01010
  00000
  00100
  10101
  10101

Since no inversion was requested, ``1`` would correspond to calculated
foreground colour, while ``0`` would correspond to provided background colour.

To spicen the example up a bit, here is what the above identicon would look like
in regular and inverted variant (with some sample foreground colours and a bit
of padding):

.. image:: images/branko.png
.. image:: images/branko_inverted.png

Limitations
-----------

There's some practical limitations to the algorithm described above.

The first limitation is the maximum number of different foreground colours that
can be used for identicon generation. Since a single byte (which is used to
determining the colour) can represent 256 values (between 0 and 255), there can
be no more than 256 colours passed to be used for foreground of the
identicon. Any extra colours passed above that count would simply be ignored.

The second limitation is that the maximum dimensions (in blocks) of a generated
identicon depend on digest algorithm used. In order for a digest algorithm to be
able to satisfy requirements of producing an identcion with ``rows`` number of
rows, and ``columns`` number of columns (in blocks), it must be able to produce at
least the following number of bits (i.e. the number of bits equal to the number
of blocks in the half-matrix)::

  rows * (columns / 2 + columns % 2) + 8

The expression is the result of vertical symmetry of identicon.  Only the
columns up to, and including, the middle one middle one (``(columns / 2 + colums
% 2)``) need to be processed, with every one of those columns having ``row``
rows (``rows *``). Finally, an extra 8 bits (1 byte) are necessary for
determining the foreground colour.

