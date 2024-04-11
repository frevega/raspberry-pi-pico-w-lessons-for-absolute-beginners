from machine import ADC, Pin, Timer
from MyLib import MyPWM

servo = MyPWM(pinNumber = 15, freq = 50)
pot_pin = ADC(28)
Pin(23, Pin.OUT, value = 1)

# 0   = 1638
# 180 = 8191

# Slope (m) equation
#  x, y     x, y
# (0, 8191) (65535, 1638)
# m =  (y2 - y1)
#      ---------
#      (x2 - x1)
# m = (1638 - 8191) / (65535 - 0)
# m = -6553 / 65535

# Equation of the line
# y - y1 = m (x - x1)
# y - 8191 = (-6553 / 65535) (x - 0)
# y - 8191 = (-6553 / 65535) x
# y = ((-6553 / 65535) x) + 8191
# y = duty value
# x = potentiometer value

pot_val = None
duty = None

def pot_servo():
    global pot_val, duty
    pot_val = pot_pin.read_u16() 
    duty = int((-6553 / 65535) * pot_val) + 8191
    servo.duty_u16(duty)

if __name__ == "__main__":
    timer = Timer(-1)
    try:
        timer.init(mode = Timer.PERIODIC, period = 100, callback = lambda t:print(f"{pot_val} {duty}    ", end = "\r"))
        while True:
            pot_servo()
    except KeyboardInterrupt:
        timer.deinit()
        print("\nSee ya later, RPi Pico!")

