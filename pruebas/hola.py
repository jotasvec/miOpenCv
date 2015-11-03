#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import sys
# from Tkinter import *

# root= Tk()
# root.title("probando...")

# #ventana principal tipo frame
# vPrincipal= Frame(root, bg="blue")
# vPrincipal.grid(padx=(50,50),pady=(50,50))
# vPrincipal.columnconfigure(0,weight=1)
# vPrincipal.rowconfigure(0,weight=1)


# etiqueta= Label(vPrincipal, text="hola mundo mundial", bg="red")
# etiqueta.grid(column=1,row=1)

# # f = Frame(root, width=1000, height=10, bg="blue")
# # f.pack(fill=X, expand=True)


# # l = Label(f, text="joder la ostia tio", width=50, height=10, bg="red", fg="white")
# # l.pack()

# root.mainloop()


####################################################################################################

# from Tkinter import *
# import time

# def minimizar():
# root.iconify() #minimiza la pantalla
# time.sleep(5) #tiempo
# root.deiconify() #desminimiza la pantalla

# def newScreen():
# nueva_ventana = Toplevel(root)
# nueva_ventana.transient(root) #esto hace que la ventana siga a la ventana padre

# def cerrar():
# sys.exit(0)


# root = Tk()

# #boton que minimiza
# btn_minimiza = Button(root, text="minimizar", command=minimizar)
# btn_minimiza.pack()

# btn_newScreen = Button(root, text="abrir ventana", command=newScreen)
# btn_newScreen.pack()

# #boton de cierre
# btn_cerrar = Button(root,text="cerrar",command=cerrar)
# btn_cerrar.pack()

# root.mainloop()

####################################################################################################
