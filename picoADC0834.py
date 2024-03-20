#!/usr/bin/env python3
#-----------------------------------------------------
#
#        This is a program for all ADC chip. It 
#    convert analog signal to digital signal.
#
#        This program is most analog signal modules' 
#    dependency. Use it like this:
#        `import ADC0834`
#        `sig = ADC0834.getResult(chn)`
#
#    *'chn' should be 0,1,2,3 represent for ch0, ch1, ch2, ch3
#    on ADC0834
#        
 
from machine import Pin
from utime import sleep_us

ADC_CS  = 15
ADC_CLK = 16
ADC_DIO = 17

ADC_CS_PIN = None
ADC_CLK_PIN = None
ADC_DIO_PIN = None

# using default pins for backwards compatibility
def setup(cs=15,clk=16,dio=17):
    global ADC_CS, ADC_CLK, ADC_DIO, ADC_CS_PIN, ADC_CLK_PIN, ADC_DIO_PIN
    ADC_CS=cs
    ADC_CLK=clk
    ADC_DIO=dio
    ADC_CS_PIN = Pin(ADC_CS, Pin.OUT)                 # Set pins' mode is output
    ADC_CLK_PIN = Pin(ADC_CLK, Pin.OUT)                # Set pins' mode is output

def destroy():
    print("See you later picoADC0834.py")

# using channel = 0 as default for backwards compatibility
def getResult(channel=0):                     # Get ADC result, input channel
 
    sel = int(channel > 1 & 1)
    odd = channel & 1
    # print("sel: {}, odd: {}".format(sel, odd))

    ADC_DIO_PIN = Pin(ADC_DIO, Pin.OUT) 
    ADC_CS_PIN.low()
    
    # Start bit
    ADC_CLK_PIN.low()
    ADC_DIO_PIN.high()
    sleep_us(2)
    ADC_CLK_PIN.high()
    sleep_us(2)

    # Single End mode
    ADC_CLK_PIN.low()
    ADC_DIO_PIN.high()
    sleep_us(2)
    ADC_CLK_PIN.high()
    sleep_us(2)

    # ODD
    ADC_CLK_PIN.low()
    ADC_DIO_PIN.value(odd)
    sleep_us(2)
    ADC_CLK_PIN.high()
    sleep_us(2)

    # Select
    ADC_CLK_PIN.low()
    ADC_DIO_PIN.value(sel)
    sleep_us(2)
    ADC_CLK_PIN.high()

    sleep_us(2)
    ADC_CLK_PIN.low()
    sleep_us(2)

    # ODD
    # ADC_CLK_PIN.low()
    # ADC_DIO_PIN.value(channel)
    # sleep_us(2)
    # ADC_CLK_PIN.high()
    # ADC_DIO_PIN.high()
    # sleep_us(2)
    # ADC_CLK_PIN.low()
    # ADC_DIO_PIN.high()
    # sleep_us(2)

    dat1 = 0
    for i in range(0, 8):
        ADC_CLK_PIN.high();  sleep_us(2)
        ADC_CLK_PIN.low();  sleep_us(2)
        ADC_DIO_PIN = Pin(ADC_DIO, Pin.IN) 
        dat1 = dat1 << 1 | ADC_DIO_PIN.value()  
    
    dat2 = 0
    for i in range(0, 8):
        dat2 = dat2 | ADC_DIO_PIN.value() << i
        ADC_CLK_PIN.high();  sleep_us(2)
        ADC_CLK_PIN.low();  sleep_us(2)
    
    ADC_CS_PIN.high()
    ADC_DIO_PIN = Pin(ADC_DIO, Pin.OUT)

    if dat1 == dat2:
        return dat1
    else:
        return 0

def getResult1():
    return getResult(1)


def loop():
    while True:
        for i in range(4):
            res = getResult(i)
            print ('res{} = {}'.format(i,res))
            sleep_us(0.1)
        sleep_us(1)

if __name__ == '__main__':        # Program start from here
    setup()
    try:
        loop()
    except KeyboardInterrupt:      # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()

