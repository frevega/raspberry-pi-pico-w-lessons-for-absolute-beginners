from machine import Pin
from time import sleep

leds = list(map(lambda n: Pin(n, Pin.OUT), [16, 17, 18, 19, 20, 21, 22, 26, 27, 28, 15, 14, 13, 12]))
reversed = 1

def larsonScanner():
    global reversed
    for i in range(len(leds) -1, -1, -1) if reversed > 0 else range(len(leds)):
        if i + 1 <= len(leds) -1:
            leds[i +1].off()
        leds[i -1].off()
        leds[i].on()
        sleep(.07)
    reversed *= -1
    
def other():
    global reversed
    for i in range(int(len(leds) / 2) -1, -1, -1) if reversed > 0 else range(int(len(leds) / 2)):
        leds[i].toggle()
        sleep(.07)
    for i in range(int(len(leds) / 2) -1, -8, -1) if reversed > 0 else range(7, int(len(leds) / 2)):
        leds[i].toggle()
        sleep(.07)
    reversed *= -1

try:
    while True:
       other()
except KeyboardInterrupt:
    [led.off() for led in leds]
    print("See ya later, RPi Pico!")