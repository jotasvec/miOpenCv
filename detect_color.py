#detect color

import numpy as np
import cv2

#se carga la imagen

img = cv2.imread("img/img2.png")

#rango = [([17,15,100],[50,56,200])]
#rango = [([49,50,50],[80,255,255])]
"""
basicamente lo que hace esto es buscar la cantidad de numeros perteneciente en
un rango de color para luego destacarlo
"""
#for (lower, upper) in rango:
while True:
	#se crean arrais con numpy para el rango
	lower = np.array([7,5,100])  # (lower, dtype="uint8")
	upper = np.array([49,50,50])  # (upper, dtype="uint8")

	#se buscan los colores con un rango especifico

	mask = cv2.inRange(img, lower, upper)
	output = cv2.bitwise_and(img, img, mask=mask)

	#se muestra la imagen
	cv2.imshow("imagen", np.hstack([img, output]))

	esc = cv2.waitKey(5) & 0XFF
	if esc == 27:
		break

cv2.destroyAllWindows()