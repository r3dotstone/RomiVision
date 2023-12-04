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

# Parameter Window
def empty(x):
    pass
cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters",640,240)
cv2.createTrackbar("Canny 1", "Parameters", 150, 255, empty)
cv2.createTrackbar("Canny 2", "Parameters", 255, 255, empty)
cv2.createTrackbar("Hue", "Parameters", 255, 255, empty)
cv2.createTrackbar("Saturation", "Parameters", 255, 255, empty)
cv2.createTrackbar("Value", "Parameters", 255, 255, empty)

while (True):

    canny1 = cv2.getTrackbarPos("Canny 1", "Parameters")
    canny2 = cv2.getTrackbarPos("Canny 2", "Parameters")
    hue = cv2.getTrackbarPos("Hue", "Parameters")
    sat = cv2.getTrackbarPos("Saturation", "Parameters")
    val = cv2.getTrackbarPos("Value", "Parameters")

    # capture
    image = picam2.capture_array("main")
    # blur
    image_blur = cv2.GaussianBlur(image, (7, 7), 1)
    # greyscale
    image_grey = cv2.cvtColor(image_blur,cv2.COLOR_BGR2GRAY)
    # edge find
    image_edges = cv2.Canny(image_grey,canny1,canny2)
    




    #convert to HSV
    hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    #Threshold GREEEN STUFFFFFFF
    lower_bound = np.array([20,190,60])
    upper_bound = np.array([60,255,255])
    #create a mask of pixels in this range
    mask = cv2.inRange(hsv,lower_bound,upper_bound)
    #now we use mask to threshold our image!
    image_threshed = cv2.bitwise_and(image,image,mask=mask)
    #now convert to grayscale for centroid calc
    image_threshed_grey = cv2.cvtColor(image_threshed,cv2.COLOR_BGR2GRAY)

    #Find contours
    contours, _ = cv2.findContours(image_threshed_grey, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
    
    # iterate through contours
    i = 0
    square = False
    for contour in contours: 
  
    # here we are ignoring first counter because  
    # findcontour function detects whole image as shape 
    
        if i == 0: 
            i = 1
            continue
    
        if cv2.contourArea(contour) < 250:
            continue

        # cv2.approxPloyDP() function to approximate the shape 
        polys = cv2.approxPolyDP( 
            contour, 0.01 * cv2.arcLength(contour, True), True) 
        
        # using drawContours() function 
        #cv2.drawContours(img, [contour], 0, (0, 0, 255), 5) 

        # finding center point of shape 
        M = cv2.moments(contour) 
        if M['m00'] != 0.0: 
            x = int(M['m10']/M['m00']) 
            y = int(M['m01']/M['m00']) 
    
        # putting shape name at center of each shape 
        # if len(polys) == 3: 
        #     cv2.putText(img, 'Triangle', (x, y), 
        #                 cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2) 
    
        elif len(polys) == 4:
            square = True
            cv2.putText(image_threshed_grey, 'Yellow square!', (x, y), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2) 
    
        # elif len(polys) == 5: 
        #     cv2.putText(img, 'Pentagon', (x, y), 
        #                 cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2) 
    
        # elif len(polys) == 6: 
        #     cv2.putText(img, 'Hexagon', (x, y), 
        #                 cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2) 
    
        # else: 
        #     cv2.putText(img, 'circle', (x, y), 
        #                 cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2) 
        else:
            square = False

        if square:
            #now find centroid! Use the moments function
            M = cv2.moments(mask)
            #to find the centroid...
            if(M["m00"] != 0):
                cX = int(M["m10"]/M["m00"])
                cY = int(M["m01"]/M["m00"])
            else:
                cX, cY = 0, 0

            # calculate and scale error
            e = int((cX - cWidth/2) * 150 / cWidth*2)

            # contrained motor commands
            lCmd = np.clip(150 + e, -255, 255)
            rCmd = np.clip(150 - e, -255, 255)

            # if conting can be found, spin around and look 
            if (cX == cY == 0):
                lCmd = -100
                rCmd = 100
        else:
            lCmd = -30
            rCmd = 30
            e = "No Squares Detected"

    # dislay image feed
    cv2.imshow("camera",image_edges)
    cv2.waitKey(1)

    print(lCmd, rCmd, e)
    # romi.motors(lCmd, rCmd)
