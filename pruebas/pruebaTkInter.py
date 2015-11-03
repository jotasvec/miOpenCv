#!/usr/bin/env python
# -*- coding: utf-8 -*-


#se importa tkinter para entorno grafico
from Tkinter import *
import sys


def cerrarTodo(): #para cerrar la ventana
	sys.exit(0)



#abre una nueva ventana
def newScreen():
	screen_wc=Toplevel(root)
	screen_wc.transient(root) #esto hace que la ventana siga a la ventana padre
	hola=Label(screen_wc,text="nueva ventana para webcam")
	hola.place(in_=screen_wc,x=100,y=10)

	screen_wc.geometry("400x400") #tamano de la ventana
	screen_wc.title("ver cam") # titulo de arriba
	 #para personalizar bg= backGround otra forma seria screen['bg']='blue'

	#agregar imagen

	lbl_img = Label(screen_wc, image=img1)
	lbl_img.place(in_=screen_wc, x=50, y =50)

	btn= Button(screen_wc, text="cerrar", command=screen_wc.destroy)
	btn.place(in_=screen_wc, x=200,y=350, width="100", height="30") #posicionamos y damos tamano

############################################################################################


root= Tk() #crea la ventana
#ventana general
root.geometry("500x500") #tamano de la ventana
root.title("y empezamos") # titulo de arriba
root.config(bg="blue") #para personalizar bg= backGround otra forma seria root['bg']='blue'

#etiqueta Label
etiqueta = Label(root, text="wenos dias, wenas tardes")
etiqueta.place(x=10,y=10)
#etiqueta.pack(expand, fill, padx o pady ->separacion,etc) #posicion
#etiqueta.grid(row=x,column=x, rowspan, sticky) -> posicion


#btn de para abrir la ventana
btn_nS= Button(root, text="webcam",command= newScreen)
btn_nS.place(in_=root,x=100,y=100)


#boton de cerrado
btn= Button(root, text="cerrar", command=cerrarTodo)
btn.place(in_=root, x=200,y=450, width="100", height="30") #posicionamos y damos tamano
#btn.pack(expand, fill, padx o pady ->separacion, etc) #posicion
#btn.grid(row=x,column=x,  rowspan, sticky)->posicion

img1 = PhotoImage(file="img/imagen.png", width= 250, height=250)


root.mainloop() #ejecuta el programa
