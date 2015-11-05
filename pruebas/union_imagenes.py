#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
jugando con union de imagen
primero -> lo comentado al final es la union de las imagenes en una sobre otra, 
el logo de opencv se pone encima de otra imagen

el codigo que no esta comentado es una prueba usando trackbars mostrando la union
de dos imagenes con transparencia, el trackbar maneja la transparencia de ambas imagenes.
por ende una se sobrepone a otra de acuerdo a su transparencia
con el comando 
	dst= cv2.addWeighted(img1, 0.7, img2, 0.3, 0)
se logra la union de las 2 imagenes
"""
import cv2

def nothing(x):
	pass

img1= cv2.imread('img/imagen.png')
img2= cv2.imread('img/img2.png')

#dst= cv2.addWeighted(img1, 0.7, img2, 0.3, 0)

cv2.imshow('imagen', img1)
cv2.imshow('imagen2', img2)


#namedwindows
cv2.namedWindow('pruebaConTrackbar')
#poner el logo sobre la imagen
filas, columnas, canales= img2.shape
roi = img1[0:filas, 0:columnas]
cv2.imshow('roi', roi)

#cramos un trackbar para modificar la opacidad de las imagenes

cv2.createTrackbar('roi', 'pruebaConTrackbar', 0, 100, nothing)
cv2.createTrackbar('img2', 'pruebaConTrackbar', 0, 100, nothing)


while True:
	valorTb1 = float(cv2.getTrackbarPos('roi', 'pruebaConTrackbar'))/100	
	valorTb2 = float(cv2.getTrackbarPos('img2', 'pruebaConTrackbar'))/100
	
	print "valor1 = ", valorTb1
	print "valor2 = ", valorTb2

	dst1= cv2.addWeighted(roi, valorTb1, img2, valorTb2 , 0)
	cv2.imshow('dst1', dst1)


	k = cv2.waitKey(5)
	if k == 27:
		break

"""
#ahora se crea la mascara del lofo y su inverso de la mascara
img2gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
mask_inv = cv2.bitwise_not(mask)

cv2.imshow('mask', mask)
cv2.imshow('mask_inv', mask_inv)

#ahora black out the area del logo en roi
img1_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
cv2.imshow('img1_bg', img1_bg)

#se toma la region del logo
img2_fg = cv2.bitwise_and(img2, img2, mask= mask)
cv2.imshow('img2_fg', img2_fg)

#se coloca el logo en roi
dst = cv2.add(img1_bg, img2_fg)
img1[1:filas, 1:columnas] = dst

cv2.imshow('img1 final', img1)"""


cv2.destroyAllWindows()
