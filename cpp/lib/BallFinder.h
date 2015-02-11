#ifndef BALLFINDER_H
#define BALLFINDER_H

#include "ImageProccessor.h"
class BlobObject;

#include "BlobObject.h"

#ifndef VECTOR_H
#define VECTOR_H
#include <vector>
using namespace std;
#endif

#ifndef OPENCV_LIB
#define OPENCV_LIB

#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
using namespace cv;
#endif



class BallFinder: public ImageProccessor{
private:
	vector<BlobObject> objects;
	int minObjectSize;
public:
    BallFinder(vector<int> inputHSV);
    void findObjects();
    BlobObject* getBiggestObject();
    void printBiggestObject(Mat raw);
};

#endif

