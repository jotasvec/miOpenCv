#usoCamv.2.py
# -*- coding: utf-8 -*-


#librerias para manejar el S.O
import sys, os

#se importa los modulos de gtk y pygtk
# previamente se instalan las librerias de gstreamer si es necesario

import pygtk
import gtk, gobject

#se cargan gstreamer "gst" y pygst
import pygst
pygst.require("0.10")
import gst

class Main:
	def __init__(self):
		#agregamos la ventana de inicio (es por que esta simpatica)
		


		fScreen = gtk.AboutDialog()

		fScreen.set_program_name("nombre del programa aqui")#nombre del programa

		fScreen.set_version("aqui la version 0.1") #version del programa

		fScreen.set_copyright("escrito por bla bla bla")#pa que quiero esto? solo derechos? de copyrigth

		fScreen.set_comments("comentarios sobre el programa - Estudios Virtuales")

		#logo y/o foto
		#fScreen.set_logo() -> esto aun no

		#mostrar la ventana
		fScreen.run()
		#se destruye la ventana para dar paso a la nueva
		fScreen.destroy()

		#se crea el mainframe
		mainFrame = gtk.Window(gtk.WINDOW_TOPLEVEL)
		mainFrame.set_title("webCam Qla") #titulo de la barra qla

		#tamaño de la venta
		mainFrame.set_default_size(640,480)
		mainFrame.connect("destroy", gtk.main_quit)


		#agregar botones qlos despues primero la imagen

		#se crea una area(box o caja) de dibujo para agregar elementos a la ventana (vbox)
		vbox= gtk.VBox() #vertical Box-> vbox


		#agregar area de imagen de video
		self.cam_screen = gtk.DrawingArea()

		vbox.add(self.cam_screen)

		#se muestra el mainframe
		mainFrame.show_all()

		#configurando el pipeline(tuberia) para el gstreamer 
		self.player = gst.parse_launch("v4l2src device=/dev/video0 ! autovideosink") #link para cargar la camara
		self.player.set_state(gst.STATE_PLAYING)
		
		#bus de datos para manejar el pipeline
		dataBus = self.player.get_bus()

		#escuchar señales
		dataBus.add_signal_watch()

		dataBus.enable_sync_message_emission()#envio de señales "sync_message"

		dataBus.connect("message", self.on_message)

		dataBus.connect("sync-message::element", self.on_sync_message)

	def salir(self):
		gtk.main_quit()

	def on_message(self, dataBus, message):
		t = message.type

		if t == gst.MESSAGE_EOS:
			self.player.set_state(gst.STATE_NULL)
		elif t==gst.MESSAGE_ERROR:
			err,debug = message.parse_error()
			print "Error: %s"%err, debug
			self.player.set_state(gst.STATE_NULL)

	def on_sync_message(self, bus, message):
		if message.structure is None:
			return
		message_name = message.structure.get_name()
		if message_name == "prepare-xwindow-id":
			# Asignando el visor
			imagesink = message.src
			imagesink.set_property("force-aspect-ratio", True)
			#imagesink.set_xwindow_id(self.cam_screen.window)

start = Main()

gtk.gdk.threads_init()
gtk.main()



