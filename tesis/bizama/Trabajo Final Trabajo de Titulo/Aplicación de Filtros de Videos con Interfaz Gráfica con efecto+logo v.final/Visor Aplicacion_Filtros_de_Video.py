#!/usr/bin/env python

# Escrito por Anibal Alberto Bizama Soto

# Importamos os, que engloba funcionalidad relativa al sistema operativo;
# Tambien usamos sys para ofrecer una funcionalidad relacionada con el propio interprete de Python
import sys, os

# Importamos el modulo pygtk y le indicamos que use la version mas reciente instalada en el sistema
# (en caso de que existan varias versiones de pygtk instaladas en el sistema)
import pygtk

# Luego importamos el modulo de gtk para poder acceder a los controles de Gtk+
# Ademas gobject se debe usar ya que es una parte fundamental para Gstreamer 
# ya que se encarga de crear un ciclo o bucle en el que gst habita y hace su trabajo.
import gtk, gobject

# Se importa gst y pygst en la version 0.10 para cargarlos.
import pygst
pygst.require("0.10")
import gst

# Creamos una clase que contenga la ventana principal del programa y los
# metodos de cada una las senales
class GTK_Main:

	# Primero definimos como sera la ventana:
	def __init__(self):

		# Creando todos los objetos que nos hacen falta para la barra de menu 
		# que tiene 2 entradas (Archivo y Ayuda). Que a su vez Archivo tiene la 
		# entrada de Salir y Ayuda de Acerca de 
		mb = gtk.MenuBar()
		filem = gtk.MenuItem("Archivo")
		filemenu = gtk.Menu()
		filem.set_submenu(filemenu)
		
		# Hemos hecho que la entrada de Salir este conectada con el evento "activate"
		# que es el evento que se produce cuando seleccionamos esa entrada del menu
		# y se une a la funcion gtk.main_quit de la libreria gtk
		# que es la encargada de determinar la interfaz
		salir = gtk.MenuItem("Salir")
		salir.connect("activate", gtk.main_quit)
		filemenu.append(salir)
		mb.append(filem)

		# Creamos la entrada de menu de "Ayuda"
		helpm = gtk.MenuItem("Ayuda")
		helpmenu = gtk.Menu()
		helpm.set_submenu(helpmenu)

		# Creamos etiqueta "Acerca de"
		about = gtk.MenuItem("Acerca de")
		helpmenu.append(about)
		mb.append(helpm)

		# Se crea un dialogo "about" para mostrarlo y destruirlo
		# Debemos de crear un objeto de tipo AboutDialog()  y luego este objeto nos ofrece su API para 
		# configurar la informacion que se va a mostrar en el about
		about = gtk.AboutDialog()
		
		# Nombre del programa		
		about.set_program_name("Reproductor de Video")
		
		# Version del programa
		about.set_version("1.0")	
		
		# Tipo de copyright		
		about.set_copyright("UCT By Anibal Bizama")
		
		# Comentarios sobre el programa
		about.set_comments("VISOR DE VIDEO - ESTUDIOS VIRTUALES DE TELEVISION CON FILTROS DE VIDEO EN TIEMPO REAL")
		
		# Logo y/o foto 		
		about.set_logo(gtk.gdk.pixbuf_new_from_file("logouctici.png"))
		
		#lanza la ventana		
		about.run()

		# a continuacion se destruye el dialogo
		about.destroy()	

		# Creamos una ventana toplevel (o sea que esta al frente de todas las
        	# ventanas) llamada "ventana" y fijamos su titulo.
		ventana = gtk.Window(gtk.WINDOW_TOPLEVEL)
		ventana.set_title("Visor de Video Virtual con Filtro by Anibal Bizama")

		# Se fija la resolucion por defecto que tendra la ventana en este caso 640x480
		ventana.set_default_size(640, 480)

		# A "ventana" le conectamos una senal (destroy), esto hara que cada
       	        # vez que se presione el boton salir (la cruz del manejador de
        	# ventanas) se llamara al metodo "exit" que cerrara la ventana
		ventana.connect("destroy", gtk.main_quit, "WM destroy")
		
		# Para agregar widgets (controles como botones, etiquetas, etc.) a la
        	# ventana, primero es necesario crear contenedores como cajas que
       	        # contengan las widgets. En este caso se crea una caja vertical
		vbox = gtk.VBox()
		ventana.add(vbox)

		# Para crear un Area de Dibujo(Video) se utiliza la funcion gtk.DrawingArea()
		self.video_ventana = gtk.DrawingArea()
		vbox.add(self.video_ventana)

		# una caja horizontal que contenga los botones
		hbox = gtk.HBox()
		vbox.pack_start(hbox, False)
		
		# Dentro de la caja vertical ira nuestra barra de menu
		vbox.pack_start(mb, False)		

		hbox.set_border_width(10)
		
		# Creacion de una etiqueta
		hbox.pack_start(gtk.Label())

		# Creamos un boton "Enviar Webcam a D.V." que nos permitira enviar la senal de video
		self.boton1 = gtk.Button("Reproducir")

		# Y luego le indicamos al boton1 que cuando le hagan click emita la
        	# senal "clicked" que llamara a la funcion "start_stop"
		self.boton1.connect("clicked", self.start_stop)

		# Agregamos el boton a la caja horizontal
		hbox.pack_start(self.boton1, False)

		# Tambien creamos un nuevo boton2 "Salir", que permitira cerrar la ventana de la aplicacion
		self.boton2 = gtk.Button("Salir")

		# Luego le indicamos al boton que cuando le hagan click emita la
                # senal "clicked" que llamara a la funcion "exit"
		self.boton2.connect("clicked", self.exit)

		# Finalmente agregamos el boton.
		hbox.pack_start(self.boton2, False)

		# Luego se muestra la caja (y todo lo que contiene) en la ventana principal.
		hbox.add(gtk.Label())
	        ventana.show_all()

		# Configurando la tuberia gstreamer
		self.player = gst.parse_launch ("v4l2src device=/dev/video0  !  autovideosink")
                
		# Bus del pipeline(tuberia) para poder manejar los datos internos
		bus = self.player.get_bus()

		# Escuchar las senales en el bus del pipeline
		bus.add_signal_watch()
			
		# Permite la emision de la senal de "sync_message"
		bus.enable_sync_message_emission()

		# Los mensajes son enviados a nuestra funcion "on_message"
		bus.connect("message", self.on_message)

		# Se utiliza para conectar video a nuestra aplicacion
		bus.connect("sync-message::element", self.on_sync_message)

	def start_stop(self, w):
		# Se ejecuta al hacer click sobre el boton "Reproducir"
		if self.boton1.get_label() == "Reproducir":
			self.boton1.set_label("Parar")
			self.player.set_state(gst.STATE_PLAYING)
		
		else:
			self.player.set_state(gst.STATE_NULL)
			self.boton1.set_label("Reproducir")

	# Funcion para salir de la ventana
	def exit(self, widget, data=None):
		gtk.main_quit()

	def on_message(self, bus, message):
		# Es una retrollamada para los mensajes del bus del pipeline
		t = message.type
		if t == gst.MESSAGE_EOS:
			self.player.set_state(gst.STATE_NULL)
			self.boton1.set_label("Reproducir")
		elif t == gst.MESSAGE_ERROR:
			err, debug = message.parse_error()
			print "Error: %s" % err, debug
			self.player.set_state(gst.STATE_NULL)
			self.boton1.set_label("Reproducir")

	def on_sync_message(self, bus, message):
		if message.structure is None:
			return
		message_name = message.structure.get_name()
		if message_name == "prepare-xwindow-id":
			# Asignando el visor
			imagesink = message.src
			imagesink.set_property("force-aspect-ratio", True)
			imagesink.set_xwindow_id(self.video_ventana.window.xid)


# Iniciamos la clase.
GTK_Main()

# iniciamos los threads, para indicarle a la aplicacion que se van a usar hilos en la interfaz grafica
gtk.gdk.threads_init()

# Ademas iniciamos el metodo gtk.main, que genera un ciclo que se utiliza
# para recibir todas las senales emitidas por los botones y demas widgets.
gtk.main()


