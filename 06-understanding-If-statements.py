# Slope (m) equation
# m =  (y2 - y1)
#      ---------
#      (x2 - x1)
# point 1 (x = 0, y = 0)
# point 2 (x = 65535, y = 100)
# m =  (100 - 0)  =   100
#     -----------    -----
#     (65535 - 0)    65535
#
#        y 
#            |
#            |
#            |
#            |
#            |
#            |
#            |
#            |            (65536, 100)
#    (0, 0)  |__ __ __ __  __ __ __  x
#            0
# Equation of the line
# y - y1 = m (x - x1)
# y - 0 = (100 / 65535) * (x - 0)
# y = (100 / 65335) * x
# y = value
# x = potentiometer value
# voltage = (100 / 65335) * potentiometer value

from machine import ADC, Pin, Timer
from time import sleep

potPin = ADC(28)
leds = [Pin(n, Pin.OUT) for n in [13, 14, 15]]
result = 0
timer = Timer(-1)

def toggle(pin: Pin, result: int, color: str):
    if pin.value() == 0:
        print(f"toggle: result = {result}, {color}")
        [led.on() if led == pin else led.off() for led in leds]

def main():
    timer.init(mode = Timer.PERIODIC, period = 500, callback = lambda t:print(f"result = {result}"))
    while True:
        result = round((100 / 65335) * potPin.read_u16())
        if result in range(0, 80):
            toggle(leds[0], result, "green")
        elif result in range(80, 95):
            toggle(leds[1], result, "yellow")
        else:
            toggle(leds[2], result, "red")
        sleep(.5)

try:
    main()
except KeyboardInterrupt:
    timer.deinit()
    [led.off() for led in leds]
    print("See ya later, RPi Pico!")

