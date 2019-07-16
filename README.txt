Introduction
============

.. image:: https://readthedocs.org/projects/sparkfun-circuitpython-qwiicrelay/badge/?version=latest
    :target: https://sparkfun-circuitpython-qwiicrelay.readthedocs.io/en/latest/
    :alt: Documentation Status

.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://discord.gg/nBQh6qu
    :alt: Discord

.. image:: https://travis-ci.org/fourstix/Sparkfun_CircuitPython_QwiicRelay.svg?branch=master
    :target: https://travis-ci.org/fourstix/Sparkfun_CircuitPython_QwiicRelay
    :alt: Build Status

CircuitPython library for Sparkfun Qwiic Single Relay.  This library is ported from examples
at `SparkFun Qwiic Relay <https://github.com/sparkfun/Qwiic_Relay>`_

.. image:: https://cdn.sparkfun.com//assets/parts/1/3/4/5/1/15093-SparkFun_Qwiic_Single_Relay-01.jpg
    :target: https://www.sparkfun.com/products/15093
    :alt: SparkFun Qwiic Single Relay (COM-15093)

`SparkFun Qwiic Single Relay (COM-15093) <https://www.sparkfun.com/products/15093>`_
  


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `Adafruit Bus Device <https://github.com/adafruit/Adafruit_CircuitPython_BusDevice>`_
* `Qwiic Single Relay Hardware <https://github.com/sparkfun/Qwiic_Relay>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.

Raspberry Pi Setup
------------------
   Adafruit has an excellent tutorial on `Installing CircuitPython Libraries on Raspberry Pi
   <https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi/>`_.
 
Quick Start Summary:

* Start with the latest version of Raspbian with Wifi configured.

* Enable SSH, I2C and SPI.

.. code-block:: shell

    sudo raspi-config

* Update your system to the latest version.

.. code-block:: shell

    sudo apt-get update
    sudo apt-get upgrade

* Update the python tools

.. code-block:: shell

    sudo pip3 install --upgrade setuptools

(If pip3 is not installed, install it and rerun the command)

.. code-block:: shell

    sudo apt-get install python3-pip

* Install the CircuitPython libraries

.. code-block:: shell

    pip3 install RPI.GPIO
    pip3 install adafruit-blinka

Installing from PyPI
--------------------
   On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
   PyPI <https://pypi.org/project/sparkfun-circuitpython-qwiicrelay/>`_.

   Installing this library will also install the dependency adafruit-circuitpython-busdevice.

Installing from PyPI

.. code-block:: shell

    pip3 install sparkfun-circuitpython-qwiicrelay

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install sparkfun-circuitpython-qwiicrelay

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .env
    source .env/bin/activate
    pip3 install sparkfun-circuitpython-qwiicrelay

Usage Example
=============
* `Qwiic Single Relay Hookup Guide <https://learn.sparkfun.com/tutorials/qwiic-single-relay-hookup-guide>`_ - The Arduino examples in the Hookup Guide are available for Python with this library
* `CircuitPython on a Raspberry Pi <https://learn.adafruit.com/circuitpython-on-raspberrypi-linux>`_ - Basic information on how to install CircuitPython on a Raspberry Pi.
* Code Example:

 .. code-block:: shell

     # import the CircuitPython board and busio libraries
     import board
     import busio

     # Create bus object using the board's I2C port
     i2c = busio.I2C(board.SCL, board.SDA)

     relay = QwiicRelay(i2c)  # default address is 0x18

     # For a different address use QwiicRelay(i2c, address)
     # relay = QwiicRelay(i2c, 0x19)


Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/fourstix/Sparkfun_CircuitPython_QwiicRelay/blob/master/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Building locally
================

Zip release files
-----------------

To build this library locally you'll need to install the
`circuitpython-build-tools <https://github.com/adafruit/circuitpython-build-tools>`_ package.

.. code-block:: shell

    python3 -m venv .env
    source .env/bin/activate
    pip install circuitpython-build-tools

Once installed, make sure you are in the virtual environment:

.. code-block:: shell

    source .env/bin/activate

Then run the build:

.. code-block:: shell

    circuitpython-build-bundles --filename_prefix sparkfun-circuitpython-qwiicrelay --library_location .

Sphinx documentation
-----------------------

Sphinx is used to build the documentation based on rST files and comments in the code. First,
install dependencies (feel free to reuse the virtual environment from above):

.. code-block:: shell

    python3 -m venv .env
    source .env/bin/activate
    pip install Sphinx sphinx-rtd-theme

Now, once you have the virtual environment activated:

.. code-block:: shell

    cd docs
    sphinx-build -E -W -b html . _build/html

This will output the documentation to ``docs/_build/html``. Open the index.html in your browser to
view them. It will also (due to -W) error out on any warning like Travis will. This is a good way to
locally verify it will pass.

License Information
-----------------------
This product is **open source**! 

Please review the LICENSE.md file for license information. 

Please use, reuse, and modify these files as you see fit. 

Please maintain the attributions to SparkFun Electronics and Adafruit and release any derivative under the same license.

Distributed as-is; no warranty is given.



