#  This is example is for the SparkFun Serial LCD displays.
#  SparkFun sells these at its website: www.sparkfun.com
#  Do you like this library? Help support SparkFun. Buy a board!
#  https://www.sparkfun.com/products/14702
#  https://www.sparkfun.com/products/14703
#  https://www.sparkfun.com/products/14704

"""
 Serial LCD Example 12 - example12_show_firmware_version.py
 Written by Gaston Williams, July 14th, 2019
 Based on Arduino code written by Gaston Williams and
 Nathan Seidle @ Sparkfun, August 22, 2018.


 Example 12 - Show Firmware Version:
 This program shows the current serial lcd firmware version on the display.
"""
from time import sleep
import board
import busio
from sparkfun_serlcd import Sparkfun_SerLCD_I2C

i2c = busio.I2C(board.SCL, board.SDA)
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
