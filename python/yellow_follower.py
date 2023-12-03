import cv2
import numpy as np
from picamera2 import Picamera2
import time

from romi_interface.romi import Romi
romi = Romi()

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
    lower_bound = np.array([20,0,0])
    upper_bound = np.array([70,255,255])
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

    e = (cX - cWidth/2) * 255 / cWidth*2

    lCmd = np.clip(255 + e, 0, 255)
    rCmd = np.clip(255 - e, 0, 255)
    romi.motors(lCmd, rCmd)