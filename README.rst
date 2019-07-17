Introduction
============

.. image:: https://readthedocs.org/projects/sparkfun-circuitpython-serlcd/badge/?version=latest
    :target: https://sparkfun-circuitpython-serlcd.readthedocs.io/en/latest/
    :alt: Documentation Status

.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://discord.gg/nBQh6qu
    :alt: Discord

.. image:: https://travis-ci.org/fourstix/Sparkfun_CircuitPython_SerLCD.svg?branch=master
    :target: https://travis-ci.org/fourstix/Sparkfun_CircuitPython_SerLCD
    :alt: Build Status

CircuitPython library for the Sparkfun SerLCD displays. This library is ported from
`SparkFun SerLCD Arduino Library <https://github.com/sparkfun/SparkFun_SerLCD_Arduino_Library>`_

`SparkFun 16x2 SerLCD - Black on RGB 3.3V (LCD-14072) <https://www.sparkfun.com/products/14072>`_

.. image:: https://cdn.sparkfun.com/r/140-140/assets/parts/1/1/9/2/5/14072-SparkFun_16x2_SerLCD_-_Black_on_RGB_3.3V-05.jpg
    :target: https://www.sparkfun.com/products/14072
    :alt: SparkFun 16x2 SerLCD - Black on RGB 3.3V (LCD-14072)

`SparkFun 16x2 SerLCD - RGB on Black 3.3V (LCD-14073) <https://www.sparkfun.com/products/14073>`_

.. image:: https://cdn.sparkfun.com/r/140-140/assets/parts/1/1/9/2/6/14073-SparkFun_16x2_SerLCD_-_RGB_on_Black_3.3V-05.jpg
    :target: https://www.sparkfun.com/products/14073
    :alt: SparkFun 16x2 SerLCD - RGB on Black 3.3V (LCD-14073)

`SparkFun 20x4 SerLCD - Black on RGB 3.3V (LCD-14074) <https://www.sparkfun.com/products/14074>`_

.. image:: https://cdn.sparkfun.com/r/140-140/assets/parts/1/1/9/2/7/14074-SparkFun_20x4_SerLCD_-_Black_on_RGB_3.3V-05.jpg
    :target: https://www.sparkfun.com/products/14074
    :alt: SparkFun 20x4 SerLCD - Black on RGB 3.3V (LCD-14074)

Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `Adafruit Bus Device <https://github.com/adafruit/Adafruit_CircuitPython_BusDevice>`_
* `Sparkfun SerLCD Hardware <https://github.com/sparkfun/OpenLCD>`_

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
=====================

.. code-block:: shell

    pip3 install sparkfun-circuitpython-serlcd

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install sparkfun-circuitpython-serlcd

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .env
    source .env/bin/activate
    pip3 install adafruit-circuitpython-serlcd

Usage Example
=============
* `Sparkfun SerLCD Hookup Guide <https://learn.sparkfun.com/tutorials/avr-based-serial-enabled-lcds-hookup-guide>`_ - The Arduino examples in the Hookup Guide are available for Python with this library
* `CircuitPython on a Raspberry Pi <https://learn.adafruit.com/circuitpython-on-raspberrypi-linux>`_ - Basic information on how to install CircuitPython on a Raspberry Pi.

* Code Example:

 .. code-block:: shell
    
    # import the CircuitPython board and busio libraries
    import board
    import busio
    
    # Enable I2C (Qwiic) communication
    from sparkfun_serlcd import Sparkfun_SerLCD_I2C
    i2c = busio.I2C(board.SCL, board.SDA)
    serlcd = Sparkfun_SerLCD_I2C(i2c)

    # Enable SPI communication
    #import digitalio
    #from sparkfun_serlcd import Sparkfun_SerLCD_SPI
    #spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
    #
    # Set up chip select, CE0 or D8 is labeled CS on Sparkfun Pi Hat
    #cs = digitalio.DigitalInOut(board.CE0)
    #cs.direction = digitalio.Direction.OUTPUT
    #
    #serlcd = Sparkfun_SerLCD_SPI(spi, cs)

    # Enable UART Serial communication
    # SerLCD is connected to the RPi via a USB to TTL 3.3v Serial Cable:
    # https://www.sparkfun.com/products/12977
    # https://www.adafruit.com/product/954
    #import serial
    #from sparkfun_serlcd import Sparkfun_SerLCD_UART
    #
    #usb0 = serial.Serial(
    #        port='/dev/ttyUSB0',
    #        baudrate = 9600,
    #        parity=serial.PARITY_NONE,
    #        stopbits=serial.STOPBITS_ONE,
    #        bytesize=serial.EIGHTBITS,
    #        timeout=1)
    #
    #serlcd = Sparkfun_SerLCD_UART(usb0)

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/fourstix/Sparkfun_CircuitPython_SerLCD/blob/master/CODE_OF_CONDUCT.md>`_
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

    circuitpython-build-bundles --filename_prefix sparkfun-circuitpython-serlcd --library_location .

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
