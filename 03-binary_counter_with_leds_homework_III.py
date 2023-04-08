from machine import Pin
from time import sleep

# leds = list(map(lambda n: Pin(n, Pin.OUT), [16, 17, 18, 19, 20, 21, 22, 26, 27, 28, 15, 14, 13, 12]))
leds = [Pin(n, Pin.OUT) for n in [16, 17, 18, 19, 20, 21, 22, 26, 27, 28, 15, 14, 13, 12]]

MAX_ITERATIONS = 16384

try:
    while True:
        for iteration in range(MAX_ITERATIONS):
            for index, led in enumerate(leds):
                led.value(int(iteration / 2 ** index) % 2)
            sleep(.001 if iteration < MAX_ITERATIONS -1 else 1)
except KeyboardInterrupt:
    [led.off() for led in leds]
    print("See ya later, RPi Pico!")