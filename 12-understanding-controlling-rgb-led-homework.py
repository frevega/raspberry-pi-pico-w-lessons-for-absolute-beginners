from time import sleep
from MyLib import MyColor, MyPWM

class Lesson12HW:
    selectedColor: str = None
    
    def __init__(self, myPWMLeds: list[MyPWM], colors: dict[str: MyColor], validColors: list[str]):
        self.leds = myPWMLeds
        self.colors = colors
        self.validColors = validColors

    def colorCheck(self):
        for index, key in enumerate(self.colors.keys()):
            self.leds[0].duty_u16(self.colors[key].r)
            self.leds[1].duty_u16(self.colors[key].g)
            self.leds[2].duty_u16(self.colors[key].b)
            print(key)
            sleep(2)
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
                "red": MyColor(65535),
                "green": MyColor(g = 65535),
                "blue": MyColor(b = 65535),
                "cyan": MyColor(g = 65535, b = 65535),
                "magenta": MyColor(65535, b = 65535),
                "yellow": MyColor(65535, 25700),
                "white": MyColor(65535, 65535, 65535),
                "orange": MyColor(65535, 5000)
            },
            validColors = ["red", "green", "blue", "cyan", "magenta", "yellow", "white", "orange"]
        )
        while True:
            homework.run()
    except KeyboardInterrupt:
        [led.duty_u16(0) for led in homework.leds]
        print("\nSee ya later, RPi Pico!")
