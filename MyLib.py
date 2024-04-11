from machine import Pin, PWM
from time import sleep_ms

class MyPWM(PWM):
    """
        A class for easy PWM pin in one line instantiation
    """
    def __init__(self, pinNumber: int, freq: int = 1000, duty_u16: int = 0):
        super().__init__(Pin(pinNumber))
        self.freq(freq)
        self.duty_u16(duty_u16)

class MyServo(MyPWM):
    """
        A class for easy Servo instantiation

        Slope (m) equation
         x, y     x, y
        (0, 7800) (180, 1400)
        m =  (y2 - y1)
             ---------
             (x2 - x1)
        m = (1400 - 7800) / (180 - 0)
        m = -6400 / 180

        Equation of the line
        y - y1 = m (x - x1)
        y - 7800 = (-6400 / 180) (x - 0)
        y - 7800 = (-6400 / 180) x
        y = ((-6400 / 180) * x) + 7800
        y = duty value
        x = angle value
    """
    def __init__(self, pin_number: int, freq: int = 50, duty_u16: int = 0):
        super().__init__(pinNumber = pin_number, freq = freq)
    
    def angle(self, angle: int):
        duty = int((-6400 / 180) * angle) + 7800
        self.duty_u16(duty)
    
    def angle_from_to(self, start_angle: int, end_angle: int, sleep_ms_time: int = 10):
        if start_angle < end_angle:
            start = start_angle + 1
            stop = end_angle
            step = 1
        else:
            start = start_angle
            stop = end_angle - 1
            step = -1

        for angle in range(start, stop, step):
            self.angle(angle)
            sleep_ms(sleep_ms_time)

class MyColor:
    """
        A class for RGB color handling
    """
    def __init__(self, r: int = 0, g: int = 0, b: int = 0):
        self.r = r
        self.g = g
        self.b = b
