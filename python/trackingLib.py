import cv2
import numpy as np
import sympy as sp
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


class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def length(self):
        return math.sqrt(self.x**2 + self.y**2)

    def dotProduct(self,other):
        return self.x*other.x + self.y*other.y

    def angle(self,other):
        return math.acos(self.dotProduct(other)/(self.length()*other.length()))

    def toTuple(self):
        return (self.x,self.y)

    def __sub__(self,other):
        return Point(self.x-other.x,self.y-other.y)

    def __add__(self,other):
        return Point(self.x+other.x,self.y+other.y)
    
    def __div__(self,other):
        return Point(self.x/other,self.y/other)


class CartesianPlane:
    def __init__(self,width,height):
        self.vectors = []
        self.plane = np.zeros([height,width,3], dtype=np.uint8)
        self.width = width
        self.height = height
    
    def convertCoords(self,point):
        return (point.x+self.width/2,self.height/2-point.y)

    def drawAll(self):
        for point in self.vectors:
            cv2.line(self.plane,self.convertCoords(point.pt1),self.convertCoords(point.pt2),(255,255,255),2)
        #draw coordinate axes
        cv2.line(self.plane,self.convertCoords(Point(0,self.height)),self.convertCoords(Point(0,-self.height)),(0,255,0),1)
        cv2.line(self.plane,self.convertCoords(Point(-self.width,0)),self.convertCoords(Point(self.width,0)),(0,255,0),1)
        cv2.imshow("plane",self.plane)
        self.vectors = []
        self.plane = np.zeros([self.height,self.width,3], dtype=np.uint8)


class lineObject:
    def __init__(self,pt1,pt2):
        self.pt1 = pt1
        self.pt2 = pt2
    
    def dotProduct(self,other):
        line1 = self.pt2-self.pt1
        line2 = other.pt2-other.pt1
        return line1.dotProduct(line2)
        
    def __cmp__(self,other):
        return cmp(len(self),len(other))
    
    def length(self):
        return math.sqrt((self.pt1.x - self.pt2.x)**2 + (self.pt1.y - self.pt2.y)**2)
    
    def __len__(self):
        return int(self.length())

    def gradient(self):
        delta = self.pt2 - self.pt1
        return delta.y/delta.x

    def yAxisCut(self):
        return self.pt1.y - self.gradient()*self.pt1.x

    def intersection(self,other):
        x,y = sp.S('x y'.split())
        eq = [sp.Eq(y,self.gradient()*x+self.yAxisCut()),sp.Eq(y,other.gradient()*x+other.yAxisCut())]
        return sp.solve(eq)

    def join(self,other):
        try:
            angle = math.acos(self.dotProduct(other)/(self.length()*other.length()))
        except ValueError:
            angle = 0
        if (angle*180)/math.pi < 5:
            return lineObject((self.pt1+other.pt1)/2,(self.pt2+other.pt2)/2)
        else:
            return self


class imageProccessor:
    def __init__(self,valHSV,width,height):
        self.width = width
        self.height = height
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
        temp = np.ones(size, dtype=np.uint8)*255
        for i in range(3):
            if (self.valHSV[i] < self.valHSV[i+3]):
                temp = cv2.bitwise_and(cv2.inRange(self.frame[:,:,i],np.array(0),np.array(self.valHSV[i+3])),temp)
                temp = cv2.bitwise_and(cv2.inRange(self.frame[:,:,i],np.array(self.valHSV[i]),np.array(255)),temp)
            else:
                temp = cv2.bitwise_and(cv2.inRange(self.frame[:,:,i],np.array(self.valHSV[i+3]),np.array(self.valHSV[i])),temp)

        #Equalize A histogram for better contrast
        self.frame = temp        
        #self.frame = cv2.equalizeHist(temp)  
        
              
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
    def __init__(self,valHSV,width,height):
        imageProccessor.__init__(self,valHSV,width,height)
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
    def __init__(self,valHSV,width,height):
        imageProccessor.__init__(self,valHSV,width,height)
        self.plane = CartesianPlane(width,height)
    def findLines(self,strength):
        self.points = list()
        self.intersections = []
        #self.frame=  cv2.GaussianBlur( self.frame,(9, 9),2 )
        #Do a Canny edge detection
        self.frame = cv2.Canny(self.frame, 0, 400)
        self.lines = cv2.HoughLines(self.frame,1, math.pi/180.0, strength, np.array([]), 0, 0)
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
                #new = lineObject(Point(0,yAxisCut),Point(self.width,gradient*self.width+yAxisCut))
                new = lineObject(Point(x1,y1),Point(x2,y2))
                if (len(self.points) > 0):
                    for other in self.points:
                        try:
                            if (math.acos(new.dotProduct(other)/(new.length()*other.length())) > 20):
                                self.points.append(new)
                        except ValueError:
                            pass
                else:
                    self.points.append(new)

    def findLineSegments(self,strength):
        self.lines = []
        self.points = []
        self.frame = cv2.Canny(self.frame,0,400)
        self.lines = cv2.HoughLinesP(self.frame,1,math.pi/180,strength+1,np.array([]),20,400)
        if self.lines is not None:
            for line in self.lines[0]:
                line = lineObject(Point(line[0],line[1]),Point(line[2],line[3]))
                self.points.append(line)
                self.plane.vectors.append(line)

            #Get two longest lines
            self.points.sort()
            if (len(self.points) >= 2):
                self.points = [self.points[0].join(self.points[1])]
    def printLines(self,raw):
        if len(self.points) > 0:
            for line in self.points:
                cv2.line(raw,line.pt1.toTuple(),line.pt2.toTuple(),(0,255,0),2)

    def drawErrorLines(self,raw):
        if len(self.points) > 0:
            for line in self.points:
                #calc line midpoint
                midpoint = (line.pt1+line.pt2)/2
                cv2.circle(raw,midpoint.toTuple(),5,(255,0,0),2)
                cv2.line(raw,(self.width/2,self.height/2),(midpoint.toTuple()[0],self.height/2),(0,0,255),2)
            return Point(midpoint.x-self.width/2,self.height/2)
    
    #def printLines(self):
     #   if self.lines is not None:
      #      a,b,c = self.lines.shape
       #     print b
        #    for i in range(b):
         #       cv2.line(raw, (self.lines[0][i][0], self.lines[0][i][1]), (self.lines[0][i][2], self.lines[0][i][3]), (0, 0, 255), 3, 8)
                

                     
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
