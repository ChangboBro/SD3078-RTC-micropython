from machine import I2C,Pin
from SD3078 import SD3078

i2c=I2C(0,sda=Pin(0),scl=Pin(1),freq=400_000)
rtc=SD3078(i2c)
rtc.enWrite()
#rtc.setdate(25,5,20,1)
rtc.settime(25,5,21,2,0,54,00,0)