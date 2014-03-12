/*
 * GUI.h
 *
 *  Created on: 25/05/2013
 *      Author: matthew
 */

#ifndef OPENCV_LIB
#define OPENCV_LIB

#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
using namespace cv;
#endif

#ifndef DEBUGGUI_H
#define DEBUGGUI_H

#ifndef VECTOR_H
#define VECTOR_H
#include <vector>
using namespace std;
#endif





class DebugGUI {
private:
	vector<int> valHSV;
	bool gui;
public:
    DebugGUI(bool input);
    void calculateHSV(bool input);
    vector<int> getHSV();
};


#endif
