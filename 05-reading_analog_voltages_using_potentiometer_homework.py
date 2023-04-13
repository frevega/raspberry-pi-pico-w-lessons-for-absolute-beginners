# Slope (m) equation
# m =  (y2 - y1)
#      ---------
#      (x2 - x1)
# point 1 (x = 0, y = 100)
# point 2 (x = 65535, y = 0)
# m =  (0 - 100)  = _  100
#     -----------     -----
#     (65535 - 0)     65535
#
#        y 
#            |
#   (0, 100) |---------------------*
#            |      /              |
#            |     /               
#            |    /                |
#            |   /                 
#            |  /                  |  
#            | /                    (65536, 0)
#            |/__ __ __ __ __ __ __|  x
#            0
# Equation of the line
# y - y1 = m (x - x1)
# y - 100 = - (100 / 65535) * (x - 0)
# y = 100 - (100 / 65335) * x
# y = voltage
# x = potentiometer value
# voltage = 100 - (100 / 65335) * potentiometer value

from machine import ADC, Timer
from time import sleep

potPin = ADC(28)
result = 0
timer = Timer(-1)

def main():
    timer.init(mode = Timer.PERIODIC, period = 500, callback = lambda t:print(f"Read = {potPin.read_u16()} \tResult = {result:.2f} \tV = {round(result)}"))
    try:
        while True:
            result = 100 - (100 / 65335) * potPin.read_u16()
#             sleep(.5)
    except KeyboardInterrupt:
        timer.deinit()
        print("See ya later, RPi Pico!")

main()
