#!/usr/bin/python3
import usb
import usb.core
import sqlite3
from struct import pack
from time import sleep,asctime,time

db = sqlite3.connect('hyg-usb.db')
c = db.cursor()

c.execute("CREATE TABLE IF NOT EXISTS th (time int PRIMARY KEY,sensor_id int,temp int,humidity int)")

LED_ON = 65
LED_OFF = 66
LED_FLASH = 67

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
        #Gets raw sensor values byte array
        self.wr()
        a = self.dev.read(0x81,21)
        return a

    def read_dec(self):
        #Gets sensor values as decimal tuple
        packed = self.read_raw()
        h = round(125* ((packed[0] << 8) + packed[1]) / 65536.0 - 6.0,2)
        t = round(175.72 * ((packed[2] << 8) + packed[3]) / 65536.0 - 46.85,2)
        return(t,h)
        
    def read_string(self,store = True):
        #Gets sensor values as a text string
        r = self.read_dec()
        if(store): 
            c.execute("INSERT INTO th VALUES(?,?,?,?)",(int(time()),1,r[0],r[1]))
            db.commit()
        return "Temp: " + str(r[0]) + " degrees C" + "\nHyg: " + str(r[1]) +"%"

#Find USB device - probably doesn't work for more than 1 device
def get_dev():
    dev = usb.core.find(idVendor=0x4d8,idProduct=0xf2c4)

    if dev is None:
        raise ValueError('Cannot find device. This is a terrible shame')
    else:
        #Try to use it if found
        dev.set_configuration()

    return dev

if __name__ == "__main__":
    a = Hyg(get_dev())
    while(1):
        print(a.read_string())
        sleep(30)

