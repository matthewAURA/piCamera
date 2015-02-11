#ifndef LINEOBJECT_H
#define LINEOBJECT_H

#ifndef OPENCV_LIB
#define OPENCV_LIB

#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
using namespace cv;
#endif


#define SUDO_INF 100000000

class LineObject{
	private:
		Point point1,point2;
	public:	
        LineObject(Point input1, Point input2);
        int compare(LineObject other);
        int size();
	    void display(Mat raw);
	    void display(Mat raw,Scalar colour);
	    double calculateGradient() const;
	    Point midPoint(int windowHeight);
        bool operator == (const LineObject& o) const;
        bool operator< (const LineObject & l2) const;
};

#endif

