#!/usr/bin/env python
# -*- coding: utf-8 -*-
# coding=utf-8
#faceDetection.py

import cv2
import numpy as np

cap = cv2.VideoCapture(0)
bgSuntractor = cv2.createBackgroundSubtractorMOG2()
kernel = np.ones((5,5),np.uint8)
print "fps->", cap.get(cv2.CAP_PROP_FPS)
cap.set(cv2.CAP_PROP_FPS, 50)
# while True:
# 	#se toma cada frame
# 	ret, frame = cap.read()

# 	mask = bgSuntractor.apply(frame)
# 	mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

# 	cv2.imshow('mask', mask)
# 	cv2.imshow('webCam', frame)

# 	esc = cv2.waitKey(5) & 0xFF == 27
# 	if esc:
# 		break

# cap.release()
# cv2.destroyAllWindows()

while True:
	#se toma cada frame
	ret, frame = cap.read()


	mask = np.zeros(frame.shape[:2], np.uint8)

	bgdModel = np.zeros((1,65),np.float64)
	fgdModel = np.zeros((1,65),np.float64)

	rect = (50,50,450,290)
	cv2.grabCut(frame, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)

	mask = np.where((mask==2) | (mask==0),0,1).astype('uint8')

	mask = frame*mask[:,:,np.newaxis]

	cv2.imshow('mask', mask)
	cv2.imshow('webCam', frame)

	esc = cv2.waitKey(5) & 0xFF == 27
	if esc:
		break

cap.release()
cv2.destroyAllWindows()