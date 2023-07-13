# MicroPython SH1106 OLED driver
#
# Pin Map I2C for ESP8266
#   - 3v - xxxxxx   - Vcc
#   - G  - xxxxxx   - Gnd
#   - D2 - GPIO 5   - SCK / SCL
#   - D1 - GPIO 4   - DIN / SDA
#   - D0 - GPIO 16  - Res (required, unless a Hardware reset circuit is connected)
#   - G  - xxxxxx     CS
#   - G  - xxxxxx     D/C
#
# Pin's for I2C can be set almost arbitrary
#
from machine import Pin, I2C
from sh1106 import SH1106_I2C
from time import sleep

i2c = I2C(0, sda = Pin(0), scl = Pin(1), freq = 400000)
display = SH1106_I2C(128, 64, i2c, rotate = 180)
display.sleep(False)
display.fill(0)
display.text('Hello World!', 0, 0)
display.text('Welcome', 0, 8)
display.pixel(60, 25, 1)
display.hline(20, 20, 40, True)
display.vline(20, 20, 40, True)
display.line(20, 20, 118, 118, True)
display.rect(64, 32, 30, 20, True)
display.fill_rect(72, 38, 15, 10, True)
display.show()
sleep(1)
display.invert(True)
sleep(1)
display.invert(False)
sleep(1)
display.poweroff()
sleep(1)
display.poweron()