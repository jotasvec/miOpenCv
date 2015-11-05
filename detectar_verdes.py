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
import cv2
import numpy as np
#se abre la camara y se guardan los datos leidos en captura

captura = cv2.VideoCapture(0)
background = cv2.imread('img/imagen.png')

#se crea un bucle infinito
while(1):
	#se leen los frames y se guardan en imagen
	ret, imagen = captura.read()
	#voltea la imagen
	imagen = cv2.flip(imagen,1,imagen)
	#se cambia la imagen RGB a HSV de esta forma es mas facil analizar la imagen
	hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
#se necesita crear 2 arrays para guardar el rango de valores del verde detectados los topes sera los limetes de verdes mas claros a los mas oscuros
	#verdes oscuros
	verdes_bajos = np.array([49,50,50])
	#verdes mas claros
	verdes_altos = np.array([80,255,255])

#se crea una mascara de imagen la cual invertira los colores y dejando blanco todos los pixeles verdes y negro todo lo que no sea verde
#crea una imagen blanco y negro poniendo en blanco todo lo verde
	mask = cv2.inRange(hsv, verdes_bajos, verdes_altos)

#se elimina el ruido de la imagen para dejarla mas definida
	kernel = np.ones((5,5),np.uint8)

	#refina el ruido externo a las regiones blancas correspondientes
	#primero se aplica un poco de erosion para reducir las zonas en con blanco

	# refina el ruido externo en regiones negras donde no corresponden que hayan puntos blancos
	mask = cv2.erode(mask, kernel,iterations=2)
	mask = cv2.dilate(mask, kernel,iterations=2)
	mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN,kernel)
	ret, mask = cv2.threshold(mask, 170,255,cv2.THRESH_BINARY)
	mask = cv2.GaussianBlur(mask, (5,5),0)

	#se se invierte la mascara para mostrar los verdes en negro con la aplicacion de filtros

	#se produce una segunda mascara para luego utilizarla con el fondo
	ret, mask = cv2.threshold(mask, 170,255,cv2.THRESH_BINARY)
	mask_inv = cv2.bitwise_not(mask)
	mask_inv = cv2.GaussianBlur(mask_inv, (5,5),0)
	mask_inv = cv2.morphologyEx(mask_inv, cv2.MORPH_OPEN,kernel)
	

	size_bg = background.shape[:2]
	size_ibi = mask_inv.shape[:2]

	(x,y) = size_ibi
	if size_bg != size_ibi:
		background = cv2.resize(background,(y,x))
	#se crea la maskra de roi (region de interes)
	roi= cv2.bitwise_and(background,background, mask=~mask_inv)
	
	#mascara final de la imagen de webcam
	mask = cv2.bitwise_and(imagen, imagen, mask=~mask)
	


	final = cv2.add(roi,mask)
	#se muetsran 2 ventanas, la primera es la imagen original luego la en blanco y negro
	
	#muestra imagen normal
	cv2.imshow('camara', imagen)
	#muestra resultado con chroma
	cv2.imshow('maskara', final)



#para cerrar el programa usando escape

	tecla = cv2.waitKey(5) & 0xFF
	if tecla == 27:
		break

captura.release()
cv2.destroyAllWindows()