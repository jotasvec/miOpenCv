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
		about.set_program_name("Estudios Virtuales - Filtros de Video")
		
		# Version del programa
		about.set_version("1.0")	
		
		# Tipo de copyright		
		about.set_copyright("UCT By Anibal Bizama")
		
		# Comentarios sobre el programa
		about.set_comments("ESTUDIOS VIRTUALES DE TELEVISION CON FILTROS DE VIDEO EN TIEMPO REAL")
		
		# Logo y/o foto 		
		about.set_logo(gtk.gdk.pixbuf_new_from_file("logouctici.png"))
		
		#lanza la ventana		
		about.run()

		# a continuacion se destruye el dialogo
		about.destroy()		

		# Creamos una ventana toplevel (o sea que esta al frente de todas las
        	# ventanas) llamada "ventana" y fijamos su titulo.
		ventana = gtk.Window(gtk.WINDOW_TOPLEVEL)
		ventana.set_title("Filtros de Video en Tiempo Real by Anibal Bizama")
		
		# Se fija la resolucion por defecto que tendra la ventana en este caso 450x500
		ventana.set_default_size(450, 550)

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
		
		# una caja horizontal que contenga fondo de aplicacion y/o botones
		hbox = gtk.HBox()
		vbox.pack_start(hbox, False)
		
		# Dentro de la caja vertical ira nuestra barra de menu y botones
		vbox.pack_start(mb, False)
		
		# Fijamos el grosor del borde de ventana
		hbox.set_border_width(10)

		# Creacion de una etiqueta
		hbox.pack_start(gtk.Label())

		# Creamos los botones "Enviar Webcam a D.V." que nos permitira enviar la senal de video con filtros de video
		self.boton0 = gtk.Button("Enviar Webcam a Dispositivo Virtual (Filtro 0: Normal+Logo)")
		self.boton1 = gtk.Button("Enviar Webcam a Dispositivo Virtual (Filtro 1: Bulge+Logo)")
		self.boton2 = gtk.Button("Enviar Webcam a Dispositivo Virtual (Filtro 2: Square+Logo)")
		self.boton3 = gtk.Button("Enviar Webcam a Dispositivo Virtual (Filtro 3: Fisheye+Logo)")
		self.boton4 = gtk.Button("Enviar Webcam a Dispositivo Virtual (Filtro 4: Kaleidoscope+Logo)")
		self.boton5 = gtk.Button("Enviar Webcam a Dispositivo Virtual (Filtro 5: Marble+Logo)")
		self.boton6 = gtk.Button("Enviar Webcam a Dispositivo Virtual (Filtro 6: Normal+Texto)")
		self.boton7 = gtk.Button("Enviar Webcam a Dispositivo Virtual (Filtro 7: Mirror+Logo)")
		self.boton8 = gtk.Button("Enviar Webcam a Dispositivo Virtual (Filtro 8: Pinch+Logo)")
		self.boton9 = gtk.Button("Enviar Webcam a Dispositivo Virtual (Filtro 9: Sphere+Logo)")
		self.boton10 = gtk.Button("Enviar Webcam a Dispositivo Virtual (Filtro 10: Square+Logo)")
	        self.boton11 = gtk.Button("Enviar Webcam a Dispositivo Virtual (Filtro 11: Stretch+Logo)")  
	        self.boton12 = gtk.Button("Enviar Webcam a Dispositivo Virtual (Filtro 12: Tunel+Logo)")   
		self.boton13 = gtk.Button("Enviar Webcam a Dispositivo Virtual (Filtro 13: Twirl+Logo)")    
		self.boton14 = gtk.Button("Enviar Webcam a Dispositivo Virtual (Filtro 14: Waterripple+Logo)")                                 
                              		             
		# Y luego le indicamos a los botones que cuando lea hagan click emita la
        	# senal "clicked" que llamara a la funcion "start_stop"
		self.boton0.connect("clicked", self.start_stop0)
		self.boton1.connect("clicked", self.start_stop1)
		self.boton2.connect("clicked", self.start_stop2)
		self.boton3.connect("clicked", self.start_stop3)
		self.boton4.connect("clicked", self.start_stop4)
		self.boton5.connect("clicked", self.start_stop5)
		self.boton6.connect("clicked", self.start_stop6)
		self.boton7.connect("clicked", self.start_stop7)
		self.boton8.connect("clicked", self.start_stop8)
	        self.boton9.connect("clicked", self.start_stop9)
		self.boton10.connect("clicked", self.start_stop10)
		self.boton11.connect("clicked", self.start_stop11)
		self.boton12.connect("clicked", self.start_stop12)
		self.boton13.connect("clicked", self.start_stop13)
		self.boton14.connect("clicked", self.start_stop14)
		
		# Agregamos los botones a la caja horizontal
		vbox.pack_start(self.boton0, False)
		vbox.pack_start(self.boton1, False)
		vbox.pack_start(self.boton2, False)
		vbox.pack_start(self.boton3, False)
		vbox.pack_start(self.boton4, False)
		vbox.pack_start(self.boton5, False)
		vbox.pack_start(self.boton6, False)
		vbox.pack_start(self.boton7, False)
		vbox.pack_start(self.boton8, False)
		vbox.pack_start(self.boton9, False)
		vbox.pack_start(self.boton10, False)
		vbox.pack_start(self.boton11, False)
		vbox.pack_start(self.boton12, False)
		vbox.pack_start(self.boton13, False)
		vbox.pack_start(self.boton14, False)
		
		# Tambien creamos un nuevo boton "Salir", que permitira cerrar la ventana de la aplicacion
		self.boton15 = gtk.Button("Salir")
		
	        # Luego le indicamos al boton que cuando le hagan click emita la
                # senal "clicked" que llamara a la funcion "exit"
		self.boton15.connect("clicked", self.exit)

		# Finalmente agregamos el boton de salir.
		vbox.pack_start(self.boton15, False)
		
		# Luego se muestra la caja (y todo lo que contiene) en la ventana principal.
		hbox.add(gtk.Label())
		ventana.show_all()

		# Configurando la tuberia gstreamer para aplicar los filtro de video "normal" , "bulge" , "square" , "fisheye", etc. + logo UCT

		self.player0 = gst.parse_launch ("v4l2src device=/dev/video0   !   alpha method=0 alpha=1   !   mezclador.   multifilesrc location=logouct1.png caps=image/png,framerate=1/1   !   pngdec   !   videobox border-alpha=0 alpha=.6 top=-380 left=-470   ! mezclador.   videomixer name=mezclador   !   videorate   !   ffmpegcolorspace   !   video/x-raw-yuv   !   v4l2sink device=/dev/video0 sync=false  ")  

		self.player1 = gst.parse_launch ("v4l2src device=/dev/video1   !   alpha method=0 alpha=1   !   mezclador.   multifilesrc location=logouct1.png caps=image/png,framerate=1/1   !   pngdec   !   videobox border-alpha=0 alpha=.6 top=-380 left=-470   ! mezclador.   videomixer name=mezclador   !   bulge   !   videorate   !   ffmpegcolorspace   !   video/x-raw-yuv   !   v4l2sink device=/dev/video0 sync=false  ")    

		self.player2 = gst.parse_launch ("v4l2src device=/dev/video1   !   alpha method=0 alpha=1   !   mezclador.   multifilesrc location=logouct1.png caps=image/png,framerate=1/1   !   pngdec   !   videobox border-alpha=0 alpha=.6 top=-380 left=-470   !   mezclador.   videomixer name=mezclador   !   square   !   videorate   !   ffmpegcolorspace   !   video/x-raw-yuv   !   v4l2sink device=/dev/video0 sync=false  ")        

		self.player3 = gst.parse_launch ("v4l2src device=/dev/video1   !   alpha method=0 alpha=1   !   mezclador.   multifilesrc location=logouct1.png caps=image/png,framerate=1/1   !   pngdec   !   videobox border-alpha=0 alpha=.6 top=-380 left=-470   !   mezclador.   videomixer name=mezclador   !   fisheye   !   videorate   !   ffmpegcolorspace   !   video/x-raw-yuv   !   v4l2sink device=/dev/video0 sync=false  ")     

		self.player4 = gst.parse_launch ("v4l2src device=/dev/video1   !   alpha method=0 alpha=1   !   mezclador.   multifilesrc location=logouct1.png caps=image/png,framerate=1/1   !   pngdec   !   videobox border-alpha=0 alpha=.6 top=-380 left=-470   !   mezclador.   videomixer name=mezclador   !   kaleidoscope   !   videorate   !   ffmpegcolorspace   !   video/x-raw-yuv   !   v4l2sink device=/dev/video0 sync=false  ")

		self.player5 = gst.parse_launch ("v4l2src device=/dev/video1   !   alpha method=0 alpha=1   !   mezclador.   multifilesrc location=logouct1.png caps=image/png,framerate=1/1   !   pngdec   !   videobox border-alpha=0 alpha=.6 top=-380 left=-470   !   mezclador.   videomixer name=mezclador   !   marble   !   videorate   !   ffmpegcolorspace   !   video/x-raw-yuv   !   v4l2sink device=/dev/video0 sync=false  ")   

		self.player6 = gst.parse_launch ("videomixer name=webcamvirtual   !   v4l2sink device=/dev/video0 webcamvirtual. v4l2src device=/dev/video1   !   video/x-raw-yuv   !   ffmpegcolorspace   !   textoverlay font-desc=Droid text=Estudios_Virtuales-Filtros_de_Video halignment=center valignment=top deltax=-10 deltay=-15 color=2576980377 shaded-background=false   !   videobox border-alpha=0 top=-0 left=-0 ! webcamvirtual.  ")   

		self.player7 = gst.parse_launch ("v4l2src device=/dev/video1   !   alpha method=0 alpha=1   !   mezclador.   multifilesrc location=logouct1.png caps=image/png,framerate=1/1   !   pngdec   !   videobox border-alpha=0 alpha=.6 top=-380 left=-470   !   mezclador.   videomixer name=mezclador   !   mirror   !   videorate   !   ffmpegcolorspace   !   video/x-raw-yuv   !   v4l2sink device=/dev/video0 sync=false  ") 

		self.player8 = gst.parse_launch ("v4l2src device=/dev/video1   !   alpha method=0 alpha=1   !   mezclador.   multifilesrc location=logouct1.png caps=image/png,framerate=1/1   !   pngdec   !   videobox border-alpha=0 alpha=.6 top=-380 left=-470   !   mezclador.   videomixer name=mezclador   !   pinch   !   videorate   !   ffmpegcolorspace   !   video/x-raw-yuv   !   v4l2sink device=/dev/video0 sync=false  ")  

		self.player9 = gst.parse_launch ("v4l2src device=/dev/video1   !   alpha method=0 alpha=1   !   mezclador.   multifilesrc location=logouct1.png caps=image/png,framerate=1/1   !   pngdec   !   videobox border-alpha=0 alpha=.6 top=-380 left=-470   !   mezclador.   videomixer name=mezclador   !   sphere   !   videorate   !   ffmpegcolorspace   !   video/x-raw-yuv   !   v4l2sink device=/dev/video0 sync=false  ")   

		self.player10 = gst.parse_launch ("v4l2src device=/dev/video1   !   alpha method=0 alpha=1   !   mezclador.   multifilesrc location=logouct1.png caps=image/png,framerate=1/1   !   pngdec   !   videobox border-alpha=0 alpha=.6 top=-380 left=-470   !   mezclador.   videomixer name=mezclador   !   square   !   videorate   !   ffmpegcolorspace   !   video/x-raw-yuv   !   v4l2sink device=/dev/video0 sync=false  ")   

		self.player11 = gst.parse_launch ("v4l2src device=/dev/video1   !   alpha method=0 alpha=1   !   mezclador.   multifilesrc location=logouct1.png caps=image/png,framerate=1/1   !   pngdec   !   videobox border-alpha=0 alpha=.6 top=-380 left=-470   !   mezclador.   videomixer name=mezclador   !   stretch   !   videorate   !   ffmpegcolorspace   !   video/x-raw-yuv   !   v4l2sink device=/dev/video0 sync=false  ") 

		self.player12 = gst.parse_launch ("v4l2src device=/dev/video1   !   alpha method=0 alpha=1   !   mezclador.   multifilesrc location=logouct1.png caps=image/png,framerate=1/1   !   pngdec   !   videobox border-alpha=0 alpha=.6 top=-380 left=-470   !   mezclador.   videomixer name=mezclador   !   tunnel   !   videorate   !   ffmpegcolorspace   !   video/x-raw-yuv   !   v4l2sink device=/dev/video0 sync=false  ")

		self.player13 = gst.parse_launch ("v4l2src device=/dev/video1   !   alpha method=0 alpha=1   !   mezclador.   multifilesrc location=logouct1.png caps=image/png,framerate=1/1   !   pngdec   !   videobox border-alpha=0 alpha=.6 top=-380 left=-470   !   mezclador.   videomixer name=mezclador   !   twirl   !   videorate   !   ffmpegcolorspace   !   video/x-raw-yuv   !   v4l2sink device=/dev/video0 sync=false  ")

		self.player14 = gst.parse_launch ("v4l2src device=/dev/video1   !   alpha method=0 alpha=1   !   mezclador.   multifilesrc location=logouct1.png caps=image/png,framerate=1/1   !   pngdec   !   videobox border-alpha=0 alpha=.6 top=-380 left=-470   !   mezclador.   videomixer name=mezclador   !   waterripple   !   videorate   !   ffmpegcolorspace   !   video/x-raw-yuv   !   v4l2sink device=/dev/video0 sync=false  ")

	
	# Se ejecutan al hacer click sobre el boton "Reproducir"
	def start_stop0(self, w):
		
		if self.boton0.get_label() == "Enviar Webcam a Dispositivo Virtual (Filtro 0: Normal+Logo)":
			self.boton0.set_label("Parar")
			self.player0.set_state(gst.STATE_PLAYING)
		
		else:
			self.player0.set_state(gst.STATE_NULL)
			self.boton0.set_label("Enviar Webcam a Dispositivo Virtual (Filtro 0: Normal+Logo)")	

	def start_stop1(self, w):
		if self.boton1.get_label() == "Enviar Webcam a Dispositivo Virtual (Filtro 1: Bulge+Logo)":
			self.boton1.set_label("Parar")
			self.player1.set_state(gst.STATE_PLAYING)
		
		else:
			self.player1.set_state(gst.STATE_NULL)
			self.boton1.set_label("Enviar Webcam a Dispositivo Virtual (Filtro 1: Bulge+Logo)")

        def start_stop2(self, w):

		if self.boton2.get_label() == "Enviar Webcam a Dispositivo Virtual (Filtro 2: Square+Logo)":
			self.boton2.set_label("Parar")
			self.player2.set_state(gst.STATE_PLAYING)
		
		else:
			self.player2.set_state(gst.STATE_NULL)
			self.boton2.set_label("Enviar Webcam a Dispositivo Virtual (Filtro 2: Square+Logo)")

	def start_stop3(self, w):

		if self.boton3.get_label() == "Enviar Webcam a Dispositivo Virtual (Filtro 3: Fisheye+Logo)":
			self.boton3.set_label("Parar")
			self.player3.set_state(gst.STATE_PLAYING)
		
		else:
			self.player3.set_state(gst.STATE_NULL)
			self.boton3.set_label("Enviar Webcam a Dispositivo Virtual (Filtro 3: Fisheye+Logo)")
	
	def start_stop4(self, w):

		if self.boton4.get_label() == "Enviar Webcam a Dispositivo Virtual (Filtro 4: Kaleidoscope+Logo)":
			self.boton4.set_label("Parar")
			self.player4.set_state(gst.STATE_PLAYING)
		
		else:
			self.player4.set_state(gst.STATE_NULL)
			self.boton4.set_label("Enviar Webcam a Dispositivo Virtual (Filtro 4: Kaleidoscope+Logo)")

	def start_stop5(self, w):

		if self.boton5.get_label() == "Enviar Webcam a Dispositivo Virtual (Filtro 5: Marble+Logo)":
			self.boton5.set_label("Parar")
			self.player5.set_state(gst.STATE_PLAYING)
		
		else:
			self.player5.set_state(gst.STATE_NULL)
			self.boton5.set_label("Enviar Webcam a Dispositivo Virtual (Filtro 5: Marble+Logo)")

	def start_stop6(self, w):

		if self.boton6.get_label() == "Enviar Webcam a Dispositivo Virtual (Filtro 6: Normal+Texto)":
			self.boton6.set_label("Parar")
			self.player6.set_state(gst.STATE_PLAYING)
			
		else:
			self.player6.set_state(gst.STATE_NULL)
			self.boton6.set_label("Enviar Webcam a Dispositivo Virtual (Filtro 6: Normal+Texto)")

	def start_stop7(self, w):

		if self.boton7.get_label() == "Enviar Webcam a Dispositivo Virtual (Filtro 7: Mirror+Logo)":
			self.boton7.set_label("Parar")
			self.player7.set_state(gst.STATE_PLAYING)
			
		else:
			self.player7.set_state(gst.STATE_NULL)
			self.boton7.set_label("Enviar Webcam a Dispositivo Virtual (Filtro 7: Mirror+Logo)")

	def start_stop8(self, w):

		if self.boton8.get_label() == "Enviar Webcam a Dispositivo Virtual (Filtro 8: Pinch+Logo)":
			self.boton8.set_label("Parar")
			self.player8.set_state(gst.STATE_PLAYING)
			
		else:
			self.player8.set_state(gst.STATE_NULL)
			self.boton8.set_label("Enviar Webcam a Dispositivo Virtual (Filtro 8: Pinch+Logo)")

	def start_stop9(self, w):

		if self.boton9.get_label() == "Enviar Webcam a Dispositivo Virtual (Filtro 9: Sphere+Logo)":
			self.boton9.set_label("Parar")
			self.player9.set_state(gst.STATE_PLAYING)
			
		else:
			self.player9.set_state(gst.STATE_NULL)
			self.boton9.set_label("Enviar Webcam a Dispositivo Virtual (Filtro 9: Sphere+Logo)")

	def start_stop10(self, w):

		if self.boton10.get_label() == "Enviar Webcam a Dispositivo Virtual (Filtro 10: Square+Logo)":
			self.boton10.set_label("Parar")
			self.player10.set_state(gst.STATE_PLAYING)
			
		else:
			self.player10.set_state(gst.STATE_NULL)
			self.boton10.set_label("Enviar Webcam a Dispositivo Virtual (Filtro 10: Square+Logo)")

	def start_stop11(self, w):

		if self.boton11.get_label() == "Enviar Webcam a Dispositivo Virtual (Filtro 11: Stretch+Logo)":
			self.boton11.set_label("Parar")
			self.player11.set_state(gst.STATE_PLAYING)
			
		else:
			self.player11.set_state(gst.STATE_NULL)
			self.boton11.set_label("Enviar Webcam a Dispositivo Virtual (Filtro 11: Stretch+Logo)")

	def start_stop12(self, w):

		if self.boton12.get_label() == "Enviar Webcam a Dispositivo Virtual (Filtro 12: Tunel+Logo)":
			self.boton12.set_label("Parar")
			self.player12.set_state(gst.STATE_PLAYING)
			
		else:
			self.player12.set_state(gst.STATE_NULL)
			self.boton12.set_label("Enviar Webcam a Dispositivo Virtual (Filtro 12: Tunel+Logo)")

	def start_stop13(self, w):

		if self.boton13.get_label() == "Enviar Webcam a Dispositivo Virtual (Filtro 13: Twirl+Logo)":
			self.boton13.set_label("Parar")
			self.player13.set_state(gst.STATE_PLAYING)
			
		else:
			self.player13.set_state(gst.STATE_NULL)
			self.boton13.set_label("Enviar Webcam a Dispositivo Virtual (Filtro 13: Twirl+Logo)")

	def start_stop14(self, w):

		if self.boton14.get_label() == "Enviar Webcam a Dispositivo Virtual (Filtro 14: Waterripple+Logo)":
			self.boton14.set_label("Parar")
			self.player14.set_state(gst.STATE_PLAYING)
			
		else:
			self.player14.set_state(gst.STATE_NULL)
			self.boton14.set_label("Enviar Webcam a Dispositivo Virtual (Filtro 14: Waterripple+Logo)")


	# Funcion para salir de la ventana
	def exit(self, widget, data=None):
		gtk.main_quit()

	

# Iniciamos la clase.
GTK_Main()

# iniciamos los threads, para indicarle a la aplicacion que se van a usar hilos en la interfaz grafica
gtk.gdk.threads_init()

# Ademas iniciamos el metodo gtk.main, que genera un ciclo que se utiliza
# para recibir todas las senales emitidas por los botones y demas widgets.
gtk.main()


