from lcd1602 import LCD
from time import sleep

lcd = LCD()

def greeting(name):
    if name != "":
        for n in range(5, 0, -1):
            lcd.write(0, 0, f"Show name {n} secs")
            lcd.write(0, 1, name)
            sleep(1)
        lcd.clear()
    
try:
    while True:
        lcd.write(0, 0, "Enter your name")
        greeting(input(""))
except KeyboardInterrupt:
    lcd.clear()