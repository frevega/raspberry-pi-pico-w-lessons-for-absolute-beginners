from machine import Pin
from time import sleep

led = Pin(25, Pin.OUT)

# for _ in range(20):
while True:
    led.toggle()
    sleep(.013)
