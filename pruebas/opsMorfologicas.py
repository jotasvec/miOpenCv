#opsMorfologicas.py

import cv2
import numpy as np

img = cv2.imread('img/j.png')

#cv2.imshow('img j original', img)

kernel = np.ones((5,5), np.uint8)
#erosion
erosion = cv2.erode(img, kernel, iterations=1)
cv2.imshow('original vs erosion', np.hstack([img, erosion]))

#dilatacion
dilatacion = cv2.dilate(img, kernel, iterations=1)
cv2.imshow('original vs dilatacion', np.hstack([img, dilatacion]))

#para manejar el ruido ver opening y closing

#en caso de usar opening
opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

#en caso de usar closing
closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)


tecla = cv2.waitKey(0) & 0xFF
if tecla == 27:
	cv2.destroyAllWindows()
