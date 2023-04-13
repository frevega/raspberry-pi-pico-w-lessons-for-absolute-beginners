from machine import Pin
from time import sleep

leds = [Pin(n, Pin.OUT) for n in [16, 17, 18, 19, 20, 21, 22, 26, 27, 28, 15, 14, 13, 12]]

def animation(range: range, delay: float):
    for i in range:
        if i + 3 <= len(leds) -1:
            leds[i +3].off()
        leds[i -3].off()
        leds[i].on()
        sleep(delay)
        
def animationTwo(firstRange: range, secondRangeArgs, delay: float):
    for i in firstRange:
        for j in range(i, secondRangeArgs[0], secondRangeArgs[1]):
            leds[j].on()
            sleep(delay)
            leds[j].off()

def animationThree():
    for i in range(int(len(leds) / 2), len(leds), 1):
        for j in range(i, len(leds), 1):
            leds[i].on()
            leds[len(leds) -1 - i].on()
            sleep(i * j ** -2.5)
        

def larsonScanner():
    for _ in range(5):
        animation(range(len(leds) -1, -1, -1), .035)
        animation(range(len(leds)), .035)

def rapidBurstEffectRight():
    animationTwo(range(len(leds) -1, -1, -1), (-1, -1), .025)
    animationTwo(range(len(leds)), (-1, -1), .025)

def rapidBurstEffectLeft():
    animationTwo(range(len(leds)), (len(leds), 1), .025)
    animationTwo(range(len(leds) -1, -1, -1), (len(leds), 1), .025)

def main():
    try:
        while True:
            animationThree()
#             animationTwo(range(int(len(leds) / 2)), (int(len(leds) / 2), 1), .025)
#             animationTwo(range(int(len(leds) / 2) -1, -1, -1), (-1, -1), .025)
#             animationTwo(range(int(len(leds) / 2) -1, -1, -1), (-1, -1), .025)
            rapidBurstEffectLeft()
            larsonScanner()
            rapidBurstEffectRight()
    except KeyboardInterrupt:
        [led.off() for led in leds]
        print("See ya later, RPi Pico!")

main()