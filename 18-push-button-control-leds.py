from machine import Pin
from time import sleep

buttons = [Pin(n, Pin.IN, Pin.PULL_UP) for n in [2, 3, 4]]
buttonStates = [[0, 1], [0, 1], [0, 1]]
leds = [Pin(n, Pin.OUT) for n in [16, 17, 18]]
ledStates = [0, 0, 0]

def readButtons():
    global ledStates
    for index, button in enumerate(buttons):
        buttonStates[index][0] = button.value()
        if (buttonStates[index][0] == 1 and buttonStates[index][0] != buttonStates[index][1]):
            ledStates = [1 if idx == index and state == 0 else 0 for idx, state in enumerate(ledStates)]
        buttonStates[index][1] = buttonStates[index][0]
        sleep(.05)
    [leds[idx].value(state) for idx, state in enumerate(ledStates)]
    print(f"R: {ledStates[0]} G: {ledStates[1]} B: {ledStates[2]}", end = "\r")

try:
    while True:
        readButtons()
except KeyboardInterrupt:
    [led.value(0) for led in leds]
    print("See you later RPi Pico!")