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
*  16x2 SerLCD Black on RGB https://www.sparkfun.com/products/14702
*  16x2 SerLCD RGB on Black https://www.sparkfun.com/products/14073
*  20x4 SerLCD Black on RGB https://www.sparkfun.com/products/14704

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
"""

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/fourstix/Sparkfun_CircuitPython_SerLCD.git"

# imports
from abc import ABC, abstractmethod
from time import sleep
from micropython import const

# public constants
DEFAULT_I2C_ADDR = const(0x72)
"""Default I2C address for SerLCD"""


# private constants
_MAX_ROWS = const(4)
_MAX_COLS = const(20)

# Character to reset display Splash Screen to default
_DEFAULT_SPLASH_SCREEN = const(0xFF)

# OpenLCD command characters
_SPECIAL_COMMAND = const(254)
_SETTING_COMMAND = const(0x7C)

# OpenLCD commands
# 45, -, the dash character: command to clear and home the display
_CLEAR_COMMAND = const(0x2D)
# Command to change the contrast setting
_CONTRAST_COMMAND = const(0x18)
# Command to change the i2c address
_ADDRESS_COMMAND = const(0x19)
# 43, +, the plus character: command to set backlight RGB value
_SET_RGB_COMMAND = const(0x2B)
# 46, ., command to enable system messages being displayed
_ENABLE_SYSTEM_MESSAGE_DISPLAY = const(0x2E)
# 47, /, command to disable system messages being displayed
_DISABLE_SYSTEM_MESSAGE_DISPLAY = const(0x2F)
# 48, 0, command to enable splash screen at power on
_ENABLE_SPLASH_DISPLAY = const(0x30)
# 49, 1, command to disable splash screen at power on
_DISABLE_SPLASH_DISPLAY = const(0x31)
# 10, Ctrl+j, command to save current text on display as splash
_SAVE_CURRENT_DISPLAY_AS_SPLASH = const(0x0A)
# Show firmware version
_SHOW_VERSION_COMMAND = const(0x2C)
# Software reset of the system
_RESET_COMMAND = const(0x08)

# special commands
_LCD_RETURNHOME = const(0x02)
_LCD_ENTRYMODESET = const(0x04)
_LCD_DISPLAYCONTROL = const(0x08)
_LCD_CURSORSHIFT = const(0x10)
_LCD_SETDDRAMADDR = const(0x80)

# flags for display entry mode
_LCD_ENTRYRIGHT = const(0x00)
_LCD_ENTRYLEFT = const(0x02)
_LCD_ENTRYSHIFTINCREMENT = const(0x01)
_LCD_ENTRYSHIFTDECREMENT = const(0x00)

# flags for display on/off control
_LCD_DISPLAYON = const(0x04)
_LCD_DISPLAYOFF = const(0x00)
_LCD_CURSORON = const(0x02)
_LCD_CURSOROFF = const(0x00)
_LCD_BLINKON = const(0x01)
_LCD_BLINKOFF = const(0x00)

# flags for display/cursor shift
_LCD_DISPLAYMOVE = const(0x08)
_LCD_CURSORMOVE = const(0x00)
_LCD_MOVERIGHT = const(0x04)
_LCD_MOVELEFT = const(0x00)

# private functions

def _map_range(value, in_min, in_max, out_min, out_max):
    """Map an integer value from a range into a value in another range."""
    result = (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    return int(result)

# abstract base class
class Sparkfun_SerLCD(ABC):
    """Abstract base class for Sparkfun AVR-Based Serial LCD display.
    Use the appropriate driver communcation subclass Sprarkfun_SerLCD_I2C()
    for I2C, Sparkfun_SerLCD_SPI() for SPI or Sparkfun_SerLCD_Serial for Serial.
    """
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-public-methods

    def __init__(self):
        self._display_control = _LCD_DISPLAYON | _LCD_CURSOROFF | _LCD_BLINKOFF
        self._display_mode = _LCD_ENTRYLEFT | _LCD_ENTRYSHIFTDECREMENT
        self._begin()

    def command(self, command):
        # pylint: disable=line-too-long
        """Send a command to the display.
            * Command cheat sheet:
            * ASCII  / DEC / HEX
            * '|'    / 124 / 0x7C - Put into setting mode
            * Ctrl+c / 3 / 0x03 - Change width to 20
            * Ctrl+d / 4 / 0x04 - Change width to 16
            * Ctrl+e / 5 / 0x05 - Change lines to 4
            * Ctrl+f / 6 / 0x06 - Change lines to 2
            * Ctrl+g / 7 / 0x07 - Change lines to 1
            * Ctrl+h / 8 / 0x08 - Software reset of the system
            * Ctrl+i / 9 / 0x09 - Enable/disable splash screen
            * Ctrl+j / 10 / 0x0A - Save currently displayed text as splash
            * Ctrl+k / 11 / 0x0B - Change baud to 2400bps
            * Ctrl+l / 12 / 0x0C - Change baud to 4800bps
            * Ctrl+m / 13 / 0x0D - Change baud to 9600bps
            *   Ctrl+n / 14 / 0x0E - Change baud to 14400bps
            * Ctrl+o / 15 / 0x0F - Change baud to 19200bps
            * Ctrl+p / 16 / 0x10 - Change baud to 38400bps
            * Ctrl+q / 17 / 0x11 - Change baud to 57600bps
            * Ctrl+r / 18 / 0x12 - Change baud to 115200bps
            * Ctrl+s / 19 / 0x13 - Change baud to 230400bps
            * Ctrl+t / 20 / 0x14 - Change baud to 460800bps
            * Ctrl+u / 21 / 0x15 - Change baud to 921600bps
            * Ctrl+v / 22 / 0x16 - Change baud to 1000000bps
            * Ctrl+w / 23 / 0x17 - Change baud to 1200bps
            * Ctrl+x / 24 / 0x18 - Change the contrast. Follow Ctrl+x with number 0 to 255. 120 is default.
            * Ctrl+y / 25 / 0x19 - Change the TWI address. Follow Ctrl+x with number 0 to 255. 114 (0x72) is default.
            * Ctrl+z / 26 / 0x1A - Enable/disable ignore RX pin on startup (ignore emergency reset)
            * '+'    / 43 / 0x2B - Set RGB backlight with three following bytes, 0-255
            * ','    / 44 / 0x2C - Display current firmware version
            * '-'    / 45 / 0x2D - Clear display. Move cursor to home position.
            * '.'    / 46 / 0x2E - Enable system messages (ie, display 'Contrast: 5' when changed)
            * '/'    / 47 / 0x2F - Disable system messages (ie, don't display 'Contrast: 5' when changed)
            * '0'    / 48 / 0x30 - Enable splash screen
            * '1'    / 49 / 0x31 - Disable splash screen
            *        / 128-157 / 0x80-0x9D - Set the primary backlight brightness. 128 = Off, 157 = 100%.
            *        / 158-187 / 0x9E-0xBB - Set the green backlight brightness. 158 = Off, 187 = 100%.
            *        / 188-217 / 0xBC-0xD9 - Set the blue backlight brightness. 188 = Off, 217 = 100%.
            * For example, to change the baud rate to 115200 send 124 followed by 18.
        """
        data = bytearray()
        data.append(_SETTING_COMMAND)
        data.append(command & 0xFF)
        self._write_bytes(data)

        # Wait a bit longer for special display commands
        sleep(0.010)


    def clear(self):
        """Clear the display"""
        self.command(_CLEAR_COMMAND)

    def home(self):
        """Send the cursor home"""
        self._special_command(_LCD_RETURNHOME)

    def write(self, message):
        """Write a character string to the display."""
        # Value -> String -> Bytes
        text = str(message).encode()
        self._write_bytes(text)

    def set_cursor(self, col, row):
        """Set the cursor position."""
        row_offsets = [0x00, 0x40, 0x14, 0x54]

        # keep variables in bounds
        # row cannot be less than 0
        row = max(0, row)
        # row cannot be greater than max rows
        row = min(row, _MAX_ROWS - 1)

        # send the command
        self._special_command(_LCD_SETDDRAMADDR | (col + row_offsets[row]))

    def create_character(self, location, charmap):
        """Create a customer character
        location - character number 0 to 7
        charmap  - bytes for character as 8 x 5 bit map"""

        # There are only 8 locations 0-7
        location &= 0x07
        data = bytearray()
        # Send request to create a customer character
        data.append(_SETTING_COMMAND)
        data.append(27 + location)
        for i in range(8):
            # Only the lowest 5 bits are used
            data.append(charmap[i] & 0x1F)
        self._write_bytes(data)
        # This takes a bit longer
        sleep(0.050)

    def write_character(self, location):
        """Write a customer character to the display
        location - character number 0 to 7"""

        # There are only locations 0-7
        location &= 0x07

        self.command(35 + location)

    def set_backlight(self, rgb):
        """Set the backlight with 24-bit RGB value."""
        red = (rgb >> 16) & 0x0000FF
        green = (rgb >> 8) & 0x0000FF
        blue = rgb & 0x0000FF
        self.set_backlight_rgb(red, green, blue)

    def set_backlight_rgb(self, red, green, blue):
        """Set the backlight with byte values for r, g, b"""
        # map the byte value range to backlight command range
        r_value = 128 + _map_range(red, 0, 255, 0, 29)
        g_value = 158 + _map_range(green, 0, 255, 0, 29)
        b_value = 188 + _map_range(blue, 0, 255, 0, 29)

        # send commands to the display to set backlights
        data = bytearray()
        # Turn display off to hide confirmation messages
        self._display_control &= ~_LCD_DISPLAYON
        data.append(_SPECIAL_COMMAND)
        data.append(_LCD_DISPLAYCONTROL | self._display_control)

        # Set the red, green and blue values
        data.append(_SETTING_COMMAND)
        data.append(r_value)
        data.append(_SETTING_COMMAND)
        data.append(g_value)
        data.append(_SETTING_COMMAND)
        data.append(b_value)

        # Turn display back on and end
        self._display_control |= _LCD_DISPLAYON
        data.append(_SPECIAL_COMMAND)
        data.append(_LCD_DISPLAYCONTROL | self._display_control)
        # Send data
        self._write_bytes(data)
        # This one is a bit slow
        sleep(0.050)

    def set_fast_backlight(self, rgb):
        """Set the backlight color by a 24-bit value in one pass."""
        # Convert from hex triplet to byte values
        red = (rgb >> 16) & 0x0000FF
        green = (rgb >> 8) & 0x0000FF
        blue = rgb & 0x0000FF
        self.set_fast_backlight_rgb(red, green, blue)

    def set_fast_backlight_rgb(self, red, green, blue):
        """Set the backlight color in one pass."""
        # Mask values into 0-255 range
        red &= 0x00FF
        green &= 0x00FF
        blue &= 0x00FF

        # Send commands to the display to set backlights
        data = bytearray()
        data.append(_SETTING_COMMAND)
        # Send the set RGB character '+' or plus
        data.append(_SET_RGB_COMMAND)
        data.append(red)
        data.append(green)
        data.append(blue)
        self._write_bytes(data)
        sleep(0.010)

    def display(self, value):
        """Turn the display on and off quickly."""
        if bool(value):
            self._display_control |= _LCD_DISPLAYON
            self._special_command(_LCD_DISPLAYCONTROL | self._display_control)
        else:
            self._display_control &= ~_LCD_DISPLAYON
            self._special_command(_LCD_DISPLAYCONTROL | self._display_control)


    def cursor(self, value):
        """Turn the underline cursor on and off."""
        if bool(value):
            self._display_control |= _LCD_CURSORON
            self._special_command(_LCD_DISPLAYCONTROL | self._display_control)
        else:
            self._display_control &= ~_LCD_CURSORON
            self._special_command(_LCD_DISPLAYCONTROL | self._display_control)

    def blink(self, value):
        """Turn the blink cursor on and off."""
        if bool(value):
            self._display_control |= _LCD_BLINKON
            self._special_command(_LCD_DISPLAYCONTROL | self._display_control)
        else:
            self._display_control &= ~_LCD_BLINKON
            self._special_command(_LCD_DISPLAYCONTROL | self._display_control)

    def system_messages(self, enable):
        """Enable or disable the printint of messages like 'UART: 57600' or 'Contrast: 5'"""
        if bool(enable):
            # Send the set '.' character
            self.command(_ENABLE_SYSTEM_MESSAGE_DISPLAY)
        else:
            # Send the set '/' character
            self.command(_DISABLE_SYSTEM_MESSAGE_DISPLAY)
        sleep(0.010)

    def autoscroll(self, enable):
        """Turn autoscrolling on and off."""
        if bool(enable):
            self._display_mode |= _LCD_ENTRYSHIFTINCREMENT
            self._special_command(_LCD_ENTRYMODESET | self._display_mode)
        else:
            self._display_mode &= ~_LCD_ENTRYSHIFTINCREMENT
            self._special_command(_LCD_ENTRYMODESET | self._display_mode)
        sleep(0.010)

    def set_contrast(self, value):
        """Set the display contrast."""
        data = bytearray()
        data.append(_SETTING_COMMAND)
        data.append(_CONTRAST_COMMAND)
        data.append(value & 0x00FF)
        self._write_bytes(data)
        sleep(0.010)

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

    def scroll_display_left(self, count=1):
        """Scroll the display to the left"""
        self._special_command(_LCD_CURSORSHIFT | _LCD_DISPLAYMOVE | _LCD_MOVELEFT, count)

    def scroll_display_right(self, count=1):
        """Scroll the display to the right"""
        self._special_command(_LCD_CURSORSHIFT | _LCD_DISPLAYMOVE | _LCD_MOVERIGHT, count)

    def move_cursor_left(self, count=1):
        """Move the cursor to the left"""
        self._special_command(_LCD_CURSORSHIFT | _LCD_CURSORMOVE | _LCD_MOVELEFT, count)

    def move_cursor_right(self, count=1):
        """Scroll the display to the right"""
        self._special_command(_LCD_CURSORSHIFT | _LCD_CURSORMOVE | _LCD_MOVERIGHT, count)

    def splash_screen(self, enable):
        """Enable or disable the splash screem."""
        if bool(enable):
            self.command(_ENABLE_SPLASH_DISPLAY)
        else:
            self.command(_DISABLE_SPLASH_DISPLAY)
        sleep(0.010)

    def save_splash_screen(self):
        """Save the current display as the splash screem."""
        self.command(_SAVE_CURRENT_DISPLAY_AS_SPLASH)
        sleep(0.010)

    def left_to_right(self):
        """Set the text to flow from left to right.  This is the direction
        that is common to most Western languages."""
        self._display_mode |= _LCD_ENTRYLEFT
        self._special_command(_LCD_ENTRYMODESET | self._display_mode)

    def right_to_left(self):
        """Set the text to flow from right to left."""
        self._display_mode &= ~_LCD_ENTRYLEFT
        self._special_command(_LCD_ENTRYMODESET | self._display_mode)

    def show_version(self):
        """Show the firmware version on the display."""
        self.command(_SHOW_VERSION_COMMAND)

    def reset(self):
        """Perform a software reset on the dislay."""
        self.command(_RESET_COMMAND)

    def default_splash_screen(self):
        """ Result to the default splash screen"""
        # Clear the display
        self.clear()
        # put the default charater
        self._put_char(_DEFAULT_SPLASH_SCREEN)
        # Wait a bit
        sleep(0.200)
        self.save_splash_screen()

    # abstract methods

    @abstractmethod
    def _write_bytes(self, data):
        pass

    @abstractmethod
    def _change_i2c_address(self, addr):
        pass

    # private functions

    def _begin(self):
        """Initialize the display"""
        data = bytearray()
        # Send special command character
        data.append(_SPECIAL_COMMAND)
        # Send the display command
        data.append(_LCD_DISPLAYCONTROL | self._display_control)
        # Send special command character
        data.append(_SPECIAL_COMMAND)
        # Send the entry mode command
        data.append(_LCD_ENTRYMODESET | self._display_mode)
        # Put LCD into setting mode
        data.append(_SETTING_COMMAND)
        # Send clear display command
        data.append(_CLEAR_COMMAND)
        self._write_bytes(data)
        sleep(0.050)

    def _special_command(self, command, count=1):
        """Send a special command to the display.  Used by other functions."""
        data = bytearray()
        data.append(_SPECIAL_COMMAND)
        for _ in range(count):
            data.append(command & 0xFF)
        self._write_bytes(data)

        # Wait a bit longer for special display commands
        sleep(0.050)


    def _put_char(self, char):
        """Send a character byte directly to display, no encoding"""
        data = bytearray()
        data.append(char & 0xFF)
        self._write_bytes(data)


# concrete subclass for I2C
class Sparkfun_SerLCD_I2C(Sparkfun_SerLCD):
    """Driver subclass for Sparkfun Serial Displays over I2C communication"""
    def __init__(self, i2c, address=DEFAULT_I2C_ADDR):
        import adafruit_bus_device.i2c_device as i2c_device
        self._i2c_device = i2c_device.I2CDevice(i2c, address)
        self._i2c = i2c
        super().__init__()


    def _write_bytes(self, data):
        with self._i2c_device as device:
            device.write(data)

    def _change_i2c_address(self, addr):
        import adafruit_bus_device.i2c_device as i2c_device
        self._i2c_device = i2c_device.I2CDevice(self._i2c, addr)

# concrete subclass for SPI
class Sparkfun_SerLCD_SPI(Sparkfun_SerLCD):
    """Driver subclass for Sparkfun Serial LCD display over SPI communication"""
    def __init__(self, spi, cs):
        import adafruit_bus_device.spi_device as spi_device
        self._spi_device = spi_device.SPIDevice(spi, cs)
        super().__init__()


    def _write_bytes(self, data):
        with self._spi_device as device:
            #pylint: disable=no-member
            device.write(data)

    def _change_i2c_address(self, addr):
        # No i2c address change for SPI
        pass

# concrete subclass for Serial
class Sparkfun_SerLCD_Serial(Sparkfun_SerLCD):
    """Driver subclass for Sparkfun Serial LCD display over Serial communication"""
    def __init__(self, uart):
        self._uart = uart
        super().__init__()

    def _write_bytes(self, data):
        self._uart.write(data)

    def _change_i2c_address(self, addr):
        # No i2c address change for UART
        pass
