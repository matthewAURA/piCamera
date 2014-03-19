#ifndef LINEFINDER_H
#define LINEFINDER_H

#include "ImageProccessor.h"
#include "LineObject.h"


#ifndef OPENCV_LIB
#define OPENCV_LIB

#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
using namespace cv;
#endif

#ifndef VECTOR_H
#define VECTOR_H
#include <vector>
using namespace std;
#endif

#ifndef IOSTREAM_H
#define IOSTREAM_H
#include <iostream>
#endif

class LineFinder : public ImageProccessor{
    private:
		vector <LineObject> points;
		int scale;
    public:
		LineFinder(vector<int> valHSV,int in_scale);
        void findLines();
        void printLines(Mat raw);
        LineObject* getBestLine();
        double calculateBestGradient();
	    void drawErrorLine(Mat frame,int height,int width);
	    LineObject* calculateErrorLine(int height,int width);
};  

#endif
