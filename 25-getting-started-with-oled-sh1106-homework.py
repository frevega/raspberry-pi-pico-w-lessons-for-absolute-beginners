# Draw a circle titled my circle
#
from machine import Pin, I2C
from sh1106 import SH1106_I2C
from math import radians, cos, sin, pi

SCREEN_WIDTH = 128
SCREN_HEIGHT = 64
RADIUS = 25

i2c = I2C(0, sda = Pin(0), scl = Pin(1), freq = 400000)
display = SH1106_I2C(SCREEN_WIDTH, SCREN_HEIGHT, i2c, rotate = 180)
display.sleep(False)

display.fill(0)
text = "My Circle"
xPos = int((SCREEN_WIDTH - len(text) * 8) / 2)
display.text(text, xPos, 0)
display.show()

for RADIUS in range(15, 25):
    for x in range(0, 360):
    #     rads = x * 2 * pi / 360
        rads = radians(x)
        x = RADIUS * cos(rads) + (SCREEN_WIDTH / 2)
        y = RADIUS * sin(rads) + (SCREN_HEIGHT / 2) + 4
        display.pixel(int(x), int(y), 1)
    display.show()
