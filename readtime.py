from machine import I2C,Pin
import time
from SD3078 import SD3078

i2c=I2C(0,sda=Pin(0),scl=Pin(1),freq=400_000)
rtc=SD3078(i2c)
weeklist=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
led=Pin(25,Pin.OUT)
led.value(1)

def Sync():
    lasttime=rtc.readtime()
    sec=lasttime[4]
    while(sec==lasttime[4]):
        sec=lasttime[4]
        lasttime=rtc.readtime()
        time.sleep_ms(50)

Sync()
while(True):
    nowtime=rtc.readtime()
    #nowdate=rtc.readdate()
    print("20%02d/%02d/%02d"%(nowtime[5],nowtime[6],nowtime[7]),end=", ")
    print(weeklist[nowtime[8]])
    if nowtime[0]:
        print("%02d:%02d:%02d"%(nowtime[2],nowtime[3],nowtime[4]))
    else:
        if nowtime[1]:
            print("pm %02d:%02d:%02d"%(nowtime[2],nowtime[3],nowtime[4]))
        else:
            print("am %02d:%02d:%02d"%(nowtime[2],nowtime[3],nowtime[4]))
    print("battery volt=%.2fV"%(rtc.readBattVolt()))
    print("temperature=%d ℃"%(rtc.readTemp()))
    print()
    time.sleep(1)
    led.toggle()
