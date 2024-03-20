import network
import neopixel
import secrets
import socket
from machine import Pin, I2C
from sh1106 import SH1106_I2C
from time import sleep

class MyScreen(SH1106_I2C):
    def __init__(self, sdaPin: Pin, sclPin: Pin, freq = 400000, channel = 0):
        i2c = I2C(channel, sda = sdaPin, scl = sclPin, freq = freq)
        super().__init__(128, 64, i2c, rotate = 180)
        self.sleep(False)
        self.fill(0)

    def writeText(self, text: str, x = 0, y = 0, shouldClear = True):
        if shouldClear:
            self.fill(0)
        self.text(text, x, y)
        self.show()
        
    def horizontalLine(self, x, y, w, color = True):
        self.hline(x, y, w, color)

    def fillRect(self, x, y, w, h, color = False):
        self.fill_rect(x, y, w, h, color)

class NetworkStation:
    def __init__(self, ssid, password, max_tries = 10):
        self.station = network.WLAN(network.STA_IF)
        self.station.active(True)
        self.station.connect(ssid, password)
        self.max_tries = max_tries

    def checkConnection(self, callback):
        tries = self.max_tries

        while not self.isconnected() and tries > 0:
            callback("NETWORK")
            callback(f"WAITING: {tries}", y = 12, shouldClear = False)
            tries -= 1
            sleep(.5)
        
        if self.isconnected():
            addressInfo = self.prepareSocket()
            callback(addressInfo[0])
            callback(f"PORT: {addressInfo[1]}", y = 12, shouldClear = False)
        else:
            callback("NETWORK FAILED", x = 0, y = 0)
                
    def prepareSocket(self) -> (str, int):
        address = socket.getaddrinfo(self.ifconfig()[0], 80)[0][-1]
        self.mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.mySocket.bind(address)
        self.mySocket.listen(5)
        
        return address
    
    def socket(self) -> socket:
        return self.mySocket

    def isconnected(self) -> bool:
        return self.station.isconnected()

    def ifconfig(self) -> (str, str, str, str):
        return self.station.ifconfig()

class Lesson28:
    def __init__(self, newPixelsPin = Pin(3), neoPixelsQtty = 8):
        self.screen = MyScreen(Pin(0), Pin(1))
        self.networkStation = NetworkStation(secrets.SSID, secrets.PASSWORD)
        self.networkStation.checkConnection(self.screen.writeText)
        self.led = Pin("LED", Pin.OUT)
        self.neopixels = neopixel.NeoPixel(newPixelsPin, neoPixelsQtty)
        
    def setNeoPixel(self, rgb):
        lightIntensity = 0.075
        self.neopixels.fill((int(rgb[0] * lightIntensity), int(rgb[1] * lightIntensity), int(rgb[2] * lightIntensity)))
        self.neopixels.write()

    def webPage(self, hex: str):
        isLedOn = self.led.value() == 1

        return """
        <html>
            <head>
            <title>RPi Pico Web Server</title>
            <script>
            let colorPicker;
            const defaultColor = "#%s";
            window.addEventListener("load", startup, false);
            
            function startup() {
              colorPicker = document.querySelector("#color-picker");
              colorPicker.value = defaultColor;
              colorPicker.select();
            }
            </script>
            </head>
            <body>
                <h1>RPi Pico Web Server</h1>
                <form>
                    <input type="checkbox" id="onboard" name="led" %s/>
                    <label for="onboard">Onboard led</label><br/>
                    <label for="color-picker">RGB</label>
                    <input type="color" id="color-picker" name="color-picker" value="#e66465"/><br/><br/>
                    <input type="submit" value="Submit">
                </form>
            </body>
        </html>
        """ % (hex, "checked" if isLedOn else "")
    
    def getHexRGBFrom(self, request: str) -> (str, (int, int, int)):
        index = request.find('color-picker=%23')
        if index != -1:
            start = index + len('color-picker=%23')
            hex = request[start:start + 6]
            rgb = tuple(int(hex[i : i + 2], 16) for i in (0, 2, 4))

            return (hex, rgb)
        else:
            return None

    def start(self):
        while True:
            conn, addr = self.networkStation.socket().accept()
            request = str(conn.recv(1024))
            rangeToTest = range(8, 33)
            self.led.value(request.find("led=on") in rangeToTest)
            hexRGB = self.getHexRGBFrom(request)
            if hexRGB != None:
                self.setNeoPixel(hexRGB[1])
            else:
                self.setNeoPixel((0,0,0))

            self.screen.fillRect(0, 22, 128, 42, False)
            self.screen.horizontalLine(0, 22, 128)
            self.screen.writeText(addr[0], y = 26, shouldClear = False)
            self.screen.writeText(f"PORT: {addr[1]}", y = 38, shouldClear = False)
            self.screen.horizontalLine(0, 48, 128)
            self.screen.writeText(f"LED: {'ON' if self.led.value() == 1 else 'OFF'}", y = 52, shouldClear = False)
            self.screen.writeText(hexRGB[0] if hexRGB is not None else "000000", x = 72, y = 52, shouldClear = False)

            response = self.webPage(hexRGB[0] if hexRGB is not None else "000000")
            conn.send("HTTP/1.0 200 OK\nContent-type: text/html\nConnection: close\n\n")
            conn.sendall(response)
            conn.close()

if __name__ == "__main__":
    try:
        lesson = Lesson28()
        lesson.start()
    except KeyboardInterrupt:
        print("\nSee you later RPi Pico W!")

