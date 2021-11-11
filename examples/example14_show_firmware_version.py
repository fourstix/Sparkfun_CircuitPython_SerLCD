# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Gaston Williams
#
# SPDX-License-Identifier: MIT

#  This is example is for the SparkFun Serial LCD displays.
#  SparkFun sells these at its website: www.sparkfun.com
#  Do you like this library? Help support SparkFun. Buy a board!
#  https://www.sparkfun.com/products/14072
#  https://www.sparkfun.com/products/14073
#  https://www.sparkfun.com/products/14074

"""
 Serial LCD Example 12 - example12_show_firmware_version.py
 Written by Gaston Williams, July 16, 2019
 Based on Arduino code written by Gaston Williams and
 Nathan Seidle @ Sparkfun, August 22, 2018.


 Example 12 - Show Firmware Version:
 This program shows the current serial lcd firmware version on the display.
"""
from time import sleep
import board
from sparkfun_serlcd import Sparkfun_SerLCD_I2C

i2c = board.I2C()
serlcd = Sparkfun_SerLCD_I2C(i2c)

print('Example 12: Show Firmware Version')
print('Press Ctrl-C to end program.')

serlcd.clear()

try:
    while True:
        # Display the firmware version for 0.5 second
        serlcd.show_version()
        sleep(0.5)

except KeyboardInterrupt:
    pass
