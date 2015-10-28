#trackbar
"""
prueba para ocupar el createTrackbar() y getTrackbarPos()
"""
import cv2
import numpy as np

def nothing(x):
	pass


#se crea una imagen en negra en una ventana
img = np.zeros([300,512,3], np.uint8)
cv2.namedWindow('image')

#crea track bar para el cambio de color

cv2.createTrackbar('R','image', 0,255,nothing)
cv2.createTrackbar('G','image', 0,255,nothing)
cv2.createTrackbar('B','image', 0,255,nothing)


#se crea switch para prender y apagar 

switch = '0 : OFF \n1 : ON'
cv2.createTrackbar(switch, 'image', 0, 1,nothing)

while (1):
	cv2.imshow('image',img)
	k = cv2.waitKey(1) & 0XFF
	if k == 27:
		break

	#se toma la pocicion de los 4 trackbars

	r = cv2.getTrackbarPos('R', 'image')
	g = cv2.getTrackbarPos('G', 'image')
	b = cv2.getTrackbarPos('B', 'image')
	s = cv2.getTrackbarPos(switch, 'image')

	if s==0:
		img[:] = 0
	else:
		img[:] = [b,g,r]

cv2.destroyAllWindows()
