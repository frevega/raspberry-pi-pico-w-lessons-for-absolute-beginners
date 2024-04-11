from machine import Pin
from MyLib import MyServo
from time import sleep_ms

servo = MyServo(pin_number = 15)

if __name__ == "__main__":
    try:
        while True:
            servo.angle_from_to(180, 0)
            sleep_ms(200)
            servo.angle_from_to(0, 180)
            sleep_ms(200)
    except KeyboardInterrupt:
        print("\nSee ya later, RPi Pico!")

