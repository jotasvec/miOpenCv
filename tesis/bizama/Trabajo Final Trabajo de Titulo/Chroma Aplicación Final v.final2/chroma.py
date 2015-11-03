#!/usr/bin/env python
import Image
from ImageChops import subtract
import numpy
import math
import cv2 

def GreenScreen(infile, inbg ,outfile='output2.png', keyColor=None, tolerance = None):

    #Abriendo archivos
    inDataFG = Image.open(infile).convert('YCbCr')
    BG = Image.open(inbg).convert('RGB')

    #Se establecen los valores que se van a ocupar
    if keyColor == None:keyColor = inDataFG.getpixel((1,1))
    if tolerance == None: tolerance = [50,130]
    [Y_key, Cb_key, Cr_key] = keyColor
    [tola, tolb]= tolerance

    #Obteniendo las dimensiones
    (x,y) = inDataFG.size

    #Crea array a partir de la imagen
    foreground = numpy.array(inDataFG.getdata()) 

    #Vectorizar funcion de enmascaramiento
    maskgen = numpy.vectorize(colorclose)

    #Generando la mascara
    alphaMask = maskgen(foreground[:,1],foreground[:,2] ,Cb_key, Cr_key, tola, tolb)


    #Crea dimensiones de mascara de la imagen original
    alphaMask.shape = (y,x)

    #Convertir el array a imagen
    imMask = Image.fromarray(numpy.uint8(alphaMask))

    #Creando la mascara invertida con extremos
    invertMask = Image.fromarray(numpy.uint8(255-255*(alphaMask/255)))

    #Generar imagenes para la mascara de color
    colorMask = Image.new('RGB',(x,y),tuple([0,0,0]))
    allgreen = Image.new('YCbCr',(x,y),tuple(keyColor))

    #Creando el color de la mascara verde en valores de verde en la imagen
    colorMask.paste(allgreen,invertMask)
    #Convertir la imagen de entrada a RGB para facilitar el trabajo
    inDataFG.show('antes')
    inDataFG = inDataFG.convert('RGB')   
    inDataFG.show('despues')
    #Sustraer verdes de la entrada
    cleaned = subtract(inDataFG,colorMask) 

    #Pegar el fondo de primer plano sobre fondo enmascarado
    BG.paste(cleaned,imMask)

    #Mostrar la imagen limpiada
    BG.show() #show()

    #Guardar la imagen limpiada
    BG.save(outfile, "PNG") 


def colorclose(Cb_p,Cr_p, Cb_key, Cr_key, tola, tolb):
    temp = math.sqrt((Cb_key-Cb_p)**2+(Cr_key-Cr_p)**2)
    if temp < tola:
        z= 0.0
    elif temp < tolb:
        z= ((temp-tola)/(tolb-tola))
    else:
        z= 1.0
    return 255.0*z


if __name__ == '__main__':
 
    GreenScreen('testimg2.png','testbg4.png')
    esc = cv2.waitKey(0) & 0XFF
    if esc == 27:
        cv2.destroyAllWindows()