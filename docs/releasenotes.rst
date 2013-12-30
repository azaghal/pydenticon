Release Notes
=============

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
