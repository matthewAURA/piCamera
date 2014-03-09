import cv2
import numpy as np
import time
import trackingLib
import MattSerial
import sys

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
        valHSV = [122, 255, 255, 100, 250, 253]
        #values for white
        #valHSV = [250, 26, 194, 0, 0, 164]        
    return valHSV

def onMouse(event,x,y,flags,userData):
    if (event == cv2.cv.CV_EVENT_LBUTTONDOWN):
        roiSize = userData.shape[0]/12
        roi = userData[y-roiSize:y+roiSize,x-roiSize:x+roiSize]
        cv2.imshow("ROI", roi)
        roi = cv2.cvtColor(roi, cv2.cv.CV_BGR2HSV)
        #print np.std(roi[:,:,1])+np.median(roi[:,:,1])
        cv2.setTrackbarPos("Hue", "Raw", int(2*np.std(roi[:,:,0])+np.median(roi[:,:,0])))
        cv2.setTrackbarPos("Hue Min", "Raw", int(-2*np.std(roi[:,:,0])+np.median(roi[:,:,0])))
        cv2.setTrackbarPos("Saturation", "Raw", int(1*np.std(roi[:,:,1])+np.median(roi[:,:,1])))
        cv2.setTrackbarPos("Sat Min", "Raw", int(-1*np.std(roi[:,:,1])+np.median(roi[:,:,1])))
        cv2.setTrackbarPos("Value", "Raw", int(np.std(roi[:,:,2])+np.median(roi[:,:,2])))
        cv2.setTrackbarPos("Value Min", "Raw", int(-np.std(roi[:,:,2])+np.median(roi[:,:,2])))
        
        
        
def main(argv):        
    #Dimentions of Capture window
    width = 640/2
    height = 480/2

    #Open capture device
    device = 0 # assume we want first device
    
    if '-h' in argv:
        print "Options:"
        print "-g for GUI"
        print "-r to record input"
        print "-f to show fps"
        sys.exit(0)

    gui = '-g' in argv
    record = '-r' in argv
    fps = '-f' in argv

    #create video capture device, set capture area
    capture = cv2.VideoCapture(device)
    capture.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,width)
    capture.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,height)

    #create recording object
    if record:
        recorder = cv2.VideoWriter("test.avi", cv2.cv.CV_FOURCC('D','I','V','X'), 30,(width,height))
        if not recorder.isOpened():
            assert("VideoWriter could not be opened")

    #create serial connection
    ser = MattSerial.SerialController("/dev/ttyACM0",9600)

    valHSV = getHSV(False)
    imgproc = trackingLib.ballFinder(valHSV)
    if gui:
        cv2.namedWindow("Raw")
        cv2.createTrackbar("Hue","Raw",valHSV[0],255,on_change);
        cv2.createTrackbar("Saturation","Raw",valHSV[1],255,on_change); 
        cv2.createTrackbar("Value","Raw",valHSV[2],255,on_change);
        cv2.createTrackbar("Hue Min","Raw",valHSV[3],255,on_change);
        cv2.createTrackbar("Sat Min","Raw",valHSV[4],255,on_change);     
        cv2.createTrackbar("Value Min","Raw",valHSV[5],255,on_change);
        


    #create image processing objects

    #imgproc.configWebcam("object")
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
                    
                    if gui:
                        cv2.setMouseCallback("Raw", onMouse,raw)
                    
                    imgproc.valHSV = getHSV(gui)
                    imgproc.getHSV()
                    
                    imgproc.fillHoles()
                    imgproc.findObjects()
                    imgproc.printBiggestObject(raw)
                    target = imgproc.getBiggestObject()
                    time2= time.time()                  
                    
                    if target is not None:                    
                        pos = (target.centre[0]/float(width))*100
                        #send position to cortex
                        print pos
                        ser.sendInt(int(pos))

                    if gui:
                        cv2.imshow("Raw",raw)
                    if fps:
                        try:
                            print (1/(time2-time1))
                        except (ZeroDivisionError):
                            print("inf")
                    if record:
                        recorder.write(raw)
                    if(cv2.waitKey(30) >= 0) :
                        capture.release()
                        break;

if  __name__ =='__main__':main(sys.argv[1:])




