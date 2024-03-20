import json
import minecraftia
import network
import secrets
import socket
import urequests
from machine import I2C, Pin, Timer
from sh1106 import SH1106_I2C
from writer import Writer

class MyScreen(SH1106_I2C):
    def __init__(self, sdaPin: Pin, sclPin: Pin, freq = 400000, channel = 0):
        super().__init__(128, 64, I2C(channel, sda = sdaPin, scl = sclPin, freq = freq))#, rotate = 0)
        self.sleep(False)
        self.fill(0)
        self.writer = Writer(self, minecraftia, False)
        Writer.set_textpos(self, 0, 0)

    def writeText(self, text: str, x = 0, y = 0, clear = False, update = False):
        if clear:
            self.fill(0)
        Writer.set_textpos(self, y, x)
        self.writer.printstring(text + "\n")
        if update:
            self.show()

class NetworkStation(network.WLAN):
    def __init__(self, ssid, password, max_tries = 75):
        super().__init__(network.STA_IF)
        self.active(True)
        # Try to get an IP address
        self.connect(ssid, password)
        self.max_tries = max_tries

    def checkConnection(self, callback):
        tries = self.max_tries

        while not self.isconnected() and tries > 0:
            callback(f"Waiting for network{''.join(['.' for num in range(1, int(tries / 4))])}", clear = True, update = True)
            tries -= 1

        if self.isconnected():
            # Prepare socket and bind it to current IP address
            self.address_info = self.__prepareSocket()
        else:
            callback("Network failed", x = 29, y = 20, clear = True, update = True)
                
    def __prepareSocket(self) -> list[int]:
        address = socket.getaddrinfo(self.ifconfig()[0], 80)[0][-1]
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(address)
        self.socket.listen(5)

        return address

