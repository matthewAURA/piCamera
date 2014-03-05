import math

number = 1234567

#convert number into bytes
#how many bytes are required?
length = int(math.ceil(math.log(number,2) / 8))

bytes = []
#get lowest 8 bits
bytes.append(number%256)
#calcuate 8 bit shorts
for i in range(1,length):
	bytes.append((number >> 8*i)%256)
	

for a in bytes:
	print chr(a)
