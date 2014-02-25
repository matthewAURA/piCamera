import cv2
import numpy as np
import random
import time
import math
import os

class blobObject:
    def __init__(self,centre,radius):
        self.centre = centre
        self.radius = radius
        
        
    def __cmp__(self,other):
        return cmp(self.radius,other.radius)
class lineObject:
    def __init__(self,pt1,pt2):
        self.pt1 = pt1
        self.pt2 = pt2 
        
    def __cmp__(self,other):
        return cmp(len(self),len(other))
        
    def __len__(self):
        return int(math.sqrt((self.pt1[0] - self.pt2[0])**2 + (self.pt1[1] - self.pt2[1])**2))   
         
class imageProccessor:
    def __init__(self,valHSV):        
        self.valHSV = valHSV
        
        
    def configWebcam(self,mode):
        if mode is "line":
            os.system('uvcdynctrl -s Brightness 100')
            os.system('uvcdynctrl -s Contrast 255')
            os.system('uvcdynctrl -s Saturation 21')
            os.system('uvcdynctrl -s "Exposure (Absolute)" 166')
            os.system('uvcdynctrl -s "Exposure, Auto Priority" 0')
            os.system('uvcdynctrl -s "Exposure, Auto" 0')      
            os.system('uvcdynctrl -s "White Balance Temperature, Auto" 0')
        elif mode is "object":
            os.system('uvcdynctrl -s Brightness 150')
            os.system('uvcdynctrl -s Contrast 37')
            os.system('uvcdynctrl -s Saturation 190')
            os.system('uvcdynctrl -s "Exposure (Absolute)" 166')
            os.system('uvcdynctrl -s "Exposure, Auto Priority" 0')
            os.system('uvcdynctrl -s "Exposure, Auto" 0')      
            os.system('uvcdynctrl -s "White Balance Temperature, Auto" o')             
        else:
            assert("Camera mode not regcognized: " + str(mode))
            
    def getHSV(self):
        #Convert to HSV space for better filtering
        self.frame = cv2.cvtColor(self.frame,cv2.cv.CV_BGR2HSV)
        #check for inverted ranges
        size = self.frame.shape[0], self.frame.shape[1]
        temp = np.ones(size, dtype=np.uint8)
        for i in range(3):
            if (self.valHSV[i] < self.valHSV[i+3]):
                temp = cv2.bitwise_and(cv2.inRange(self.frame[:,:,i],np.array(0),np.array(self.valHSV[i+3])),temp)
                temp = cv2.bitwise_and(cv2.inRange(self.frame[:,:,i],np.array(self.valHSV[i]),np.array(255)),temp)
            else:
                temp = cv2.bitwise_and(cv2.inRange(self.frame[:,:,i],np.array(self.valHSV[i+3]),np.array(self.valHSV[i]))[:,:,0],temp)
        

        #Equalize A histogram for better contrast
        self.frame = cv2.equalizeHist(temp)  
        
              
    def fillHoles(self):                
        #create erode and dilate kernels 
        erodeKernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
        dilateKernel = cv2.getStructuringElement(cv2.MORPH_RECT,(15,15))
        #Perform Erode and dilate to fill holes in image
        self.frame = cv2.erode(self.frame,erodeKernel)
        self.frame = cv2.dilate(self.frame, dilateKernel)   
        
    def getGray(self):
        self.frame = cv2.cvtColor(self.frame,cv2.cv.CV_BGR2GRAY) 
        
        
        
class ballFinder(imageProccessor):
    def __init__(self,valHSV):
        imageProccessor.__init__(self,valHSV)
        self.minObjectSize = 3
        
    def findObjects(self):
        maxSize = 0
        # Find contours  
        contours = cv2.findContours(self.frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
        self.objects = list()
        #remove contours that are too small
        if (len(contours) > 0):
                for contour in contours:
                        #contours[i] = cv2.approxPolyDP(contours[i],3,True)
                        #rectangle = cv.MinAreaRect2(contours,storage)
                        rect = cv2.minAreaRect(contour)
                        box = cv2.cv.BoxPoints(rect)
                        box = np.int0(box)
                        (x,y),radius = cv2.minEnclosingCircle(contour)
                        blob = blobObject((int(x),int(y)),int(radius))
                        if (radius > self.minObjectSize):				
                                self.objects.append(blob)
                                
    def getBiggestObject(self):
        if len(self.objects) > 0:
            return max(self.objects)
        else:
            return None
    def printBiggestObject(self,raw):
        blob = self.getBiggestObject()
        if blob is not None:
            cv2.circle(raw,blob.centre,blob.radius,(0.0,255.0,0.0),3,5,0)
            
            
class lineFinder(imageProccessor): 
    def __init__(self,valHSV):
        imageProccessor.__init__(self,valHSV)
        
    def findLines(self):
        self.points = list()
        #self.frame=  cv2.GaussianBlur( self.frame,(9, 9),2 )
        #Do a Canny edge detection
        self.frame = cv2.Canny(self.frame, 0, 400)
        self.lines = cv2.HoughLines(self.frame,1, math.pi/180.0, 120, np.array([]), 0, 0)
        if self.lines is not None:
           for rho,theta in self.lines[0]:
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a*rho
                y0 = b*rho
                x1 = int(x0 + 1000*(-b)) 
                y1 = int(y0 + 1000*(a)) 
                x2 = int(x0 - 1000*(-b)) 
                y2 = int(y0 - 1000*(a))
                new = lineObject((x1,y1),(x2,y2))
                self.points.append(new)
                
    def printLines(self,raw):
        if len(self.points) > 0:
            for line in self.points:
                cv2.line(raw,line.pt1,line.pt2,(0,255,0),2)
                
    
    
    #def printLines(self):
     #   if self.lines is not None:
      #      a,b,c = self.lines.shape
       #     print b
        #    for i in range(b):
         #       cv2.line(raw, (self.lines[0][i][0], self.lines[0][i][1]), (self.lines[0][i][2], self.lines[0][i][3]), (0, 0, 255), 3, 8)
                
                

    def calculateBestGradient(self):
        gradients = []
        if len(self.points) > 0:
            for line in self.points:
                deltaX = line.pt1[0]-line.pt2[0]
                deltaY = line.pt1[1]-line.pt2[1]
                if deltaX is not 0:
                    gradients.append(float(deltaY)/float(deltaX))
            if len(gradients) > 0:
                print (180*(math.atan(max(gradients)))/math.pi)   
                     
class SerialHandler:  
    def __init__(self):
        self.ser = serial.Serial("/dev/ttyACM0",9600)
        if (not self.ser.isOpen()):
            assert( "Serial Communication Failed!")
    def sendInt(self,inputNum):
	    msb = inputNum
	    lsb = inputNum << 8
	    self.ser.write(str(msb)) #Send first 8 bits
	    self.ser.write(str(lsb)) #Send Last 8 bits