class CMCApiClient:
    def __init__(self, debug = False):
        self.screen = MyScreen(Pin(0), Pin(1))
        self.invertColorsScreenTimer = Timer(-1)
        self.invertScreenState = 0
        self.invertScreenCounter = 0
        
        # Flip screen button
        self.flipButton = Pin(22, Pin.IN, Pin.PULL_UP)
        self.flipButtonStates = [0, 1]
        
        # Update change column button
        self.changeColumnButton = Pin(17, Pin.IN, Pin.PULL_UP)
        self.changeColumnButtonStates = [0, 1]
        
        # Change collumn titles & values
        self.percent_changes = ["1h","24h","7d","30d","60d","90d"]
        self.selected_percent_change_index = 0
        
        # Server response json is empty at this point
        self.server_response = json.loads("{}")
        
        # Flag for configuration web page
        self.parameters = [
            ("BTC", "checked"),
            ("ETH", "checked"),
            ("USDT", "checked"),
            ("BNB", "checked")
        ]
        
        # Program timers
        self.timers = [Timer(-1), Timer(-1)]
        
        # Debugging flag
        self.debug = debug
    
    def prepreCMCURL(self):
        symbols = ",".join([b for b, a in self.parameters if a != ""])
        self.url = f"https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest?aux=cmc_rank&symbol={symbols}"
        self.headers = {
            "Accepts": "application/json",
            "X-CMC_PRO_API_KEY": secrets.CMC_KEY
        }

    def invertScreenColors(self):
        if self.invertScreenCounter < 10:
            self.invertScreenCounter += 1
            self.invertScreenState ^= 1
            self.screen.invert(self.invertScreenState)
        else:
            self.invertScreenCounter = 0
            self.invertColorsScreenTimer.deinit()

    def startNetwork(self):
        self.networkStation = NetworkStation(secrets.SSID, secrets.PASSWORD)
        self.networkStation.checkConnection(self.screen.writeText)

    def readFlipButton(self):
        self.flipButtonStates[0] = self.flipButton.value()
        if (self.flipButtonStates[0] == 1 and self.flipButtonStates[0] != self.flipButtonStates[1]):
            self.screen.flip()
        self.flipButtonStates[1] = self.flipButtonStates[0]

    def updateChangeColumnButton(self):
        self.changeColumnButtonStates[0] = self.changeColumnButton.value()
        if (self.changeColumnButtonStates[0] == 1 and self.changeColumnButtonStates[0] != self.changeColumnButtonStates[1]):
            self.selected_percent_change_index = 0 if self.selected_percent_change_index > 4 else self.selected_percent_change_index + 1
            self.displayCMCData(pull_from_server = False)
        self.changeColumnButtonStates[1] = self.changeColumnButtonStates[0]

    def displayCMCData(self, pull_from_server = True, invert_colors = False):
        self.prepreCMCURL()

        if pull_from_server:
            if self.debug:
                from cmc_dummy_data import response
                self.server_response = response
            else:
                self.server_response = urequests.request("GET", self.url, headers = self.headers).json()

        if self.server_response["status"]["error_code"] == 0:
            text_y_pos = 10
            price_title_x_pos = 128
            change_title_x_pos = 128
            
            self.screen.fill(0)
            items = [b for b, a in self.parameters if a != ""]
            for symbol in items:
                data = self.server_response["data"][symbol][0]
                percent_change_json_key = f"percent_change_{self.percent_changes[self.selected_percent_change_index]}"
                change = f'{data["quote"]["USD"][percent_change_json_key]:.2f}'
                price = f'{data["quote"]["USD"]["price"]:.2f}'
                # Change value & title position
                change_x_pos = 32 + (32 - self.screen.writer.stringlen(change))
                change_title_x_pos = change_title_x_pos if change_title_x_pos <= change_x_pos else change_x_pos
                # Price value & title position
                price_x_pos = 73 + (56 - self.screen.writer.stringlen(price))
                price_title_x_pos = price_title_x_pos if price_title_x_pos <= price_x_pos else price_x_pos

                self.screen.writeText(data["symbol"], y = text_y_pos)
                self.screen.writeText(change, x = change_x_pos, y = text_y_pos)
                self.screen.writeText(price, x = price_x_pos, y = text_y_pos)
                # Vertical position
                text_y_pos += 9

            self.screen.hline(0, 9, 128, True)
            self.screen.writeText("SYMB")
            self.screen.writeText(f"% {self.percent_changes[self.selected_percent_change_index]}", x = change_title_x_pos)
            price_column_overflow = 128 - (price_title_x_pos + self.screen.writer.stringlen("PRICE"))
            self.screen.writeText("PRICE", x = price_title_x_pos if price_column_overflow >= 0 else (price_column_overflow + price_title_x_pos))
            address_info = f"{self.networkStation.address_info[0]}:{self.networkStation.address_info[1]}"
            self.screen.writeText(address_info, x = (128 - self.screen.writer.stringlen(address_info)), y = 47, update = True)
        else:
            self.screen.writeText(f'Error: {self.server_response["status"]["error_code"]}')

        if invert_colors:
            self.invertColorsScreenTimer.init(mode = Timer.PERIODIC, period = 50, callback = lambda t:self.invertScreenColors())


    def webPage(self) -> str:
        return f'''
        <html>
            <head>
            <title>RPi Pico CoinMarketCap Display configuration</title>
            </head>
            <body>
                <h1>RPi Pico Web Server</h1>
                <form>
                    <input type="checkbox" id="btc" name="btc" {self.parameters[0][1]}/>
                    <label for="btc">BTC</label><br/>
                    <input type="checkbox" id="eth" name="eth" {self.parameters[1][1]}/>
                    <label for="eth">ETH</label><br/>
                    <input type="checkbox" id="usdt" name="usdt" {self.parameters[2][1]}/>
                    <label for="usdt">USDT</label><br/> 
                    <input type="checkbox" id="bnb" name="bnb" {self.parameters[3][1]}/>
                    <label for="bnb">BNB</label><br/><br/>
                    <input type="submit" value="Submit">
                </form>
            </body>
        </html>
        '''

    def web_server(self):
        while True:
            conn, addr = self.networkStation.socket.accept()
            incoming_request = str(conn.recv(1024))

            try:
                request = incoming_request.split()[1].replace("/", "").replace("?", "")
                if len(request) > 0:
                    self.parameters = [
                        ("BTC", "checked" if request.find("btc=on") != -1 else ""),
                        ("ETH", "checked" if request.find("eth=on") != -1 else ""),
                        ("USDT", "checked" if request.find("usdt=on") != -1 else ""),
                        ("BNB", "checked" if request.find("bnb=on") != -1 else "")
                    ]
                    self.displayCMCData()
                    self.timers[1].deinit()
                    self.timers[1].init(mode = Timer.PERIODIC, period = 60000, callback = lambda t:program.displayCMCData(invert_colors = True))
            except IndexError:
                pass

            web_page = self.webPage()
            conn.send("HTTP/1.0 200 OK\nContent-type: text/html\nConnection: close\n\n")
            conn.sendall(web_page)
            conn.close()

if __name__ == "__main__":
    flipScreenTimer = Timer(-1)
    try:
        program = CMCApiClient(debug = False)
        flipScreenTimer.init(mode = Timer.PERIODIC, period = 50, callback = lambda t:program.readFlipButton())
        program.startNetwork()
        if  program.networkStation.isconnected():   
            program.screen.writeText("Getting CMC data", x = 25, y = 20, clear = True, update = True)
            program.displayCMCData()
            program.timers[0].init(mode = Timer.PERIODIC, period = 50, callback = lambda t:program.updateChangeColumnButton())
            program.timers[1].init(mode = Timer.PERIODIC, period = 60000, callback = lambda t:program.displayCMCData(invert_colors = True))
            program.web_server()
    except KeyboardInterrupt:
        flipScreenTimer.deinit()
        [timer.deinit() for timer in program.timers]
        program.screen.fill(0)
        print("\nSee you later RPi Pico W!")
