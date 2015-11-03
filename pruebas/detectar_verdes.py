"""
para reconocer y marcar un objeto de un color determinado.

	1. capturar una imagen con la camara
	2. convertir la imagen de rgb a HSV
	3. buscar el color deseado
	4. eliminar el ruido
	5.mostrar la imagen 
"""

#primero para capturar la imagen
#se cargan las librerias para capturar imagen
import cv2 #libreria de opencv
import numpy as np #libreria numpy

captura = cv2.VideoCapture(0) #se abre la camara y se guardan los datos leidos en captura

#segundo, se convierte la imagen

#se crea un bucle infinito

while(1):
	ret, imagen = captura.read() #se leen los frames y se guardan en imagen
	hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV) #se cambia la imagen RGB a HSV de esta forma es mas facil analizar la imagen

#tercero, se buscan los lados verdes

#se necesita crear 2 arrays para guardar el rango de valores del verde detectados los topes sera los limetes de verdes mas claros a los mas oscuros

	verdes_bajos = np.array([49,50,50]) #verdes oscuros
	verdes_altos = np.array([80,255,255]) #verdes mas claros

#se crea una mascara de imagen la cual invertira los colores y dejando blanco todos los pixeles verdes y negro todo lo que no sea verde

	mask = cv2.inRange(hsv, verdes_bajos, verdes_altos) #crea una imagen blanco y negro poniendo en blanco todo lo verde

#cuarto, se elimina el ruido de la imagen para dejarla mas definida
	
	kernel = np.ones((7,7), np.uint8)
	
	# refina el ruido externo a las regiones blancas correspondientes
	#primero se aplica un poco de erosion para reducir las zonas en con blanco

	# refina el ruido externo a las regiones blancas correspondientes
	opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
	cv2.imshow('img opening', opening)

	#se produce dilatacion para mejorar los bordesen el cambio de blanco a negro en la maskara 
	dilation = cv2.dilate(opening,kernel, iterations=1)

	blur = cv2.GaussianBlur(dilation, (5,5),0)
	ret1, thBlur = cv2.threshold(blur, 0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	cv2.imshow('img blur gaussian effect',thBlur)

	#se se invierte la mascara para mostrar los verdes en negro con la aplicacion de filtros 
	mask2 = cv2.bitwise_and(imagen, imagen, mask= ~thBlur)

#se muetsran 2 ventanas, la primera es la imagen original luego la en blanco y negro
	cv2.imshow('mask2', mask2)
	cv2.imshow('camara', imagen)

#para cerrar el programa usando escape

	tecla = cv2.waitKey(5) & 0xFF
	if tecla == 27:
		break


cv2.destroyAllWindows()

#revisar bien el programa como funciona y complementarlo.