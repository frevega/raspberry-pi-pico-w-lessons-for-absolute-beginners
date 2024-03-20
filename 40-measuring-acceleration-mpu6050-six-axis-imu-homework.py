from imu import MPU6050
from machine import I2C, Pin, Timer
import time

mpu = MPU6050(I2C(0, sda = Pin(16), scl = Pin(17), freq = 400000)) 

if __name__ == "__main__":
    timer = Timer(-1)
    try:
        timer.init(mode = Timer.PERIODIC, period = 100, callback = lambda t:print(f"X: {mpu.accel.x:.3f} G \tY: {mpu.accel.y:.3f} G \tZ: {mpu.accel.z:.3f} G     ", end = "\r"))
    except KeyboardInterrupt:
        timer.deinit()
        print("\nSee ya later, RPi Pico!")
    
