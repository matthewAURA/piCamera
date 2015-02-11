

//#define time
#define RECORD

#include "LineObject.h"
#include "GUI.h"
#include "LineFinder.h"
#include "timer.h"
#include "math.h"
using namespace cv;


void onMouse(int event,int x,int y,int,void* param){
    if (event == CV_EVENT_LBUTTONDOWN){
        Mat img = *((Mat *)param);
        Mat roi = img(Rect(x,y,img.cols/12,img.rows/12));
        imshow("roi",roi);
        cvtColor(roi,roi,CV_BGR2HSV);
        Scalar cvMean;
        Scalar cvStddev;
        meanStdDev(roi, cvMean, cvStddev);
        setTrackbarPos("Hue","Raw",(int)cvMean[0]+1*cvStddev[0] > 255 ? 255 : (int)cvMean[0]+1*cvStddev[0] );
        setTrackbarPos("Hue Min","Raw",(int)cvMean[0]-1*cvStddev[0]);
        setTrackbarPos("Saturation","Raw",(int)cvMean[1]+cvStddev[1]);
        setTrackbarPos("Sat Min","Raw",(int)cvMean[1]-cvStddev[1]);
        setTrackbarPos("Value","Raw",(int)cvMean[2]+cvStddev[2]);
        setTrackbarPos("Value Min","Raw",(int)cvMean[2]-cvStddev[2]);
    }
}


int main(int argc, char *argv[]){
	//Dimensions of Capture window
    int scale = 1;
    if (argc > 1){
        sscanf(argv[1],"%d",&scale);
        cout << scale << endl;
    }
	int width = 640/scale;
	int height = 480/scale;
	int lineSize;
	unsigned int start_time,stop_time;
	//Open capture device
	int device = 0; //assume we want first device

	bool gui = false;
	bool record = false;

	//create video capture device, set capture area
	VideoCapture capture = VideoCapture(device);
	capture.open(device);
	capture.set(CV_CAP_PROP_FRAME_WIDTH,width);
	capture.set(CV_CAP_PROP_FRAME_HEIGHT,height);


    
	//create recording object
	VideoWriter *recorder;
	if (record){
	recorder = new VideoWriter ("test.avi",CV_FOURCC('D','I','V','X'), 30,Point(width,height));
	if (!recorder->isOpened() && record){
		return 0;
	}
	}


	//Construct GUI object
    DebugGUI myGUI(gui);
    
	//create image processing objects
	LineFinder imgproc(myGUI.getHSV(),scale);
	//imgproc.configWebcam("line");
	if(capture.isOpened()){  //check if we succeeded
		Mat raw;
		//main loop
		while(true){
			start_time = GetTimeMs64();

			//Pull a frame from the camera to the raw image
			// capture the current frame

			if (!capture.grab()){
				break;
			}
			capture >> raw;

			if (gui){
                setMouseCallback("Raw",onMouse,&raw);
				imgproc.setFrame(raw.clone());
			}else{
				imgproc.setFrame(raw);
			}
            myGUI.calculateHSV(true);
			imgproc.setHSV(&myGUI);
			//imgproc.getGray();
			imgproc.thresholdHSV();
			imgproc.fillHoles();
            if (gui){
                imshow("Working",imgproc.getFrame());
            }
			//imgproc.findObjects();
			//imgproc.printBiggestObject(raw)
			//imgproc.findLines();
			double size =  imgproc.calculateBestGradient();
			LineObject* drawLine = imgproc.calculateErrorLine(height,width);
			if (drawLine != 0){
				lineSize = drawLine->size();
			}else{
				lineSize = 0;
			}
			if (gui){
				imgproc.drawErrorLine(raw,height,width);
				imgproc.printLines(raw);
			}
			//print (1/(time2-time1))

            stop_time = GetTimeMs64();
			cout << "FPS: "  <<  1000/(stop_time - start_time) << endl;
#ifdef time

#else
			//cout << "Gradient: " << size << " " << "Offset: " << lineSize  << endl;
#endif
			
			if (gui){
				imshow("Raw",raw);
			}
			if (record){
				recorder->write(raw);
			}
			if(waitKey(30) >= 0){
				return 0;
			}
		}
	}
}



