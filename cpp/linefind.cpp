

//#define time
#define LINUX

#include "LineObject.h"
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


int main(){
	//Dimensions of Capture window
	int scale = 4;
	int width = 640/scale;
	int height = 480/scale;
	int lineSize;
	unsigned int start_time,stop_time;
	//Open capture device
	int device = 0; //assume we want first device


	//create video capture device, set capture area
	VideoCapture capture = VideoCapture(device);
	capture.open(device);
	capture.set(CV_CAP_PROP_FRAME_WIDTH,width);
	capture.set(CV_CAP_PROP_FRAME_HEIGHT,height);
    vector<int> valHSV;

	//create image processing objects
    LineFinder imgproc = LineFinder(valHSV,scale);
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
            cvtColor(raw,raw,CV_BGR2GRAY);
			imgproc.setFrame(raw);
            imgproc.findLines();
            imgproc.printLines(raw);
            imshow("raw",raw);
            stop_time = GetTimeMs64();
			cout << imgproc.calculateBestGradient() << endl;
#ifdef time
            cout << "FPS: "  <<  1000/(stop_time - start_time) << endl;
#else
			//cout << "Gradient: " << size << " " << "Offset: " << lineSize  << endl;
#endif
			if(waitKey(30) >= 0){
				return 0;
			}
		}
	}
}



