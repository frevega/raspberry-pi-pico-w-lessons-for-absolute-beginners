# Servo
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

from machine import ADC, I2C, Pin, PWM, RTC, Timer
from sh1106 import SH1106_I2C
from writer import Writer
import minecraftia
import time
import _thread

screen = SH1106_I2C(128, 64, I2C(0, sda = Pin(0), scl = Pin(1), freq = 400000))
screen.fill(0)

servo = PWM(Pin(18))
servo.freq(50)

pot_pin = ADC(28)

temp_sensor = ADC(4)

Pin(23, Pin.OUT, value = 1)

pot_val = 0
duty = 0
rtc = RTC()


led = Pin("LED", Pin.OUT, value = 0)
led_button = Pin(22, Pin.IN, Pin.PULL_UP)
led_button_states = [0, 1]

def pot_servo():
    global pot_val, duty
    pot_val = pot_pin.read_u16() 
    duty = int((-6553 / 65535) * pot_val) + 8191
    servo.duty_u16(duty)

def write_screen(message, x, y, clr_h):
    global screen
    try:
        screen.fill_rect(x, y, 128, clr_h, False)
        time.sleep_us(1)
        screen.text(message, x, y)
        time.sleep_us(1)
        screen.show()
    except Exception as e:
        print('--- Caught Exception ---')
        import sys
        sys.print_exception(e)
        print('----------------------------')

def simple_task():
    while True:
        read_temp()
        time.sleep(2.5)
        
def read_temp():
    adc_value = temp_sensor.read_u16()
    temperature = 27 - (adc_value * (3.3/65535) - 0.706) / 0.001721
    text = f"TEMP: {round(temperature, 2)}" if temperature >= 0 else "TEMP: WAITING"
    write_screen(text, 0, 20, 10)
    

def write_pot_duty():
    write_screen(f"POT : {pot_val}", 0, 0, 10)
    write_screen(f"DUTY: {duty}", 0, 10, 10)
    
def datetime():
    time = rtc.datetime()
    write_screen(f"DATE: {time[2]}/{time[1]}/{time[0]}", 0, 30, 10)
    write_screen(f"TIME: {time[4]:02d}:{time[5]:02d}:{time[6]:02d}", 0, 40, 10)

def read_onboard_led_button():
    led_button_states[0] = led_button.value()
    if (led_button_states[0] == 1 and led_button_states[0] != led_button_states[1]):
        led.toggle()
    led_button_states[1] = led_button_states[0]
    

if __name__ == "__main__":
    timers = [Timer(-1), Timer(-1), Timer(-1)]
    temperature_thread = None
    try:
#         timers[0].init(mode = Timer.PERIODIC, period = 52, callback = lambda t:read_onboard_led_button())
#         timers[1].init(mode = Timer.PERIODIC, period = 151, callback = lambda t:write_pot_duty())
#         timers[2].init(mode = Timer.PERIODIC, period = 1000, callback = lambda t:datetime())
        temperature_thread = _thread.start_new_thread(simple_task, ())
        
        
        read_onboard_led_button_deadline = time.ticks_add(time.ticks_ms(), 50)
        pot_duty_deadline = time.ticks_add(time.ticks_ms(), 150)
        datetime_deadline = time.ticks_add(time.ticks_ms(), 1000)
        
        
        while True:
            pot_servo()
            
            current_onboard_led_button_millis = time.ticks_ms()
            if time.ticks_diff(read_onboard_led_button_deadline, current_onboard_led_button_millis) < 0:
                read_onboard_led_button_deadline = time.ticks_add(current_onboard_led_button_millis, 50)
                read_onboard_led_button()
            
            current_pot_duty_millis = time.ticks_ms()
            if time.ticks_diff(pot_duty_deadline, current_pot_duty_millis) < 0:
                pot_duty_deadline = time.ticks_add(current_pot_duty_millis, 150)
                write_pot_duty()
            
            current_datetime_milllis = time.ticks_ms()
            if time.ticks_diff(datetime_deadline, current_datetime_milllis) < 0:
                datetime_deadline = time.ticks_add(current_datetime_milllis, 1000)
                datetime()
                
    except KeyboardInterrupt:
        [timer.deinit() for timer in timers]
        screen.fill(0)
        print("\nSee ya later, RPi Pico!")



