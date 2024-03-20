# Draw a circle titled my circle
#
from machine import Pin, I2C
from sh1106 import SH1106_I2C
from math import radians, cos, sin, pi

SCREEN_WIDTH = 128
SCREN_HEIGHT = 64
RADIUS = 31
phase = 0

i2c = I2C(0, sda = Pin(0), scl = Pin(1), freq = 400000)
display = SH1106_I2C(SCREEN_WIDTH, SCREN_HEIGHT, i2c, rotate = 180)
display.sleep(False)

while True:
    for x in range(0, 360):
    #     rads = x * 2 * pi / 360
        rads = radians(x)
        x = 2 * RADIUS * cos(rads + phase) + (SCREEN_WIDTH / 2)
        y = 1 * RADIUS * sin(2 * rads) + (SCREN_HEIGHT / 2)
        display.pixel(int(x), int(y), 1)
    display.show()
    display.fill(0)
    phase += radians(1)

