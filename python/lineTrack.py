import cv2
import numpy as np
import random
import time
import trackingLib

def on_change(var):
    pass

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
        valHSV = [122, 255, 255, 100, 250, 253]
    #values for white
    #valHSV = [250, 26, 194, 0, 0, 164]
    return valHSV

def onMouse(event,x,y,flags,userData):
    if (event == cv2.cv.CV_EVENT_LBUTTONDOWN):
        roiSize = userData.shape[0]/16
        roi = userData[y-roiSize:y+roiSize,x-roiSize:x+roiSize]
        cv2.imshow("ROI", roi)
        roi = cv2.cvtColor(roi, cv2.cv.CV_BGR2HSV)
        stdDevs = 2
        cv2.setTrackbarPos("Hue", "Raw", int(stdDevs*np.std(roi[:,:,0])+np.median(roi[:,:,0])))
        cv2.setTrackbarPos("Hue Min", "Raw", int(-stdDevs*np.std(roi[:,:,0])+np.median(roi[:,:,0])))
        cv2.setTrackbarPos("Saturation", "Raw", int(stdDevs*np.std(roi[:,:,1])+np.median(roi[:,:,1])))
        cv2.setTrackbarPos("Sat Min", "Raw", int(-stdDevs*np.std(roi[:,:,1])+np.median(roi[:,:,1])))
        cv2.setTrackbarPos("Value", "Raw", int(stdDevs*np.std(roi[:,:,2])+np.median(roi[:,:,2])))
        cv2.setTrackbarPos("Value Min", "Raw", int(-stdDevs*np.std(roi[:,:,2])+np.median(roi[:,:,2])))



#Dimentions of Capture window
scale = 1
width = 640/scale
height = 480/scale

#Open capture device
device = 0 # assume we want first device

gui = False
record = False

rollingError = []

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

lineTol = 140

if gui:
    cv2.namedWindow("Raw")
    cv2.createTrackbar("Hue","Raw",valHSV[0],255,on_change);
    cv2.createTrackbar("Saturation","Raw",valHSV[1],255,on_change);
    cv2.createTrackbar("Value","Raw",valHSV[2],255,on_change);
    cv2.createTrackbar("Hue Min","Raw",valHSV[3],255,on_change);
    cv2.createTrackbar("Sat Min","Raw",valHSV[4],255,on_change);
    cv2.createTrackbar("Value Min","Raw",valHSV[5],255,on_change);
    cv2.createTrackbar("Line Strictness","Raw",lineTol,300,on_change)



#create image processing objects
imgproc = trackingLib.lineFinder(valHSV,width,height)
#imgproc.configWebcam("line")
if(capture):  # check if we succeeded
    
        #main loop
        while(True):
                time1 = time.time()
                #Pull a frame from the camera to the raw image
                # capture the current frame
                raw = capture.read()[1]
                
                if raw is None:
                        break
                
                if gui:
                    cv2.setMouseCallback("Raw", onMouse,raw)
                    lineTol = cv2.getTrackbarPos("Line Strictness","Raw")

        
                imgproc.frame = raw
                #imgproc.valHSV = getHSV(gui)
                #imgproc.getHSV()
                imgproc.getGray()
                imgproc.fillHoles()
                #imgproc.findObjects()
                #imgproc.printBiggestObject(raw)
                
                imgproc.findLineSegments(lineTol)
                imgproc.printLines(raw)
                error = imgproc.drawErrorLines(raw)
                if error is not None:
                    if len(rollingError) < 5:
                        rollingError.append(error.x)
                    else:
                        rollingError = (rollingError[1:])
                        rollingError.append(int(error.x))
                print np.mean(rollingError)
                #cv2.imshow("filter",imgproc.frame)
                time2 = time.time()
                #print (1/(time2-time1))
                #size =  imgproc.calculateBestGradient()
                size = None
                if size is not None:
                    print size
                if gui: 
                    cv2.imshow("Raw",raw)
                    #imgproc.plane.drawAll()
                if record:
                    recorder.write(imgproc.frame)
                if(cv2.waitKey(30) >= 0) :
                        capture.release()
                        break;






