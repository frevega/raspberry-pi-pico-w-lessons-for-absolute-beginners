from machine import Pin
from time import sleep
from dht import DHT11

dht11 = DHT11(Pin(16, Pin.OUT, Pin.PULL_DOWN))

try:
    while True:
        dht11.measure()
        print(f"Temperature: {dht11.temperature()}{chr(176)}C, humidity: {dht11.humidity()}%", end = "\r")
        sleep(1)
except KeyboardInterrupt:
    print("See you later RPi Pico!")