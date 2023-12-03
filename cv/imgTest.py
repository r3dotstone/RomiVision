import cv2 
import numpy as np
from matplotlib import pyplot as plt 
  
# reads an input image 
img = cv2.imread("./pics/yellowsquare.jpg",0) 
  
# find frequency of pixels in range 0-255 
thresh = 250e3
while True:
    histr = cv2.calcHist([img],[0],None,[256],[0,256]) 
    histrGtThresh = histr[histr > thresh]
    if (histr.size/histrGtThresh.size) > 20:
        print("goin forward...")
# show the plotting graph of an image 
plt.plot(histr)
<<<<<<< HEAD:cvTest.py
plt.show()
=======
print(histr)
plt.show()
plt.savefig('testHistr.png')

#TEST
>>>>>>> 99cf75ae6aefb172c003a1ec9034aa3a59ac742c:cv/imgTest.py
