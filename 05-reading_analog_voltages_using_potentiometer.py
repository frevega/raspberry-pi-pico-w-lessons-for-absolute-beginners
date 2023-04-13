from machine import ADC
from time import sleep

potPin = ADC(28)

# Slope (m) equation
#  x, y     x, y
# (0, 0) (65535, 3.3)
# m =  (y2 - y1)
#      ---------
#      (x2 - x1)

# Equation of the line
# y - y1 = m (x - x1)
# y - 0 = ((3.3 - 0) / (65335 - 0)) * (x - 0)
# y = ((3.3 - 0) / (65335 - 0)) * (x - 0)
# y = (3.3 / 65335) * x
# y = voltage
# x = potentiometer value

def main():
    try:
        while True:
            print(f"Read = {potPin.read_u16()} \tV = {(3.3 / 65335) * potPin.read_u16():.2f}")
            sleep(.5)
    except KeyboardInterrupt:
        print("See ya later, RPi Pico!")

main()


