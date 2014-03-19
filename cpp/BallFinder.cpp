#include "BallFinder.h"



BallFinder::BallFinder(vector<int> inputHSV): ImageProccessor(inputHSV){	
    //objects = new vector<BlobObject>;
    minObjectSize = 3;
}
void BallFinder::findObjects(){
	Point2f centre;
	float radius;
	vector<int> contours;
    // Find contours  
    findContours(working,contours, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE);
    //remove contours that are too small
    if (contours.size() > 0){
        for(size_t i=0;i<contours.size();i++){    
                    //contours[i] = cv2.approxPolyDP(contours[i],3,True)
                    //rectangle = cv.MinAreaRect2(contours,storage)
                    minEnclosingCircle(contours[i],centre,radius);
					if (radius > minObjectSize){				
                            objects.push_back(BlobObject(centre,radius));
					}
		}
	}
}         
BlobObject* BallFinder::getBiggestObject(){
	sort(objects.begin(),objects.end());
    if (objects.size() > 0){
        return &objects[objects.size()-1];
	}
    else{
        return NULL;
	}
}

void BallFinder::printBiggestObject(Mat raw){
    BlobObject* blob = getBiggestObject();
    if (blob != NULL){
        blob->display(raw);
	}
}


