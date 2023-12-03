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

params = cv2.SimpleBlobDetector_Params() 

params.filterByArea = True
params.minArea = 10
  
params.filterByCircularity = True 
params.minCircularity = 0.6
params.maxCircularity = 0.85

detector = cv2.SimpleBlobDetector_create(params)

while (True):
    image = picam2.capture_array("main")

    hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    lower_bound = np.array([20,190,60])
    upper_bound = np.array([70,255,255])
    mask = cv2.inRange(hsv,lower_bound,upper_bound)
    thresh = cv2.bitwise_and(image,image,mask=mask)
    grey = cv2.cvtColor(thresh,cv2.COLOR_BGR2GRAY)
    M = cv2.moments(mask)
    if(M["m00"] != 0):
        cX = int(M["m10"]/M["m00"])
        cY = int(M["m01"]/M["m00"])
    else:
        cX, cY = 0, 0
    
    keypoints = detector.detect(grey)

    rCmd = 0
    lCmd = 0
    e = 0
    for kp in keypoints:
        e = int((kp.pt[0] - cWidth/2) * 150 / cWidth*2)
        lCmd = np.clip(150 + e, -255, 255)
        rCmd = np.clip(150 - e, -255, 255)

    print(lCmd, rCmd, e, keypoints[0].pt[0], keypoints[0].pt[1])
    #romi.motors(lCmd, rCmd)

    cv2.circle(grey,(cX,cY),5,(0,0,255),-1)
    cv2.putText(grey,"centroid",(cX-25,cY-25),
    cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),2)
    
    cv2.imshow("camera",grey)
    cv2.waitKey(1)