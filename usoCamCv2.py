#usoCamCv2.py

import cv2

cv2.namedWindow('webCam')
cap = cv2.VideoCapture()
cap.open("img/bg.avi")


if cap.isOpened():
	ret, frame = cap.read()
else:
	ret = False
	print "problema aqui?"


while True:
	#se toma cada frame
	ret,frame = cap.read()

	cv2.imshow('webCam', frame)

	esc = cv2.waitKey(5) & 0xFF == 27
	if esc:
		break

cap.release()
cv2.destroyAllWindows()