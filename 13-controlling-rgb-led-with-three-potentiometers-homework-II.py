# point 1 (x1 = 0,   y1 = 65535)
# point 2 (x2 = 65535, y2 = 0)
#
# Slope (m) equation
# m =  (y2 - y1)
#      ---------
#      (x2 - x1)
# m = (65535 - 0)     65535    -1
#     ----------- = - ----- =
#     (0 - 65535)     65535
#
#        y 
#            |
# (0, 65535) |---------------------*
#            |      /              |
#            |     /               
#            |    /                |
#            |   /                 
#            |  /                  |  
#            | /                    (65535, 0)
#            |/__ __ __ __ __ __ __|  x
#            0
#
# Equation of the line
# y - y1 = m (x - x1)
# y - 65535 = -1 * (x - 0)
# y = 65535 -1 * x
# y = duty
# x = potentiometer value
# duty = 65535 -1 * potentiometer value

from machine import Pin, PWM, ADC, Timer
from time import sleep

class MyPWM(PWM):
    def __init__(self, pinNumber: int, freq: int = 1000, duty_u16: uint16 = 0):
        super().__init__(Pin(pinNumber))
        self.freq(freq)
        self.duty_u16(duty_u16)

pots = [ADC(n) for n in [26, 27, 28]]
leds = [MyPWM(n) for n in [16, 17, 18]]
# timer = Timer(mode = Timer.PERIODIC, period = 200, callback = lambda t:print(f"r: {65535 -1 * pots[0].read_u16()} g: {65535 -1 * pots[1].read_u16()} b: {65535 -1 * pots[2].read_u16()}"))
timer = Timer(
    mode = Timer.PERIODIC,
    period = 200,
    callback = lambda t:print(f"r: {65535 if pots[0].read_u16() >= 65400 else 0 if pots[0].read_u16() < 550 else pots[0].read_u16()} g: {65535 if pots[1].read_u16() >= 65400 else 0 if pots[1].read_u16() < 550 else pots[1].read_u16()} b: {65535 if pots[2].read_u16() >= 65400 else 0 if pots[2].read_u16() < 550 else pots[2].read_u16()}")
)

def main():
    while True:
        for i in range(len(leds)):
            leds[i].duty_u16(65535 -1 * (65535 if pots[i].read_u16() >= 65400 else 0 if pots[i].read_u16() < 400 else pots[i].read_u16()))
try:
    main()
except KeyboardInterrupt:
    timer.deinit()
    [led.duty_u16(0) for led in leds]
    print("\nSee ya later, RPi Pico!")