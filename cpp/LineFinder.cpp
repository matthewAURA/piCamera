#include "LineFinder.h"

using namespace cv;

LineFinder::LineFinder(vector<int> valHSV,int in_scale) : ImageProccessor(valHSV){
		scale = in_scale;
}
void LineFinder::findLines(){
	//self.working=  cv2.GaussianBlur( self.working,(9, 9),2 )
	//Do a Canny edge detection
	vector<Vec2f> lines;
	points.clear();
	Canny(working,working, 0, 400);
	HoughLines(working,lines,1, M_PI/180.0, 120, 0, 0);
	if (lines.size() > 0){
		  for( size_t i = 0; i < lines.size(); i++ ){
			float rho = lines[i][0];
			float theta = lines[i][1];
			double a = cos(theta), b = sin(theta);
			double x0 = a*rho, y0 = b*rho;
			Point pt1(cvRound(x0 + 1000*(-b)),cvRound(y0 + 1000*(a)));
			Point pt2(cvRound(x0 - 1000*(-b)),cvRound(y0 - 1000*(a)));
			points.push_back(LineObject(pt1,pt2));
		}
	}
}

void LineFinder::printLines(Mat raw){
	if (points.size() > 0){
		for (size_t i=0;i<points.size();i++){
			points[i].display(raw);
		}
	}
}

LineObject* LineFinder::getBestLine(){
	if (points.size() > 0){
		sort(points.begin(),points.end());;
		return &points[points.size()-1];
	}else{
		return NULL;
	}
}

double LineFinder::calculateBestGradient(){
	if (points.size() > 0){
			return (180*(atan(getBestLine()->calculateGradient()))/M_PI);
		}
	return 0;
}

void LineFinder::drawErrorLine(Mat frame,int height,int width){
	LineObject* drawLine = calculateErrorLine(height,width);
	if (drawLine != NULL){
		cout << "Size: " << drawLine->size() << endl;
		drawLine->display(frame,Scalar(255,0,0));
	}
}

LineObject* LineFinder::calculateErrorLine(int height,int width){
	Point pt1 = Point(width/2,height/2);
	
	LineObject* bestLine = getBestLine();
	if (bestLine != NULL){
		Point pt2 = bestLine->midPoint(height);
		//Create a new line
		LineObject lineVal = LineObject(pt1,pt2);
		return &lineVal;
	}
	return 0;
}

