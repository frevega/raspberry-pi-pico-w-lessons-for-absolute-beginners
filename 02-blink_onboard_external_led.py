from machine import Pin
from time import sleep

onboardLed = Pin(25, Pin.OUT)
externalLed = Pin(21, Pin.OUT)

try:
    while True:
        onboardLed.toggle()
        externalLed.value(not onboardLed.value())
        sleep(.25)
except KeyboardInterrupt:
    print("See ya later, RPi Pico!")
    
    
