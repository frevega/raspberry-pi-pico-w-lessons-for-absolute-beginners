from machine import ADC, Pin, PWM, Timer
import utime
import _thread


servo = PWM(Pin(15))
servo.freq(50)
pot_pin = ADC(28)
temp_sensor = ADC(4)
Pin(23, Pin.OUT, value = 1)

# 0   = 1638
# 180 = 8191

# Slope (m) equation
#  x, y     x, y
# (0, 8191) (65535, 1638)
# m =  (y2 - y1)
#      ---------
#      (x2 - x1)
# m = (1638 - 8191) / (65535 - 0)
# m = -6553 / 65535

# Equation of the line
# y - y1 = m (x - x1)
# y - 8191 = (-6553 / 65535) (x - 0)
# y - 8191 = (-6553 / 65535) x
# y = ((-6553 / 65535) x) + 8191
# y = duty value
# x = potentiometer value

pot_val = None
duty = None

# spLock = _thread.allocate_lock() # creating semaphore lock

def pot_servo():
    global pot_val, duty
    pot_val = pot_pin.read_u16() 
    duty = int((-6553 / 65535) * pot_val) + 8191
    servo.duty_u16(duty)


def read_temp_task():
    while True:
#         spLock.acquire() # acquiring semaphore lock
        
        adc_value = temp_sensor.read_u16()
        volt = (3.3/65535) * adc_value
        temperature = 27 - (volt - 0.706)/0.001721
        print("Temp", round(temperature, 2))
        utime.sleep(5) # 0.5 sec or 500us delay
        
#         spLock.release()



if __name__ == "__main__":
    timer = Timer(-1)
    temp_thread = None
    try:
        timer.init(mode = Timer.PERIODIC, period = 75, callback = lambda t:print(f"{pot_val} {duty}    ", end = "\r"))
        temp_thread = _thread.start_new_thread(read_temp_task, ())
        while True:
            pot_servo()
    except KeyboardInterrupt:
        timer.deinit()
        print("\nSee ya later, RPi Pico!")


