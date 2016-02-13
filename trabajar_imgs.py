# -*- coding: utf-8 -*-

#resize a image
import cv2

#se abre una imagen

img_fg = cv2.imread("img/dudegreen.jpg")
img_bg = cv2.imread("img/imagen.png")

size_bg = img_bg.shape[:2]   # obtenemos el ancho largo y canal? de la imagen
size_fg = img_fg.shape[:2]

cv2.imshow("imagen1", img_bg)
cv2.imshow('imagen2', img_fg)

print "tamaño frente: ",size_fg
print "tamaño bg: ",size_bg

(x,y) = size_bg
#re escalar una imagen
if size_fg > size_bg:
	img_fg2 = cv2.resize(img_fg, (y,x))
	print "tamaño nuevo fg ", img_fg2.shape[:2]
	cv2.imshow('tamaño nuevo', img_fg2)

#img_fg2 = img_fg.resize((width,height))

#print "tamaño frente2: ",img_fg2.size
#print "tamaño bg2: ",img_bg2.size

#cv2.imshow("imagenes2", np.hstack([img_bg2, img_fg2]))


esc = cv2.waitKey(0) & 0XFF
if esc == 27:
	cv2.destroyAllWindows()