#usoCamCv2.py

import cv2
import numpy as np

cv2.namedWindow('webCam')
cap = cv2.VideoCapture()
cap.open("http://admin:123456@pcmix.dyndns.org:8080")

#capture frame por frame
#set width
#ret = cap.set(3,480)
#set Height
#ret = cap.set(4,360)

#cv2.namedWindow('mask')
#cv2.namedWindow('res')

#definimos rango de color en hsv
bajos_rojos = np.array([49,50,50])
altos_rojos = np.array([80,100,100])



if cap.isOpened():
	ret, frame = cap.read()
else:
	ret = False
	print "problema aqui?"


while True:
	#se toma cada frame
	ret,frame = cap.read()
	#convertir de rgb a hsv
	#hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	#Threshold el hsv para obtener el color azul de la mascara
	#mask = cv2.inRange(hsv, bajos_rojos, altos_rojos)

	#bitwise and y mask
	#res = cv2.bitwise_and(frame, frame, mask = mask)

	cv2.imshow('webCam', frame)
	#cv2.imshow('mask', mask)
	#cv2.imshow('res', res)
	esc = cv2.waitKey(5) & 0xFF == 27
	if esc:
		break

cap.release()
cv2.destroyAllWindows()