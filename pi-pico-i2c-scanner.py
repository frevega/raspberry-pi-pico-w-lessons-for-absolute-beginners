from machine import Pin, SoftI2C

i2c = SoftI2C(sda=Pin(0), scl=Pin(1))

print('I2C SCANNER')
devices = i2c.scan()

if len(devices) == 0:
  print("No i2c device!")
else:
  print('I2C devices found:', len(devices))

  for device in devices:
    print("I2C hexadecimal address: ", hex(device))