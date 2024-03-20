from time import ticks_add, ticks_ms, ticks_diff, sleep
from machine import Pin
import sys
     
led = Pin("LED", Pin.OUT, value = 0)

deadline = ticks_add(ticks_ms(), 1000)

while True:
    currentMillis = ticks_ms()
    if ticks_diff(deadline, currentMillis) < 0:
        led.toggle()
        deadline = ticks_add(currentMillis, 1000)