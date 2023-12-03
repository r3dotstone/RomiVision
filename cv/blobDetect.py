import cv2
import numpy as np
from picamera2 import Picamera2
import time

cHeight = 1080
cWidth = 1920

picam2 = Picamera2()
config = picam2.create_preview_configuration(main={'size': (1920, 1080), 'format': 'XRGB8888'})
picam2.configure(config)

picam2.start()

while (True):
    image = picam2.capture_array("main")

    #image = np.frombuffer(cameraData, np.uint8).reshape((cHeight, cWidth, 4))
    #convert to HSV
    hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    #Threshold GREEEN STUFFFFFFF
    lower_bound = np.array([80*255/360,30,30])
    upper_bound = np.array([150*255/360,255,255])
    #create a mask of pixels in this range
    mask = cv2.inRange(hsv,lower_bound,upper_bound)
    #now we use mask to threshold our image!
    thresh = cv2.bitwise_and(image,image,mask=mask)
    #now convert to grayscale for centroid calc
    grey = cv2.cvtColor(thresh,cv2.COLOR_BGR2GRAY)
    #now find centroid! Use the moments function
    M = cv2.moments(mask)
    #to find the centroid...
    if(M["m00"] != 0):
        cX = int(M["m10"]/M["m00"])
        cY = int(M["m01"]/M["m00"])
    else:
        cX, cY = 0, 0
    #add a label to original image!!
    cv2.circle(image,(cX,cY),5,(0,0,255),-1)
    cv2.putText(image,"centroid",(cX-25,cY-25),
    cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),2)

    #display camera Image
    cv2.imshow("camera",image)
    cv2.waitKey(1)