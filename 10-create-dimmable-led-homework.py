# Slope (m) equation
# m =  (y2 - y1)
#      ---------
#      (x2 - x1)
# point 1 (x = 0, y = 0)
# point 2 (x = 65535, y = 16)
# m =  (16 - 0)  =     16
#     -----------     -----
#     65535           65535
#
#        y = duty
#            |
#            |
#            |                    
#            |                    
#            |                    
#            |                    
#            |                      
#            |                     (65000, 65535)
#    (400, 0)  |__ __ __ __ __ __ __|  x = pot val
#           0
# Equation of the line
# y - y1 = m (x - x1)
# y - 0 = (16 / 65535) * (x - 0)
# y = (16 / 65135) * x
# y = voltage
# x = potentiometer value
# voltage = (16 / 65135) * potentiometer value

# FOR 50 STEPS
# brightness = n ** 50
#             
#          50
# 65535 = n
#
# To eliminate exponents, we elevate bot numbers to 1/50
# and then, ((n ** 50) ** 1/50), remove exponent multiply them 50 * 1/50 = 1,
# then first number to the powr will gave us our number
#
#                1/50  = 50/50
#     1/50    50
# 65535    = n
# 
#     1/50    
# 65535    = n
# 
# 1.2483301679385130095 = n
# 
# exp = 50/65535 * pot
# 
# brightness = 1.2483301679385130095 ** exp

from machine import PWM, Pin, ADC, Timer
from time import sleep

class MyPWM(PWM):
    def __init__(self, pinNumber: int, freq: int = 1000, duty_u16: uint16 = 0):
        super().__init__(Pin(pinNumber))
        self.freq(freq)
        self.duty_u16(duty_u16)
        
        

potPin = ADC(28)
pwmPin = MyPWM(16)
exponent = 0
dutyValue = 0
timer = Timer(-1)

def main():
    timer.init(mode = Timer.PERIODIC, period = 500, callback = lambda t:print(exponent, dutyValue, pwmPin.freq(), pwmPin.duty_u16()))
    while True:
        exponent = int((100 / 65535) * potPin.read_u16())
        dutyValue = int(1.11728696758644464621 ** exponent)
        pwmPin.duty_u16(dutyValue)

try:
    main()
except KeyboardInterrupt:
    timer.deinit()
    print("See ya later, RPi Pico!")
