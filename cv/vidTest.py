from picamera2 import Picamera2, Preview
from matplotlib import pyplot as plt
import time

picam2 = Picamera2()
config = picam2.create_preview_configuration()
picam2.configure(config)

picam2.start_preview(Preview.QTGL)
picam2.start()
while True:
	time.sleep(1)
#array = picam2.capture_array("main")
#plt.imshow(array, interpolation='nearest')
#plt.show()
