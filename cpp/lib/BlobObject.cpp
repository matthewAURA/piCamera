#include "BlobObject.h"

using namespace cv;

BlobObject::BlobObject(Point2f inputCentre, int inputRadius){
        centre = inputCentre;
        radius = inputRadius;
}
        
bool BlobObject::operator <(BlobObject other) const{
    return radius > other.radius;
}    
    
    
int BlobObject::compare(BlobObject other){
	if (radius > other.radius){
		return 1;
	}else if (radius < other.radius){
		return -1;
	}else{
		return 0;
	}
}

void BlobObject::display(Mat raw){
	circle(raw,centre,radius,Scalar(0,255,0),3,5,0);
}

