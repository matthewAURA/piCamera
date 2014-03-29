import cv2
import numpy as np
from trackingLib import *

#create test lines
point1 = Point(100,100)
point2 = Point(0,100)

line = lineObject(point1,point2)

#create canvas
plane = CartesianPlane(400,400)
plane.vectors.append(line)

plane.drawAll()

while(True):
    if(cv2.waitKey(30) >= 0) :
        break