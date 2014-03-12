import serial
import time

ser = serial.Serial('/dev/ttyAMA0',4800,timeout=3)
time.sleep(3)
if (not ser.isOpen()):
	print "Cannot open Serial!"
else:	
	ser.write('H')
	while(True):
                char = ser.read()
                if char is 'a':
                        ser.write('H')	
		 		
		#msb =  bytearray(ser.read(1))
		#lsb = bytearray(ser.read(1))
		#print (msb[0]*256+lsb[0])/10
		time.sleep(0.05)
