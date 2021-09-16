# The MIT License (MIT)
#
# Copyright (c) 2019 Gaston Williams
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`sparkfun_serlcd`
================================================================================

CircuitPython driver library for the Sparkfun Serial LCD displays


* Author(s): Gaston Williams

* Based on the Arduino library for the Sparkfun SerLCD displays
  Written by Gaston Williams, August 22, 2018
* Based on sample code provided with the SparkFun Serial OpenLCD display.
  The original LiquidCrystal library was written by David A. Mellis and
  modified by Limor Fried @ Adafruit and the OpenLCD code was written by
  Nathan Seidle @ SparkFun.


Implementation Notes
--------------------

**Hardware:**

*  This is library is for the SparkFun Serial LCD displays
*  SparkFun sells these at its website: www.sparkfun.com
*  Do you like this library? Help support SparkFun. Buy a board!
*  16x2 SerLCD Black on RGB https://www.sparkfun.com/products/14072
*  16x2 SerLCD RGB on Black https://www.sparkfun.com/products/14073
*  20x4 SerLCD Black on RGB https://www.sparkfun.com/products/14074

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
"""

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/fourstix/Sparkfun_CircuitPython_SerLCD.git"

# imports
// from abc import ABC, abstractmethod  // Please no abstractmethods, CircuitPython is not Python 3 
from time import sleep
from micropython import const
from sparkfun_serlcd.py import Sparkfun_SerLCD:


# public constants
DEFAULT_I2C_ADDR = const(0x72)
"""Default I2C address for SerLCD"""

# sparkfun_serlcd_i2c.py
class Sparkfun_SerLCD_i2c(Sparkfun_SerLCD):
"""Sparkfun SerLCD connected to I2C
This is a subclass of 'Sparkfun_SerLCD' and implements 
all of the same functions.

"""

def __init__(self, i2c, columns, lines, address=None):
    

def set_i2c_address(self, new_address):
    """Change the I2C Address. 0x72 is the default.
    Note that this change is persistent.  If anything goes wrong
    you may need to do a hardware reset to unbrick the display.

    byte new_addr - new i2c address"""
    # Mask new address to byte
    new_address &= 0x00FF
    # Transmit to device on old address
    data = bytearray()
    # Send contrast command
    data.append(_SETTING_COMMAND)
    data.append(_ADDRESS_COMMAND) # 0x19
    data.append(new_address)
    self._write_bytes(data)
    # Update our own address so we can still talk to the display
    self._change_i2c_address(new_address)

    # This may take awhile
    sleep(0.050)
