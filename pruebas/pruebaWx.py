#!/usr/bin/env python
# -*- coding: utf-8 -*-
#coding=utf-8


from wx import *
import cv2
import sys
import numpy as np

def cerrarTodo(self):
			sys.exit(0)

tamano_btn=(90,30) #tamano de botones

class VentanaPrincipal(Frame):
	def __init__(self, parent, title):
		super(VentanaPrincipal, self).__init__(parent,title=title, size=(500,500))
		self.Centre()
	
		status = self.CreateStatusBar() #barra de estado
		menubar = MenuBar() #barra de menu
		primerMenubar = Menu() #primer menu
		segundoMenubar = Menu() #segundo menu
		tercerMenubar = Menu() #tercer menu
		#asignar
		menubar.Append(primerMenubar,"archivos")
		menubar.Append(segundoMenubar,"editar")
		menubar.Append(tercerMenubar,"ayuda")

		# wx.ID_ABOUT y wx.ID_EXIT son tipos estandard incluidos en wxWidgets
		# Se aconseja usar los tipos estandard para hacer la interfaz
		# más nativa -> http://docs.wxwidgets.org/stable/wx_stdevtid.html
	
		#primer menu
		arch_nVentana = primerMenubar.Append(NewId(), "&ventana Nueva\tCtrl+N","click para abrir una nueva ventana" )
		arch_open = primerMenubar.Append(ID_OPEN, "&Abrir...\tCtrl+O ","Click para abrir un nuevo archivo" )
		arch_cVentana = primerMenubar.Append(ID_EXIT, "&Salir\tCtrl+Q","salir del programa")
		#Binds
		self.Bind(EVT_MENU, self.openCam, arch_nVentana) #nueva ventan
		self.Bind(EVT_MENU, cerrarTodo, arch_cVentana) #cerrar todo
		self.Bind(EVT_MENU, self.abrirArchivo, arch_open) #abrir un archivo
		#tercer menu
		tercerMenubar.Append(ID_ABOUT, "&Acerca de","informacion del programa")

		#para agregar barra de menus
		self.SetMenuBar(menubar)#se anade la barra de menu

		#agrega etiqueta
		saludo = StaticText(self, label="buenos dias, buenas tardes", pos=(10,20))
		#agregar boton para webcam
		btn_abrirCam = Button(self, label="webcam", pos=(10,100), size=tamano_btn)
		btn_abrirCam.Bind(EVT_BUTTON, self.openCam)

		#agrega btn para cerrar programa
		btn_cerrarMain = Button(self, label="cerrar", pos=(400,425), size=tamano_btn)
		btn_cerrarMain.Bind(EVT_BUTTON, cerrarTodo)

		self.Show()

	def openCam(self, Event):
		screenCam = VentanaWebcam(self)
		screenCam.Show()

	def abrirArchivo(self, event):
		self.dirname = ''
		dlg = FileDialog(self, "elegir un archivo", self.dirname, "","*.*",OPEN)
		#cuando se seleccione alguno -> ok?
		if dlg.ShowModal() == ID_OK:
			self.filename = dlg.GetFilename() #guardamos el nombre del archivo
			self.dirname = dlg.GetDirectory() #se guarda el directorio

			#se abre el fichero en modo lectura
			fichero = open(os.path.join(self.dirname, self.filename), 'r')
			#con setValue se pasa el fichero al control de texto
			self.control.setValue(fichero.read())
			fichero.close()
		dlg.Destory()


