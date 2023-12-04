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
cv2.createTrackbar("Canny 1", "Parameters", 52, 255, empty)
cv2.createTrackbar("Canny 2", "Parameters", 96, 255, empty)
cv2.createTrackbar("Area Threshold", "Parameters", 2500, 10000, empty)
cv2.createTrackbar("Hue", "Parameters", 255, 255, empty)
cv2.createTrackbar("Saturation", "Parameters", 255, 255, empty)
cv2.createTrackbar("Value", "Parameters", 255, 255, empty)
cv2.createTrackbar("Epsilon", "Parameters", 464, 10000, empty)

while (True):

    canny1 = cv2.getTrackbarPos("Canny 1", "Parameters")
    canny2 = cv2.getTrackbarPos("Canny 2", "Parameters")
    area = cv2.getTrackbarPos("Area Threshold", "Parameters")
    hue = cv2.getTrackbarPos("Hue", "Parameters")
    sat = cv2.getTrackbarPos("Saturation", "Parameters")
    val = cv2.getTrackbarPos("Value", "Parameters")
    eps = cv2.getTrackbarPos("Epsilon", "Parameters")

    # capture
    image = picam2.capture_array("main")
    image_contours = image.copy()
    # blur
    image_blur = cv2.GaussianBlur(image, (7, 7), 1)
    # greyscale
    image_grey = cv2.cvtColor(image_blur,cv2.COLOR_BGR2GRAY)




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

    # edge find
    image_edges = cv2.Canny(image_threshed_grey,canny1,canny2)

    # dilate
    dilatationKernal = np.ones((5,5))
    image_dilate = cv2.dilate(image_edges, dilatationKernal, iterations = 1) 

    #Find contours
    contours, _ = cv2.findContours(image_dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
    
    # iterate through contours
    i = 0
    polys = []
    square = False
    triangle = False

    if triangle == True:
        sign = -1
    else:
        sign = 1

    lCmd = 0
    rCmd = 0
    e = "init"

    for contour in contours: 
  
    # here we are ignoring first counter because  
    # findcontour function detects whole image as shape 
    
        if i == 0: 
            i = 1
            continue
    
        # skip it if smaller than 2500 pixels^2
        if cv2.contourArea(contour) < area:
            continue


        # cv2.approxPloyDP() function to approximate the shape 
        polys = cv2.approxPolyDP( 
            contour, eps/10000 * cv2.arcLength(contour, True), True) 
        print("verticies = ",polys)

        cv2.drawContours(image_contours, polys, -1, (255, 0, 255), 7, cv2.LINE_AA)

        # using drawContours() function 
        #cv2.drawContours(img, [contour], 0, (0, 0, 255), 5) 

        # finding center point of shape 
        # mContour = cv2.moments(contour) 
        # if mContour['m00'] != 0.0: 
        #     x = int(mContour['m10']/mContour['m00']) 
        #     y = int(mContour['m01']/mContour['m00']) 
    
        # putting shape name at center of each shape 
        # if len(polys) == 3: 
        #     cv2.putText(img, 'Triangle', (x, y), 
        #                 cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2) 
    
        # elif len(polys) == 4:
        #     square = True
        #     cv2.putText(image_threshed_grey, 'Yellow square!', (x, y), 
        #                 cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2) 
    
        # elif len(polys) == 5: 
        #     cv2.putText(img, 'Pentagon', (x, y), 
        #                 cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2) 
    
        # elif len(polys) == 6: 
        #     cv2.putText(img, 'Hexagon', (x, y), 
        #                 cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2) 
    
        # else: 
        #     cv2.putText(img, 'circle', (x, y), 
        #                 cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2) 
        
    if len(polys) == 4:
        square = True
        print("square!")
    elif len(polys) == 3:
        triangle = True
        print("triangle!")
    else:
        square = False
        triangle = False
        print("no square :(, # of vertices = ",len(polys))

    if square or triangle:
        #now find centroid! Use the moments function
        # M = cv2.moments(polys)
        # #to find the centroid...
        # if(M["m00"] != 0):
        #     cX = int(M["m10"]/M["m00"])
        #     cY = int(M["m01"]/M["m00"])
        #     cv2.circle(image,(cX,cY),5,(0,0,255),-1)
        #     cv2.putText(image,"yellow square!",(cX-25,cY-25),
        #     cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),2)
        # else:
        #     cX, cY = 0, 0
        cX = int(np.average(polys[:,:,0]))
        cY = int(np.average(polys[:,:,1]))
        print("centroid = ",cX,cY)

        cv2.circle(image_contours,(cX,cY),5,(0,0,255),-1)
        cv2.putText(image_contours,"yellow square!",(cX-25,cY-25),
        cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),2)

        # calculate and scale error
        k = 65
        e = int((cX - cWidth/2) * k / cWidth*2)

        # contrained motor commands
        lCmd = np.clip(k + e, -255, 255)
        rCmd = np.clip(k - e, -255, 255)

        # # if conting can be found, spin around and look 
        # if (cX == cY == 0):
        #     lCmd = -100
        #     rCmd = 100

    else:
        lCmd = 0
        rCmd = 0
        e = "inf"

    # dislay image feed
    # cv2.imshow("camera",image_dilate)
    cv2.imshow("camera",image_contours)
    cv2.waitKey(1)

    print(lCmd, rCmd, e,)
    romi.motors(sign * lCmd, sign * rCmd)
