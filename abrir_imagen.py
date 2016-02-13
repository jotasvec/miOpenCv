import cv2
import sys
import numpy as np


#esto sirve para cargar una imagen
img = cv2.imread('dudegreen.jpg')


cv2.imshow('hey dude', img) #se muestra la pestania hey dude

#rango de verde para eliminar verdes
verdes_bajos = np.array([49,50,50])
verdes_altos = np.array([80,255,255])

#imagen a HSV
img_hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
cv2.imshow('con hsv', img_hsv) #muestra la imagen con hsv aplicado

#se crea la mascara para sacar los verdes
mask = cv2.inRange(img_hsv, verdes_bajos, verdes_altos)
#muestra quitando los verdes
cv2.imshow('sin verde img', mask)#muestra la pestania con la maskara aplicada

#me identifica el color y lo sobre la maskara con el color identificado por sobre la imagen original
res = cv2.bitwise_not(mask) #cv2.bitwise_and(mask, mask, mask= img)
cv2.imshow('a ved a ved', res) #deberia mostrar el fondo blaco con la imagen del personaje

mask_color = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR)
cv2.imshow('mask color', mask_color)#cambio de color




k = cv2.waitKey(0) & 0XFF
if k == 27:
	cv2.destroyAllWindows()
