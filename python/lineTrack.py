import cv2
import numpy as np
import random
import time
import serial
import trackingLib


def on_change(var):
    return


def getHSV(gui):
    valHSV = [0,0,0,0,0,0]
    if gui:
        valHSV[0] = cv2.getTrackbarPos("Hue","Raw")
        valHSV[3] = cv2.getTrackbarPos("Hue Min","Raw")
        valHSV[1] = cv2.getTrackbarPos("Saturation","Raw")
        valHSV[4] = cv2.getTrackbarPos("Sat Min","Raw")
        valHSV[2] = cv2.getTrackbarPos("Value","Raw")
        valHSV[5] = cv2.getTrackbarPos("Value Min","Raw") 
    else:
        #Values for blue:
        #valHSV = [142,229,243,104,100,120]
        #values for white
        valHSV = [250, 26, 194, 0, 0, 164]        
    return valHSV


#Dimentions of Capture window
scale = 4
width = 640/scale
height = 480/scale

#Open capture device
device = 0 # assume we want first device

gui = False
record = True

#create video capture device, set capture area
capture = cv2.VideoCapture(device)
capture.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,width)
capture.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,height)

#create recording object
if record:
    recorder = cv2.VideoWriter("test.avi", cv2.cv.CV_FOURCC('D','I','V','X'), 30,(width,height))
    if not recorder.isOpened():
        assert("VideoWriter could not be opened")

valHSV = getHSV(False)


if gui:
    cv2.nameWindow("Raw")
    cv2.createTrackbar("Hue","Raw",valHSV[0],255,on_change);
    cv2.createTrackbar("Saturation","Raw",valHSV[1],255,on_change); 
    cv2.createTrackbar("Value","Raw",valHSV[2],255,on_change);
    cv2.createTrackbar("Hue Min","Raw",valHSV[3],255,on_change);
    cv2.createTrackbar("Sat Min","Raw",valHSV[4],255,on_change);     
    cv2.createTrackbar("Value Min","Raw",valHSV[5],255,on_change);



#create image processing objects
imgproc = trackingLib.lineFinder(valHSV)
imgproc.configWebcam("line")
if(capture):  # check if we succeeded
    
        #main loop
        while(True):
                time1 = time.time()
                #Pull a frame from the camera to the raw image
                # capture the current frame
                raw = capture.read()[1]
                
                if raw is None:
                        break
                imgproc.frame = raw
                #imgproc.valHSV = getHSV(gui)
                imgproc.getGray()
                #imgproc.fillHoles()
                #imgproc.findObjects()
                #imgproc.printBiggestObject(raw)
                #imgproc.findLines()
                #imgproc.printLines(raw)
                time2 = time.time()
				#print (1/(time2-time1))
                size =  imgproc.calculateBestGradient()
                if size is not None:
                    print size
                if gui: 
					cv2.imshow("Raw",raw)
                
                if record:
                    recorder.write(imgproc.frame)
                if(cv2.waitKey(30) >= 0) :
                        capture.release()
                        break;






