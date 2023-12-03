# importing required libraries of opencv 
import cv2 
# import sys
# sys.path.append("/pics")

# importing library for plotting 
from matplotlib import pyplot as plt 
  
# reads an input image 
img = cv2.imread("test1.jpg",0) 
  
# find frequency of pixels in range 0-255 
histr = cv2.calcHist([img],[0],None,[256],[0,256]) 
thresh = 2e5
# show the plotting graph of an image 
plt.plot(histr)
print(histr)
plt.show()
plt.savefig('testHistr.png')

#TEST
