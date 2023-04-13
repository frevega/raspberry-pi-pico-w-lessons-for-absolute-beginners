# Slope (m) equation
# m =  (y2 - y1)
#      ---------
#      (x2 - x1)
# point 1 (x = 0, y = 0)
# point 2 (x = 3.3, y = 65535)
# m =  (65535 - 0)  =   65535
#     -----------       -----
#      (3.3 - 0)         3.3
#
#        y 
#            |
#            +            (3.3, 65535)
#            |
#            |
#            |
#            |
#            |
#            |
#    (0, 0)  |__ __ __ __  __ __ _|_  x
#            0
# Equation of the line
# y - y1 = m (x - x1)
# y - 0 = (65535 / 3.3) * (x - 0)
# y = (65535 / 3.3) * x
# y = pwm value
# x = voltage value
# pwm = (65535 / 3.3) * voltage value

from machine import PWM, Pin
from time import sleep

pwmPin = PWM(Pin(16))
pwmPin.freq(1000) # 1 millisecond
pwmPin.duty_u16(0)
voltage = 0
dutyValue = 0
dutyRange = range(0, 65536)

def main():
    while True:
        try:
            voltage = float(input(f"What voltage would you like? (0, 3.3): "))
            dutyValue = int((65535 / 3.3) * voltage)
            if dutyValue in dutyRange:
                print(f"voltage: {voltage}, dutyValue = {dutyValue}")
                pwmPin.duty_u16(dutyValue)
                #sleep(.1)
            else:
                print(f"Voltage out of range: {voltage}")
        except ValueError:
            print("Invalid value, please enter numbers only")

try:
    main()
except KeyboardInterrupt:
    pwmPin.duty_u16(0)
    print("\nSee ya later, RPi Pico!")