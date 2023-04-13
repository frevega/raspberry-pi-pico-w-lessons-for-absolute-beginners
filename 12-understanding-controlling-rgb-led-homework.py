from machine import Pin, PWM
from time import sleep

class MyPWM(PWM):
    def __init__(self, pinNumber: int, freq: int = 1000, duty_u16: uint16 = 0):
        super().__init__(Pin(pinNumber))
        self.freq(freq)
        self.duty_u16(duty_u16)

class Color:
    def __init__(self, r: int = 0, g: int = 0, b: int = 0):
        self.r = r
        self.g = g
        self.b = b

colors = {
    "red": Color(65535),
    "green": Color(g = 65535),
    "blue": Color(b = 65535),
    "cyan": Color(g = 65535, b = 65535),
    "magenta": Color(65535, b = 65535),
    "yellow": Color(65535, 25700),
    "white": Color(65535, 65535, 65535),
    "orange": Color(65535, 5000)
}
leds = [MyPWM(n) for n in [16, 17, 18]]
validColors = ["red", "green", "blue", "cyan", "magenta", "yellow", "white", "orange"]
selectedColor = None

def colorValidation():
    for index, key in enumerate(colors.keys()):
        leds[0].duty_u16(colors[key].r)
        leds[1].duty_u16(colors[key].g)
        leds[2].duty_u16(colors[key].b)
        print(key)
        sleep(1.2)
        if index == len(colors) -1:
            [led.duty_u16(0) for led in leds]

def main():
    while True:
        try:
            selectedColor = input(f"What color would you like? {validColors}: ")
            if selectedColor in validColors:
                print(f"Color: {selectedColor}, value = (r: {colors[selectedColor].r}, g: {colors[selectedColor].g}, b: {colors[selectedColor].b})")
                leds[0].duty_u16(colors[selectedColor].r)
                leds[1].duty_u16(colors[selectedColor].g)
                leds[2].duty_u16(colors[selectedColor].b)
            else:
                print(f"Invalid color: {selectedColor}")
        except ValueError:
            print("Invalid value, please enter letters only")

try:
    main()
except KeyboardInterrupt:
    [led.duty_u16(0) for led in leds]
    print("\nSee ya later, RPi Pico!")