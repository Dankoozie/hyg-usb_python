#!/usr/bin/python3
import usb
import usb.core
from struct import pack
from time import sleep,asctime

LED_ON = 65
LED_OFF = 66
LED_FLASH = 67

def unp(packed):
    tem = (packed[0] << 8) + packed[1]
    hige = (packed[2] << 8) + packed[3]
    hyg = round(125.0 * tem / 65536.0 - 6.0,2) ;
    temp = round(175.72 * hige / 65536.0 - 46.85,2) ;
    return(temp,hyg)

class Hyg():
    def __init__(self,dev):
        self.dev = dev
        self.serial = 0
        self.red = LED_OFF
        self.green = LED_FLASH
        self.orange = LED_OFF

    def wr(self):
        do = pack("BBBB",self.green,self.red,self.orange,66)
        self.dev.write(1,do)
        
    def read_raw(self):
        self.wr()
        a = self.dev.read(0x81,21)
        return a

    def read_dec(self):
            return unp(self.read_raw())
    def read_string(self):
        r = self.read_dec()
        return "Temp: " + str(r[0]) + " degrees C" + "\nHyg: " + str(r[1]) +"%"

#Find USB device
def get_dev():
    dev = usb.core.find(idVendor=0x4d8,idProduct=0xf2c4)

    if dev is None:
        raise ValueError('Cannot find device. This is a terrible shame')
    else:
        #print("Device found!")
        #Try to use it if found
        dev.set_configuration()

    return dev

if __name__ == "__main__":
    a = Hyg(get_dev())
    a.red = LED_ON
    a.orange = LED_ON
    a.green = LED_FLASH
    while(1):
        print(a.read_string())
        sleep(10)
