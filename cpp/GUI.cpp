/*
 * GUI.cpp
 *
 *  Created on: 25/05/2013
 *      Author: matthew
 */
#include "GUI.h"



DebugGUI::DebugGUI(bool input){
		//Do constructor stuff
		valHSV = vector<int> (6,0);
		gui = input;
		calculateHSV(false);	
		if (gui){
			namedWindow("Raw");
			createTrackbar("Hue","Raw",&valHSV[0],255,0,0);
			createTrackbar("Saturation","Raw",&valHSV[1],255,0,0);
			createTrackbar("Value","Raw",&valHSV[2],255,0,0);
			createTrackbar("Hue Min","Raw",&valHSV[3],255,0,0);
			createTrackbar("Sat Min","Raw",&valHSV[4],255,0,0);
			createTrackbar("Value Min","Raw",&valHSV[5],255,0,0);
		}
}

void DebugGUI::calculateHSV(bool input){
if (input){
    valHSV[0] = getTrackbarPos("Hue","Raw");
    valHSV[3] = getTrackbarPos("Hue Min","Raw");
    valHSV[1] = getTrackbarPos("Saturation","Raw");
    valHSV[4] = getTrackbarPos("Sat Min","Raw");
    valHSV[2] = getTrackbarPos("Value","Raw");
    valHSV[5] = getTrackbarPos("Value Min","Raw") ;
} else{
    //Values for blue:
    //valHSV = [142,229,243,104,100,120]
    //values for white
    int whiteVals [] = {250, 26, 194, 0, 0, 164};
	for (int i=0;i<6;i++){
		valHSV[i] = whiteVals[i];//whiteVals, whiteVals + sizeof(whiteVals) / sizeof(int) );
	}
}
}

vector<int> DebugGUI::getHSV(){
	return valHSV;
}

