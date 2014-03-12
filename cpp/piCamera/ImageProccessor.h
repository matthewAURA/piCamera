#ifndef OPENCV_LIB
#define OPENCV_LIB

#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
using namespace cv;
#endif

#ifndef IMAGEPROCCESSOR_H
#define IMAGEPROCCESSOR_H

#ifndef VECTOR_H
#define VECTOR_H
#include <vector>
using namespace std;
#endif


#include "GUI.h"






class ImageProccessor{
private:
	vector<int> valHSV;
protected:
	Mat working;
public:	
    ImageProccessor(vector<int> inputVals);
    Mat getFrame();
    void setFrame(Mat frame);
    void setHSV(DebugGUI* gui);
    void configWebcam(String mode);
	void thresholdHSV();
	void fillHoles();
    void getGray();
	void show(String name);
};

#endif


