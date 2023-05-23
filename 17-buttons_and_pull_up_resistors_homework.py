from machine import Pin
from time import sleep

button = Pin(14, Pin.IN, Pin.PULL_UP)
ledPin = Pin(15, Pin.OUT)
buttonState = [0, 1]

def readButton():
    buttonState[0] = button.value()
    if (buttonState[0] == 1 and buttonState[0] != buttonState[1]):
        ledPin.toggle()
        print("Off" if ledPin.value() == 0 else "On ", end = "\r")
    buttonState[1] = buttonState[0]
    sleep(.1)

try:
    while True:
        readButton()
except KeyboardInterrupt:
    ledPin.value(0)
    print("See you later RPi Pico!")
