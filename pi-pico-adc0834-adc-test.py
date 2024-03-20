from machine import ADC, Pin
from time import sleep

if True:
    pot_pin = ADC(28)
    Pin(23, Pin.OUT, value = 1)

    while True:
        print(f"{pot_pin.read_u16()}    ", end = "\r")
        sleep(.2)
else:    
    import picoADC0834  

    picoADC0834.setup()

    while True:
        print(f"{picoADC0834.getResult()}    ", end = "\r")
        sleep(.2)
