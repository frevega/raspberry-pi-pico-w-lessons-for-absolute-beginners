from MyLib import MyColor, MyPWM
from time import sleep

class Lesson15HW:
    colorsQuantity = 0
    currentColor = None
    selectedColors = None
    
    def __init__(self, myPWMLeds: list[MyPWM], colors: dict[str: MyColor]):
        self.leds = myPWMLeds
        self.colors = colors

    def run(self):
        global currentColor, selectedColors, colorsQuantity
        self.resetColors()
        n = -1
        
        try:
            colorsQuantity = int(
                input(f"\nPress Ctrl-C to exit program at any time\nHow many colors would you like?: ")
            )
            if colorsQuantity > 0:
                n = 0
                selectedColors = []
                print(f"Valid colors: {', '.join(str(color) for color in self.colors)}")
                while n < colorsQuantity:
                    currentColor = input(f"Enter color nº {n + 1}: ").lower()
                    if currentColor in self.colors.keys():
                        selectedColors.append(currentColor)
                        n += 1
                    else:
                        print(f"Invalid color: {currentColor}")
            else:
                print("Invalid quantity: should be greater than zero")
            
            if n == colorsQuantity:
                self.showColors()
        except ValueError:
            print("Invalid input: enter only whole numbers")
            
    def showColors(self):
        print("\nCheck out your colors")
        for color in selectedColors:
            print(f"Color: {color}, value = (r: {self.colors[color].r}, g: {self.colors[color].g}, b: {self.colors[color].b})")
            self.leds[0].duty_u16(self.colors[color].r)
            self.leds[1].duty_u16(self.colors[color].g)
            self.leds[2].duty_u16(self.colors[color].b)
            sleep(1)
    
    def resetColors(self):
        [led.duty_u16(0) for led in homework.leds]
    
if __name__ == "__main__":
    try:
        homework = Lesson15HW(
            myPWMLeds = [MyPWM(n) for n in [16, 17, 18]],
            colors = {
                "red": MyColor(65535),
                "green": MyColor(g = 65535),
                "blue": MyColor(b = 65535),
                "cyan": MyColor(g = 65535, b = 65535),
                "magenta": MyColor(65535, b = 65535),
                "yellow": MyColor(65535, 25700),
                "white": MyColor(65535, 65535, 65535),
                "orange": MyColor(65535, 5000),
                "off": MyColor()
            }
        )
        while True:
            homework.run()
    except KeyboardInterrupt:
        homework.resetColors()
        print("\nSee ya later, RPi Pico!")