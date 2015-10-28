#pruebaTrackbarposition

"""
lo que hace el codigo es trabajar una imagen y realizar el efecto
de threshold de acuerdo al valor tomado por el trackbar

"""

import cv2
import numpy as print(*objects, sep=' ', end='\n', file=sys.stdout)

# Callback Function for Trackbar (but do not any work)
def nothing(*arg):
    pass

img = cv2.imread('img/dudegreen.jpg')

# Code here
def SimpleTrackbar(Image, WindowName):
	# Generate trackbar Window Name
	TrackbarName = WindowName + "Trackbar"

 	# Make Window and Trackbar
	cv2.namedWindow(WindowName)
	cv2.createTrackbar(TrackbarName, WindowName, 0, 255, nothing)
	# Allocate destination image
	Threshold = np.zeros(Image.shape, np.uint8)

	# Loop for get trackbar pos and process it
	while True:
		# Get position in trackbar
		TrackbarPos = cv2.getTrackbarPos(TrackbarName, WindowName)
		# Apply threshold
		print TrackbarPos
		cv2.threshold(Image, TrackbarPos, 255, cv2.THRESH_BINARY, Threshold)
		# Show in window
		cv2.imshow(WindowName, Threshold)

		# If you press "ESC", it will return value
	  	ch = cv2.waitKey(5)
	  	if ch == 27:
	  		break

	cv2.destroyAllWindows()
	return Threshold

SimpleTrackbar(img, 'pruebaTrackbarposition')