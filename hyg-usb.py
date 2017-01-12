#!/usr/bin/python3
import usb
import usb.core
from struct import pack
from time import sleep,asctime

LED_ON = 65
LED_OFF = 66
LED_FLASH = 67

def wr(led1 = LED_OFF, led2 = LED_OFF, led3 = LED_OFF):
    do = pack("BBBB",led1,led2,led3,66)
    dev.write(1,do)

def unp(packed,p = False):
    tem = (packed[0] << 8) + packed[1]
    hige = (packed[2] << 8) + packed[3]
    hyg = round(125.0 * tem / 65536.0 - 6.0,2) ;
    temp = round(175.72 * hige / 65536.0 - 46.85,2) ;

    if(p):
        print("Temp:", temp , "degrees C")
        print("Hyg:", hyg,"%")
    return(temp,hyg)

#Find USB device
dev = usb.core.find(idVendor=0x4d8,idProduct=0xf2c4)

if dev is None:
    raise ValueError('Cannot find device. This is a terrible shame')
    exit()
else:
    print("Device found!")

#Try to use it if found
dev.set_configuration()

while(1):
    wr(LED_FLASH)
    h = dev.read(0x81,21)
    log = unp(h,True)
    fo = open('tl.log','a')
    fo.write(asctime() + " : " + str(log[0]) + "c " + str( log[1]) + "%\n")
    fo.close
    sleep(10)
