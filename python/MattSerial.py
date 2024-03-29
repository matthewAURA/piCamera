import serial
import struct
import math



class SerialController:
    def __init__(self,serialPort,baud):
        self.ser = serial.Serial(serialPort,baud,timeout=3)			
        self.notifier = 'i'

    def setNotifier(self,notifier):
        self.notifier = notifier

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
        self.ser.write(self.notifier)
        self.ser.write(chr(len(shorts)))
        for i in shorts:
            self.ser.write(chr(i))

