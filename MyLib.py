from machine import Pin, PWM

class MyPWM(PWM):
    """
        A class for easy PWM pin in one line instantiation
    """
    def __init__(self, pinNumber: int, freq: int = 1000, duty_u16: int = 0):
        super().__init__(Pin(pinNumber))
        self.freq(freq)
        self.duty_u16(duty_u16)

class MyColor:
    """
        A class for RGB color handling
    """
    def __init__(self, r: int = 0, g: int = 0, b: int = 0):
        self.r = r
        self.g = g
        self.b = b
