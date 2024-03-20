# Draw a circle titled my circle
#
from machine import Pin, I2C
from sh1106 import SH1106_I2C
from math import radians, cos, sin, pi
import time

SCREEN_WIDTH = 128
SCREN_HEIGHT = 64
RADIUS = 31
phase = 0

i2c = I2C(0, sda = Pin(0), scl = Pin(1), freq = 400000)
display = SH1106_I2C(SCREEN_WIDTH, SCREN_HEIGHT, i2c, rotate = 180)
display.sleep(False)

a = [1] * 35       # 1
a.extend([1] * 30) # 2
a.extend([2] * 45) # 3
a.extend([2] * 30) # 4
a.extend([3] * 30) # 5
a.extend([3] * 35) # 6
a.extend([5] * 35) # 7
a.extend([5] * 35) # 8
a.extend([5] * 35) # 9
a.extend([1] * 35) # 10
a.extend([7] * 35) # 11
a.extend([2] * 35) # 12
a.extend([9] * 35) # 13

b = [1] * 35       # 1
b.extend([2] * 30) # 2
b.extend([1] * 45) # 3
b.extend([3] * 30) # 4
b.extend([2] * 30) # 5
b.extend([5] * 35) # 6
b.extend([3] * 35) # 7
b.extend([7] * 35) # 8
b.extend([3] * 35) # 9
b.extend([7] * 35) # 10
b.extend([1] * 35) # 11
b.extend([9] * 35) # 12
b.extend([2] * 35) # 13

currentZ = None
while True:
    for z in range(0, len(a)):
        for x in range(0, 360):
            if currentZ != b[z]:
                phase = 0
                print("Pattern", a[z], b[z], end = "\r")
        # Radians formula: rads = x * 2 * pi / 360
            rads = radians(x)
            x = int(2 * RADIUS * cos(a[z] * rads + phase) + (SCREEN_WIDTH / 2))
            y = int(RADIUS * sin(b[z] * rads) + (SCREN_HEIGHT / 2))
            display.pixel(x, y, 1)
        display.show()
        display.fill(0)
        phase += radians(8)
        currentZ = b[z]

