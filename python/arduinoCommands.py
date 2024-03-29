import serial
import struct
import math



class ArduinoController:
    def __init__(self):
        self.ser = serial.Serial("/dev/ttyACM0",9600,timeout=3)			

    def splitInt(self,integer):
        #convert number into bytes
        #how many bytes are required?
        length = int(math.ceil(math.log(integer,2) / 8))
        bytes = []
        #get lowest 8 bits
        bytes.append(integer%256)
        #calcuate 8 bit shorts
        for i in range(1,length):
	        bytes.append((integer >> 8*i)%256)
        return bytes

    def sendInt(self,integer):
        shorts = self.splitInt(integer)
        self.ser.write('i')
        self.ser.write(chr(len(shorts)))
        for i in shorts:
            self.ser.write(chr(i))
