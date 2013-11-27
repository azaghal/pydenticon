About Pydenticon
================

Pydenticon is a small utility library that can be used for deterministically
generating identicons based on the hash of provided data.

The implementation is a port of the Sigil identicon implementation from:

* https://github.com/cupcake/sigil/

Why was this library created?
-----------------------------

A number of web-based applications written in Python have a need for visually
differentiating between users by using avatars for each one of them.

This functionality is particularly popular with comment-posting since it
increases the readability of threads.

The problem is that lots of those applications need to allow anonymous users to
post their comments as well. Since anonymous users cannot set the avatar for
themselves, usually a random avatar is created for them instead.

There is a number of free (as in free beer) services out there that allow web
application developers to create such avatars. Unfortunately, this usually means
that the users visiting websites based on those applications are leaking
information about their browsing habits etc to these third-party providers.

Pydenticon was written in order to resolve such an issue for one of the
application (Django Blog Zinnia, in particular), and to allow the author to set
up his own avatar/identicon service.

Features
--------

Pydenticon has the following features:

* Compatible with Sigil implementation (https://github.com/cupcake/sigil/) if
  set-up with right parameters.
* Creates vertically symmetrical identicons of any rectangular shape and size.
* Uses digests of passed data for generating the identicons.
  * Automatically detects if passed data is hashed already or not.
  * Custom digest implementations can be passed to identicon generator (defaults
  to 'MD5').
* Support for multiple image formats.
  * PNG
  * ASCII
* Foreground colour picked from user-provided list.
* Background colour set by the user.
* Ability to invert foreground and background colour in the generated identicon.
* Customisable padding around generated identicon using the background colour
  (foreground if inverted identicon was requested).

