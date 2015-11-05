# -*- coding: utf-8 -*-
#detect_chroma
#chroma sin openCV

from PIL import Image
from ImageChops import subtract
import numpy as np
import math
import cv2
#import ajustarImagen


def greenScreen(imgFg, imgBg, output='img/imageTest.png', keyColor = None, tolerance = None):
	img = ajustarImagen(imgFg, imgBg)
	#se abre un archivo
	img_fg = img.convert('YCbCr')#Image.open(img).convert('YCbCr')
	img_bg = Image.open(imgBg).convert('RGB')

	#se establece colores a usar
	if keyColor == None:
		keyColor = img_fg.getpixel((1,1))

	if tolerance == None:
		tolerance = [50,130]

	[key_g, key_b, key_r] = keyColor
	[tolerance_a, tolerance_b] = tolerance

	print "keyColor: ", keyColor
	print "tolerance: ", tolerance

	#se obtienen las dimenciones
	(x,y) = img_fg.size
	print "tamaño img_fg", (x, y)

	img_bg.size = (x,y)
	(w, q) = img_bg.size
	print "tamaño img_bg", (w, q)
	
	#crear un array a partir de la imagen
	foreground = np.array(img_fg.getdata())

	#vectorizar funcion de maskara
	mask = np.vectorize(colorClose)

	#se genera la maskara
	a_mask = mask(foreground[:,1],foreground[:,2], key_b,key_r,tolerance_a,tolerance_b)

	#se crea dimenciones de mascara y imagen original
	a_mask.shape = (y,x) #crea toda la region que es verde y la coloca en negro

	#convertir el array a imagen
	mask_img = Image.fromarray(np.uint8(a_mask))
	
	#maskara invertida con extremos
	mask_img_inv = Image.fromarray(np.uint8(225-225*(a_mask)))

	#generar imagenes para la mascara de color
	colorMask = Image.new('RGB',(x,y), tuple([0,0,0]))
	allGreen = Image.new('YCbCr',(x,y), tuple(keyColor))

	#creando el color de la mascara verde
	colorMask.paste(allGreen, mask_img_inv)

	#convertir la imagen a RGB 
	img_fg = img_fg.convert('RGB')

	#sustraer verdes de la entrada
	cleaned = subtract(img_fg, colorMask)

	#pegar fondo de primer plano sobre fondo enmascarado
	img_bg.paste(cleaned, mask_img)

	#mostrar imagen final
	#img_bg.show()

	#guardar 
	img_bg.save(output,"PNG")

def colorClose(Cb_p,Cr_p, Cb_key, Cr_key, tola, tolb):
    temp = math.sqrt((Cb_key-Cb_p)**2+(Cr_key-Cr_p)**2)
    if temp < tola:
        z= 0.0
    elif temp < tolb:
        z= ((temp-tola)/(tolb-tola))
    else:
        z= 1.0
    return 255.0*z 

def ajustarImagen(imgFg, imgBg):
	img_fg = cv2.imread(imgFg)
	img_bg = cv2.imread(imgBg)

	size_bg = img_bg.shape[:2] #obtenemos el ancho largo y canal? de la imagen
	size_fg = img_fg.shape[:2]#obtenemos el ancho largo y canal? de la imagen
	
	#se muetsran imagnes con tamaño normal
	#cv2.imshow("imagen1", img_bg)
	#cv2.imshow('imagen2', img_fg)

	print "tamaño frente: ",size_fg
	print "tamaño bg: ",size_bg

	(x,y) = size_bg
	#re escalar una imagen
	if size_fg > size_bg:
		img_fg2 = cv2.resize(img_fg, (y,x))
		print "tamaño nuevo fg ", img_fg2.shape
		cv2.imshow('tamaño nuevo', img_fg2)	

	ifg2 = Image.fromarray(img_fg2,'RGB') #pasar de cv2 a PIL.Image
	ifg2.show()
	print "-----------------> ",type(img_fg2)
	#img2r = Image.merge('RGB', (ifg2,ifg2,ifg2))
	#img2r.show()
	
	return ifg2



if __name__=='__main__':
	greenScreen("img/dudegreen.jpg", "img/imagen.png")

	esc = cv2.waitKey(0) & 0XFF
	if esc == 27:
		cv2.destroyAllWindows()