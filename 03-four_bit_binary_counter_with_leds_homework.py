from machine import Pin
from time import sleep

leds = list(map(lambda n: Pin(n, Pin.OUT), [21, 20, 19, 18]))
patterns = [
    [0, 0, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 1, 0, 0],
    [0, 1, 0, 1],
    [0, 1, 1, 0],
    [0, 1, 1, 1],
    [1, 0, 0, 0],
    [1, 0, 0, 1],
    [1, 0, 1, 0],
    [1, 0, 1, 1],
    [1, 1, 0, 0],
    [1, 1, 0, 1],
    [1, 1, 1, 0],
    [1, 1, 1, 1]
]

def blink(pattern: [int]):
    for index, led in enumerate(leds):
        led.value(pattern[index])
    sleep(.4)

try:
    while True:
        for pattern in patterns:
            blink(pattern)
except KeyboardInterrupt:
    print("See ya later, RPi Pico!")
