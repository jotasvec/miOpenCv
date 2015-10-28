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
	_, imagen = captura.read() #se leen los frames y se guardan en imagen
	hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV) #se cambia la imagen RGB a HSV de esta forma es mas facil analizar la imagen

#tercero, se buscan los lados verdes

#se necesita crear 2 arrays para guardar el rango de valores del verde detectados los topes sera los limetes de verdes mas claros a los mas oscuros

	verdes_bajos = np.array([49,50,50]) #verdes oscuros
	verdes_altos = np.array([80,255,255]) #verdes mas claros

#se crea una mascara de imagen la cual invertira los colores y dejando blanco todos los pixeles verdes y negro todo lo que no sea verde

	mask = cv2.inRange(hsv, verdes_bajos, verdes_altos) #crea una imagen blanco y negro poniendo en blanco todo lo verde

#cuarto, se elimina el ruido de la imagen para dejarla mas definida

	moments = cv2.moments(mask) # esta funcion da como salida un diccionario del cual se necita el valor 'm00' 
	area = moments['m00'] #para ver como queda ->print area

#para eliminar el ruido, leer manual

	if(area > 20000000):
		#se buscan los centros
		x = int(moments['m10']/moments['m00'])
		y = int(moments['m01']/moments['m00'])

		#se escriben los valores de los centros de x e y

		print "x = ", x
		print "y = ", y

		#se dibuja en el centro un rectangulo rojo
		cv2.rectangle(imagen, (x,y),(x+2,y+2), (0,0,255), 2) #revisar que pasa con esto

#se muestran las imagenes

#se muetsran 2 ventanas, la primera es la imagen original luego la en blanco y negro

	cv2.imshow('mask', mask)
	cv2.imshow('camara', imagen)

#para cerrar el programa usando escape

	tecla = cv2.waitkey(5) & 0xFF
	if tecla == 27:
		break
cv2.destroyAllWindows()

#revisar bien el programa como funciona y complementarlo.