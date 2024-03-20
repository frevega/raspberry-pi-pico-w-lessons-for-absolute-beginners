import neopixel
from machine import Pin

rgb = (180, 100, 75)
lightIntensity = 0.025
neopixels = neopixel.NeoPixel(Pin(15), 16)
neopixels.fill((int(rgb[0] * lightIntensity), int(rgb[1] * lightIntensity), int(rgb[2] * lightIntensity)))
neopixels.write()