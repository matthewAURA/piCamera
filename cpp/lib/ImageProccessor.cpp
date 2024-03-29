#include "ImageProccessor.h"

using namespace cv;

ImageProccessor::ImageProccessor(vector<int> inputVals){
    valHSV = inputVals;
}
Mat ImageProccessor::getFrame(){
	return working;
}
void ImageProccessor::setFrame(Mat frame){
	working = frame;
}        

void ImageProccessor::setHSV(DebugGUI* gui){
	valHSV = gui->getHSV();
}        
            
void ImageProccessor::configWebcam(String mode){
    if (mode == "line"){		
        system("uvcdynctrl -s Brightness 100");
        system("uvcdynctrl -s Contrast 255");
        system("uvcdynctrl -s Saturation 21");
        system("uvcdynctrl -s \"Exposure (Absolute)\" 166");
        system("uvcdynctrl -s \"Exposure, Auto Priority\" 0");
        system("uvcdynctrl -s \"Exposure, Auto\" 0");      
        system("uvcdynctrl -s \"White Balance Temperature, Auto\" 0");
	}else if  (mode == "object"){
	#ifdef LINUX
        system('uvcdynctrl -s Brightness 150');
        system('uvcdynctrl -s Contrast 37');
        system('uvcdynctrl -s Saturation 190');
        system('uvcdynctrl -s "Exposure (Absolute)" 166');
        system('uvcdynctrl -s "Exposure, Auto Priority" 0');
        system('uvcdynctrl -s "Exposure, Auto" 0');      
        system('uvcdynctrl -s "White Balance Temperature, Auto" o') ;            
	#else
		//Do nothing
	#endif
	}
}

void ImageProccessor::thresholdHSV(){
    //Convert to HSV space for better filtering
    cvtColor(working,working,COLOR_BGR2HSV);
    //Threshold each channel
    inRange(working,Scalar(valHSV[3],valHSV[4],valHSV[5]),Scalar(valHSV[0],valHSV[1],valHSV[2]),working);
    //Equalize A histogram for better contrast
    equalizeHist(working,working);   
}
void ImageProccessor::fillHoles(){                
    //create erode and dilate kernels 
    Mat erodeKernel = getStructuringElement(MORPH_RECT,Point(5,5));
    Mat dilateKernel = getStructuringElement(MORPH_RECT,Point(15,15));
    //Perform Erode and dilate to fill holes in image
    erode(working,working,erodeKernel);
    dilate(working,working, dilateKernel);
}
    
void ImageProccessor::getGray(){
    cvtColor(working,working,COLOR_BGR2GRAY);
}

void ImageProccessor::show(String name){
	imshow(name,working);
}

