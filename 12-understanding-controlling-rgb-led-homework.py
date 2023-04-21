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

class Lesson12HW:
    selectedColor: str = None
    
    def __init__(self, myPWMLeds: list[MyPWM], colors: dict[str: Color], validColors: list[str]):
        self.leds = myPWMLeds
        self.colors = colors
        self.validColors = validColors

    def colorCheck(self):
        for index, key in enumerate(self.colors.keys()):
            self.leds[0].duty_u16(self.colors[key].r)
            self.leds[1].duty_u16(self.colors[key].g)
            self.leds[2].duty_u16(self.colors[key].b)
            print(key)
            sleep(1.2)
            if index == len(self.colors) -1:
                [led.duty_u16(0) for led in self.leds]
                print("\ncolorCheck(): done!")

    def run(self):
        selectedColor = input(f"What color would you like? {self.validColors}: ")
        if selectedColor in self.validColors:
            print(f"Color: {selectedColor}, value = (r: {self.colors[selectedColor].r}, g: {self.colors[selectedColor].g}, b: {self.colors[selectedColor].b})")
            self.leds[0].duty_u16(self.colors[selectedColor].r)
            self.leds[1].duty_u16(self.colors[selectedColor].g)
            self.leds[2].duty_u16(self.colors[selectedColor].b)
        else:
            print(f"Invalid color: {selectedColor}")


if __name__ == "__main__":
    try:
        homework = Lesson12HW(
            myPWMLeds = [MyPWM(n) for n in [16, 17, 18]],
            colors = {
                "red": Color(65535),
                "green": Color(g = 65535),
                "blue": Color(b = 65535),
                "cyan": Color(g = 65535, b = 65535),
                "magenta": Color(65535, b = 65535),
                "yellow": Color(65535, 25700),
                "white": Color(65535, 65535, 65535),
                "orange": Color(65535, 5000)
            },
            validColors = ["red", "green", "blue", "cyan", "magenta", "yellow", "white", "orange"]
        )
        while True:
            homework.run()
    except KeyboardInterrupt:
        [led.duty_u16(0) for led in homework.leds]
        print("\nSee ya later, RPi Pico!")
