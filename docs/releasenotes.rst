Release Notes
=============

0.3.1
-----

Minor bug-fixes.

Bug fixes:

* `PYD-8 - Cannot generate identicons in JPEG format when using Pillow >= 4.2.0
  <https://projects.majic.rs/pydenticon/issues/PYD-8>`_

0.3
---

Update introducing support for more output formats and ability to use
transparency for PNG identicons.

New features:

* `PYD-6: Add support for having transparent backgrounds in identicons
  <https://projects.majic.rs/pydenticon/issues/PYD-6>`_

  Ability to use alpha-channel specification in PNG identicons to obtain
  complete or partial transparency. Works for both background and foreground
  colour.

* `PYD-7: Ability to specify image format
  <https://projects.majic.rs/pydenticon/issues/PYD-7>`_

  Ability to specify any output format supported by the Pillow library.

0.2
---

A small release that adds support for Python 3 in addition to Python 2.7.

New features:

* `PYD-5: Add support for Python 3.x
  <https://projects.majic.rs/pydenticon/issues/PYD-5>`_

  Support for Python 3.x, in addition to Python 2.7.

0.1.1
-----

This is a very small release feature-wise, with a single bug-fix.

New features:

* `PYD-3: Initial tests <https://projects.majic.rs/pydenticon/issues/PYD-3>`_

  Unit tests covering most of the library functionality.

Bug fixes:

* `PYD-4: Identicon generation using pre-hashed data raises ValueError
  <https://projects.majic.rs/pydenticon/issues/PYD-4>`_

  Fixed some flawed logic which prevented identicons to be generated from
  existing hashes.

0.1
---

Initial release of Pydenticon. Implemented features:

* Supported parameters for identicon generator (shared between multiple
  identicons):
  * Number of blocks in identicon (rows and columns).
  * Digest algorithm.
  * List of foreground colours to choose from.
  * Background colour.
* Supported parameters when generating induvidual identicons:
  * Data that should be used for identicon generation.
  * Width and height of resulting image in pixels.
  * Padding around identicon (top, bottom, left, right).
  * Output format.
  * Inverted identicon (swaps foreground with background).
* Support for PNG and ASCII format of resulting identicons.
* Full documentation covering installation, usage, algorithm, privacy. API
  reference included as well.
