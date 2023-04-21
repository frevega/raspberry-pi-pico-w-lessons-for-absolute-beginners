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
leds = [MyPWM(n) for n in [16, 18, 19]]
timer = Timer(mode = Timer.PERIODIC, period = 200, callback = lambda t:print(f"(0) r: {65535 -1 * pots[0].read_u16()} g: {65535 -1 * pots[1].read_u16()} b: {65535 -1 * pots[2].read_u16()}"))
# timer = Timer(mode = Timer.PERIODIC, period = 250, callback = lambda t:print(f"(1) r: {MAP(pots[0].read_u16(), 0, 65535, 65535, 0)} g: {MAP(pots[1].read_u16(), 0, 65535, 65535, 0)} b: {MAP(pots[2].read_u16(), 0, 65535, 65535, 0)}"))
# timer = Timer(mode = Timer.PERIODIC, period = 200, callback = lambda t:print(f"(2) r: {pots[0].read_u16()} g: {pots[1].read_u16()} b: {pots[2].read_u16()}"))
   
def MAP(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def main():
    while True:
#         print(MAP(pots[0].read_u16(), 0, 65535, 65535, 0), end = " ")
#         print(MAP(pots[1].read_u16(), 0, 65535, 65535, 0), end = " ")
#         print(MAP(pots[2].read_u16(), 0, 65535, 65535, 0))
#         sleep(.25)
        for i in range(len(leds)):
            leds[i].duty_u16(65535 -1 * pots[i].read_u16())
            #leds[i].duty_u16(MAP(pots[i].read_u16(), 0, 65535, 65535, 0))
            #leds[i].duty_u16(pots[i].read_u16())
            
#         podsVal[0] = pots[0].read_u16()
#         podsVal[1] = pots[1].read_u16()
#         podsVal[2] = pots[2].read_u16()
#         leds[0].duty_u16(0 if redPodVal < 300 else redPodVal)
#         leds[1].duty_u16(pots[1].read_u16())
#         leds[2].duty_u16(pots[2].read_u16())
try:
    main()
except KeyboardInterrupt:
    timer.deinit()
    [led.duty_u16(0) for led in leds]
    print("\nSee ya later, RPi Pico!")
