Release Notes
=============

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
