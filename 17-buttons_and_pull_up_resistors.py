from machine import Pin
from time import sleep

button = Pin(14, Pin.IN, Pin.PULL_UP)

try:
    while True:
        print(button.value(), end = "\r")
        sleep(.1)
except KeyboardInterrupt:
    print("See you later RPi Pico!")