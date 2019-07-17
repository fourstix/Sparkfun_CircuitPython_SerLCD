#  This is example is for the SparkFun Serial LCD displays.
#  SparkFun sells these at its website: www.sparkfun.com
#  Do you like this library? Help support SparkFun. Buy a board!
#  https://www.sparkfun.com/products/14072
#  https://www.sparkfun.com/products/14073
#  https://www.sparkfun.com/products/14074

"""
 Serial LCD Example 12 - example12_display_input_text.py
 Written by Gaston Williams, July 14th, 2019
 Based on Arduino code written by Gaston Williams and
 Nathan Seidle @ Sparkfun, August 22, 2018.


 Example 12 - Display Input Text:
 This program takes text typed into the console and writes
 it to the serial displays.
"""
from time import sleep
import board
import busio
from sparkfun_serlcd  import Sparkfun_SerLCD_I2C

i2c = busio.I2C(board.SCL, board.SDA)
serlcd = Sparkfun_SerLCD_I2C(i2c)

print('Example 12: Display Input Text')
print('Press Ctrl-C to end program.')


try:
    while True:
        text = input("Please type some text to display: ")
        serlcd.clear()
        serlcd.write(text)
        sleep(2)

except KeyboardInterrupt:
    pass
