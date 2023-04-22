from machine import Pin, PWM, ADC, Timer
from time import sleep

class MyPWM(PWM):
    def __init__(self, pinNumber: int, freq: int = 1000, duty_u16: uint16 = 0):
        super().__init__(Pin(pinNumber))
        self.freq(freq)
        self.duty_u16(duty_u16)

pots = [ADC(n) for n in [26, 27, 28]]
leds = [MyPWM(n) for n in [16, 17, 18]]
timer = Timer(
    mode = Timer.PERIODIC,
    period = 100,
    callback = lambda t:print(
        f"r: {leds[0].duty_u16()}\tg: {leds[1].duty_u16()}\tb: {leds[2].duty_u16()}"
    )
)

def main():
    while True:
        for i, led in enumerate(leds):
            led.duty_u16(0 if pots[i].read_u16() <= 700 else pots[i].read_u16())
try:
    main()
except KeyboardInterrupt:
    timer.deinit()
    [led.duty_u16(0) for led in leds]
    print("\nSee ya later, RPi Pico!")

