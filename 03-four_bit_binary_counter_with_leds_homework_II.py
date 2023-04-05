from machine import Pin
from time import sleep

leds = list(map(lambda n: Pin(n, Pin.OUT), [21, 20, 19, 18]))

try:
    while True:
        for i in range(16):
            leds[0].value(int(i / 8) % 2)
            leds[1].value(int(i / 4) % 2)
            leds[2].value(int(i / 2) % 2)
            leds[3].value(i % 2)
            sleep(.3)
except KeyboardInterrupt:
    print("See ya later, RPi Pico!")