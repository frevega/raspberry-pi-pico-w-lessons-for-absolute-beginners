from ssd1306 import SSD1306_I2C
from machine import Pin, I2C
from time import sleep

i2c = I2C(0, sda = Pin(4), scl = Pin(5), freq = 400000)
display = SSD1306_I2C(128, 64, i2c)
# display = SSD1306_I2C(96, 16, i2c)

display.text("Hello World!", 0, 0)
display.text("Freddy", 0, 8)
display.show()