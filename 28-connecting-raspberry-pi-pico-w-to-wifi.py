import socket
from machine import Pin, Timer
from time import sleep
import network
import secrets

timer = Timer(-1)

led = Pin("LED", Pin.OUT)

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(secrets.SSID, secrets.PASSWORD)

while not wifi.isconnected():
    print("Waiting for connection...")
    sleep(1)
    
print("Connected")

wifiInfo = wifi.ifconfig()
print(wifiInfo)
serverIP = wifiInfo[0]
serverPort = 2222
bufferSize = 1024

udpServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udpServer.bind((serverIP, serverPort))

while True:
    message, address = udpServer.recvfrom(bufferSize)
    messageDecoded = message.decode("utf-8")
    print(address[0], messageDecoded)
    dataString = "Cmd received: " + messageDecoded
    dataStringEncoded = dataString.encode("utf-8")
    udpServer.sendto(dataStringEncoded, address)
    
    if messageDecoded == "ON":
        timer.init(mode = Timer.PERIODIC, period = 250, callback = lambda t:led.toggle())
    elif messageDecoded == "OFF":
        timer.deinit()
        led.off()
