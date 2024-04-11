from machine import Pin
from MyLib import MyPWM
from time import sleep

servo = MyPWM(pinNumber = 15, freq = 50)

# Slope (m) equation
#  x, y     x, y
# (0, 8191) (180, 1638)
# m =  (y2 - y1)
#      ---------
#      (x2 - x1)
# m = (1638 - 8191) / (180 - 0)
# m = -6553 / 180

# Equation of the line
# y - y1 = m (x - x1)
# y - 8191 = (-6553 / 180) (x - 0)
# y - 8191 = (-6553 / 180) x
# y = ((-6553 / 180) x) + 8191
# y = duty value
# x = potentiometer value

duty = None

def pos_servo(angle):
    global pot_val, duty
    duty = int((-6553 / 180) * angle) + 8191
    servo.duty_u16(duty)

if __name__ == "__main__":
    try:
        while True:
            for x in range(181):
                pos_servo(x)
                sleep(.005)
            for x in range(180, -1, -1):
                pos_servo(x)
                sleep(.005)
    except KeyboardInterrupt:
        print("\nSee ya later, RPi Pico!")

