from machine import Pin
from time import sleep

led = Pin(21, Pin.OUT)
    
def blink(repetitions: int, repetitionsDelay: int, avoidInBetweenDelayDelay = False, inBetweenDelay: int = .3):
    for repetition in range(repetitions):
        led.toggle()
        sleep(repetitionsDelay)
        led.toggle()
        sleep(repetitionsDelay if repetition != repetitions - 1 else 0 if avoidInBetweenDelayDelay else inBetweenDelay)

try:
    while True:
        blink(3, .15)
        blink(3, .3)
        blink(3, .15, True)
        led.off()
        sleep(1)
except KeyboardInterrupt:
    print("See ya later, RPi Pico!")
    
# https://en.wikipedia.org/wiki/Morse_code