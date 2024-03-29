#include "LineObject.h"

using namespace cv;

LineObject::LineObject(Point input1, Point input2){
        point1 = input1;
        point2 = input2;
	}

int LineObject::compare(LineObject other){
	if (size() > other.size()){
		return 1;
	}else if (size() < other.size()){
		return -1;
	}else{
		return 0;
	}
}   
int LineObject::size(){
    return int(sqrt(((point1.x - point2.x)^2) + ((point1.y - point2.y)^2))) ;  
} 

void LineObject::display(Mat raw){
		line(raw,point1,point2,Scalar(0,255,0),2);
}      

void LineObject::display(Mat raw,Scalar colour){
		line(raw,point1,point2,colour,2);
}  

double LineObject::calculateGradient() const{
	double deltaX = point1.x-point2.x;
    double deltaY = point1.y-point2.y;
    if (deltaX != 0){
		return (deltaY/deltaX);
	}else{
		return SUDO_INF;
	}
}

Point LineObject::midPoint(int windowHeight){
	//Calculate the gradient of the line
	double gradient = calculateGradient();
	//Calculate the c value of the line
	double c = (point1.y-gradient*point1.x);
	
	
	//Calculate the x offset
	double x  = ((windowHeight/2)-c)/gradient;
	
	//Return
	return Point(x,windowHeight/2);
}


bool LineObject::operator == (const LineObject& o) const {
return calculateGradient() == o.calculateGradient();
}

bool LineObject::operator< (const LineObject & l2) const{
return calculateGradient() < l2.calculateGradient();//Compare(o)<0;   
}


