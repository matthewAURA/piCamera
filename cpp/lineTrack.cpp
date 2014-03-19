

//#define time
#define LINUX

#include "LineObject.h"
#include "GUI.h"
#include "LineFinder.h"
#include "timer.h"
using namespace cv;


int main(){
	//Dimensions of Capture window
	int scale = 1;
	int width = 640/scale;
	int height = 480/scale;
	int lineSize;
	unsigned int start_time,stop_time;
	//Open capture device
	int device = 0; //assume we want first device

	bool gui = true;
	bool record = false;

	//create video capture device, set capture area
	VideoCapture capture = VideoCapture(device);
	capture.open(device);
	capture.set(CAP_PROP_FRAME_WIDTH,width);
	capture.set(CAP_PROP_FRAME_HEIGHT,height);


	//create recording object
	VideoWriter *recorder;
	//recorder = new VideoWriter ("test.avi",cv::CV_F FOURCC('D','I','V','X'), 30,Point(width,height));
	if (!recorder->isOpened() && record){
		return 0;
	}


	//Construct GUI object
	DebugGUI myGUI = DebugGUI(gui);

	//create image processing objects
	LineFinder imgproc = LineFinder(myGUI.getHSV(),scale);
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
				imgproc.setFrame(raw.clone());
			}else{
				imgproc.setFrame(raw);
			}
			imgproc.setHSV(&myGUI);
			/*//imgproc.getGray();
			imgproc.thresholdHSV();
			imgproc.fillHoles();
			//imgproc.findObjects();
			//imgproc.printBiggestObject(raw)
			imgproc.findLines();
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

#ifdef time
			stop_time = GetTimeMs64();
			cout << "FPS: "  <<  1000/(stop_time - start_time) << endl;
#else
			cout << "Gradient: " << size << " " << "Offset: " << lineSize  << endl;
#endif
			*/
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



