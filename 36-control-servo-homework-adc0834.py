import picoADC0834   
from machine import ADC, Pin, PWM, Timer

servo = PWM(Pin(14))
servo.freq(50)

# 0   = 1638
# 180 = 8191

# Slope (m) equation
#  x, y     x, y
# (0, 8191) (255, 1638)
# m =  (y2 - y1)
#      ---------
#      (x2 - x1)
# m = (1638 - 8191) / (255 - 0)
# m = -6553 / 255

# Equation of the line
# y - y1 = m (x - x1)
# y - 8191 = (-6553 / 255) (x - 0)
# y - 8191 = (-6553 / 255) x
# y = ((-6553 / 255) x) + 8191
# y = duty value
# x = potentiometer value

pot_val = None
duty = None

def pot_servo():
    global pot_val, duty
    pot_val = picoADC0834.getResult()
    duty = int((-6553 / 255) * pot_val) + 8191
    servo.duty_u16(duty)

if __name__ == "__main__":
    picoADC0834.setup()
    timer = Timer(-1)
    try:
        timer.init(mode = Timer.PERIODIC, period = 250, callback = lambda t:print(f"{pot_val} {duty}    ", end = "\r"))
        while True:
            pot_servo()
    except KeyboardInterrupt:
        timer.deinit()
        print("\nSee ya later, RPi Pico!", picoADC0834.destroy())

