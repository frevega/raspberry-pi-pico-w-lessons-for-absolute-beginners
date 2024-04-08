from imu import MPU6050
from machine import I2C, Pin, Timer
import network
import secrets
import socket
import time

teleplotAddr = ("192.168.100.250", 47269)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(secrets.SSID, secrets.PASSWORD)

while not station.isconnected():
    print(f"NETWORK: WAITING", end = "\r")
    time.sleep(.5)

if station.isconnected():
    print("\nNETWORK: SUCCESS")
else:
    print("\nNETWORK: FAILED")

# TELEPLOT
def sendTelemetry(name, value):
    # msg = name + ":" + str(time.time() * 1000) + ":" + value
    msg = name + ":" + value
    sock.sendto(msg.encode(), teleplotAddr)

mpu = MPU6050(I2C(0, sda = Pin(16), scl = Pin(17), freq = 400000))

display = None

def prepare_display():
    global display
    from ssd1306 import SSD1306_I2C
    display = SSD1306_I2C(96, 16, I2C(1, sda = Pin(14), scl = Pin(15), freq = 400000))
#     from sh1106 import SH1106_I2C
#     display = SH1106_I2C(128, 64, I2C(1, sda = Pin(14), scl = Pin(15), freq = 400000))#, rotate = 0)
    display.fill(0)

def write_to_oled():
    x = f"{mpu.gyro.x:.2f}  "
    y = f"{mpu.gyro.y:.2f}  "
    z = f"{mpu.gyro.z:.2f}  "
    # x = f"{mpu.accel.x:.2f}  "
    # y = f"{mpu.accel.y:.2f}  "
    # z = f"{mpu.accel.z:.2f}  "

    if display != None:
        display.fill(0)
        display.text(x, 0, 0)
        display.text(y, 49, 0)
        display.text(z, 24, 9)
        display.show()

def print_values():
    temp = f"\tTEMP: {mpu.temperature:.2f}"
    print(f"X: {mpu.accel.x:.2f} \tY: {mpu.accel.y:.2f} \tZ: {mpu.accel.z:.2f}", end = " \t")
    print(f"GX: {mpu.gyro.x:.2f} \tGY: {mpu.gyro.y:.2f} \tGZ: {mpu.gyro.z:.2f}")
    
    # TELEPLOT
    sendTelemetry("X", f"{mpu.accel.x:.2f}")
    sendTelemetry("Y", f"{mpu.accel.y:.2f}")
    sendTelemetry("Z", f"{mpu.accel.z:.2f}")
    sendTelemetry("GX", f"{mpu.gyro.x:.2f}")
    sendTelemetry("GY", f"{mpu.gyro.y:.2f}")
    sendTelemetry("GZ", f"{mpu.gyro.z:.2f}")

if __name__ == "__main__":
    timer = Timer(-1)
    timer2 = Timer(-1)
    try:
        timer2.init(mode = Timer.PERIODIC, period = 200, callback = lambda t:print_values())
        prepare_display()
        timer.init(mode = Timer.PERIODIC, period = 200, callback = lambda t:write_to_oled())
        while True:
            pass
    except KeyboardInterrupt:
        timer.deinit()
        timer2.deinit()
        if display != None:
            display.fill(0)
        print("\nSee ya later, RPi Pico!")
