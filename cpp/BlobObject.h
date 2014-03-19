/*
 * BlobObject.h
 *
 *  Created on: 25/05/2013
 *      Author: matthew
 */
#ifndef BLOBOBJECT_H
#define BLOBOBJECT_H

#ifndef OPENCV_LIB
#define OPENCV_LIB

#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"

#endif

using namespace cv;

class BlobObject{
	private:
	    Point2f centre;
        int radius;	
	public:
        BlobObject(Point2f inputCentre, int inputRadius);
        bool operator<(BlobObject other) const ;
        int compare(BlobObject other);
	    void display(Mat raw);
};

#endif
