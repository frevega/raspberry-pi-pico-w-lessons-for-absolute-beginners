from machine import Pin, Timer
from time import sleep
from dht import DHT11

dht11 = DHT11(Pin(16, Pin.OUT, Pin.PULL_DOWN))
button = Pin(17, Pin.IN, Pin.PULL_UP)
buttonStates = [0, 1]
tempData = {"temp": None, "hum": None, "symbol": "C"}
timers = [Timer(-1), Timer(-1)]

def readButton():
    global tempData
    if tempData["temp"] != None:
        buttonStates[0] = button.value()
        if (buttonStates[0] == 1 and buttonStates[0] != buttonStates[1]):
            tempData["symbol"] = "C" if tempData["symbol"] != "C" else "F"
        buttonStates[1] = buttonStates[0]
    printTemperature()
    
def readTemperature():
    global tempData
    dht11.measure()
    tempData["temp"] = dht11.temperature()
    tempData["hum"] = dht11.humidity()
    
def printTemperature():
    if tempData["temp"] != None:
        temp = f"{tempData['temp'] if tempData['symbol'] == 'C' else (tempData['temp'] * 9/5 + 32)}"
        print(f"Temperature: {temp} {chr(176)}{tempData['symbol']}, humidity: {tempData['hum']}%   ", end = "\r")
    else:
        print("Waiting for sensor data...", end = "\r")

try:
    timers[0].init(mode = Timer.PERIODIC, period = 1000, callback = lambda t:readTemperature())
    timers[1].init(mode = Timer.PERIODIC, period = 50, callback = lambda t:readButton())
    while True:
        pass
except KeyboardInterrupt:
    [timer.deinit() for timer in timers]
    print("\nSee you later RPi Pico!")