class VentanaWebcam(Frame):
	def __init__(self, parent):
		super(VentanaWebcam, self).__init__(parent, title="ventana Webcam", size=(400,400))
		#self.Centre()

		self.txtWebcam= StaticText(self, label="Ok!, to Work!", pos=(100,10))

		btn_CloseWc=Button(self, label="cerrar cam", pos=(300,350), size=tamano_btn)
		btn_CloseWc.Bind(EVT_BUTTON, self.cerrarCam)

		#agrego boton para modificar la imagen y buscar los valores de seteo de los verdes
		btn_setColor=Button(self, label="set color", pos=(200,350), size=(tamano_btn))
		btn_setColor.Bind(EVT_BUTTON, self.setColores)

		#agregar el video a la ventana
		self.capture = cv2.VideoCapture(0)
		self.capture.set(3,400)
		self.capture.set(4,300)
		
		if self.capture.isOpened():
			ret, frame = self.capture.read()
		else:
			ret = False
			print "problemas por aqui?"
					
		ret, frame = self.capture.read()
		
		(height, width) = frame.shape[:2]
		self.bmp = wx.BitmapFromBuffer(width, height, frame)
		
		print "a ved -> ", self.bmp.GetSize()
		#los siguientes codigos son para que se capture los videos framexframe 
		#se toma un timer para iniciar la secuencia de frames
		fps=15
		self.timer = wx.Timer(self)
		self.timer.Start(1000./fps)

		self.Bind(wx.EVT_PAINT, self.onPaint)
		self.Bind(wx.EVT_TIMER, self.onNextFrame)


	def onPaint(self, evt):
		dc = wx.AutoBufferedPaintDC(self)
		dc.DrawBitmap(self.bmp, 20,20, True)


	def onNextFrame(self,evt):
		ret, frame = self.capture.read()
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		self.bmp.CopyFromBuffer(frame)
		self.Refresh()

		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		cv2.imshow('hsv',hsv)

		bajosrb = np.array([49,50,50])
		altosrb = np.array([80,255,255])

		mask = cv2.inRange(hsv, bajosrb, altosrb)

		moments = cv2.moments(mask)
		area = moments['m00']

		if area > 2000000:
			#se buscan los centros
			x = int(moments['m10']/moments['m00'])
			y = int(moments['m01']/moments['m00'])

			#escribimos el valor de los centros
			print "x = %d, y = %d" %(x, y)

			cv2.rectangle(frame, (x,y), (x+2,y+2), (0,0,255), 2)

		mask2 = cv2.bitwise_and(frame, frame, mask=~mask)

		cv2.imshow('mask', mask)
		cv2.imshow('mask2 cvt rgb', cv2.cvtColor(mask2, cv2.COLOR_BGR2RGB))

	def cerrarCam(self, Event):
		self.Destroy()

	def setColores(self, Frame):
		nFrame = SetColorVerdes("set colores")
		nFrame.ShowModal()
		nFrame.Destroy()

class SetColorVerdes(wx.Dialog):
	def __init__(self, parent):		
		super(SetColorVerdes
			, self).__init__(None,-1, "set colores")
		self.SetSize((200,170))


		#se crea una caja vertical para ir cargano los elementos
		panel = Panel(self)
		vBox = BoxSizer(wx.VERTICAL)
		
		sb = StaticBox(panel, 1, label = "colores")
		sbs = StaticBoxSizer(sb, wx.VERTICAL)
		
		#se crean diferente caja horizontales que iran en la vertical
		#Horizontal Box 1
		hBox1 = BoxSizer(wx.HORIZONTAL)
		hBox1.Add(StaticText(panel, -1,'R : '), 1)
		hBox1.Add(TextCtrl(panel, -1), 0)
		sbs.Add(hBox1, 0, wx.LEFT)

		#horzontalBox 2
		hBox2= BoxSizer(wx.HORIZONTAL)	
		hBox2.Add(StaticText(panel, -1,'G : '), 1)
		hBox2.Add(TextCtrl(panel, -1), 0)
		sbs.Add(hBox2, 0, wx.LEFT)

		#Horizontal Box 3
		hBox3 = BoxSizer(wx.HORIZONTAL)			
		hBox3.Add(StaticText(panel, -1,'B : '), 1)
		hBox3.Add(TextCtrl(panel, -1), 0)
		sbs.Add(hBox3, 0, wx.LEFT)

		panel.SetSizer(sbs)
		#botones
		hBoxBotones = BoxSizer(wx.HORIZONTAL)
		okButton = Button(self, 0,label="ok")
		cnclButton = Button(self, 0,label="cancel")
		hBoxBotones.Add(okButton)
		hBoxBotones.Add(cnclButton)

		#se agregan los paneles al vertical Box
		vBox.Add(panel, -1, wx.ALL | wx.EXPAND, border=10)
		vBox.Add(hBoxBotones, 0,wx.ALIGN_CENTER |wx.BOTTOM, border=10)
		self.SetSizer(vBox)

		okButton.Bind(wx.EVT_BUTTON, self.envData)
		cnclButton.Bind(wx.EVT_BUTTON, self.cerrar)

	def envData(self, Event):
		pass

	def cerrar(self, Event):
		self.Destroy()


app = App(0)
VentanaPrincipal(None, title="Main Frame")
app.MainLoop()	