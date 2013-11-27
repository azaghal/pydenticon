Installation
============

Pydenticon can be installed through one of the following methods:

* Using *pip*, which is the easiest and recommended way for production websites.
* Manually, by copying the necessary files and installing the dependencies.

Requirements
------------

The main external requirement for Pydenticon is `Pillow
<http://python-imaging.github.io/>`_, which is used for generating the images.

Using pip
---------

In order to install latest stable release of Pydenticon using *pip*, run the
following command::

  pip install pydenticon

In order to install the latest development version of Pydenticon from Github,
use the following command::

  pip install -e git+https://github.com/azaghal/pydenticon#egg=pydenticon

Manual installation
-------------------

If you wish to install Pydenticon manually, make sure that its dependencies have
been met first, and then simply copy the ``pydenticon`` directory (that contains
the ``__init__.py`` file) somewhere on the Python path.

