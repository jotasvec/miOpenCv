#!/usr/bin/env python
# -*- coding: utf-8 -*-
# coding=utf-8


import wx
import cv2
import sys
import numpy as np


def cerrarTodo(self):
    sys.exit(0)

tamano_btn = (90, 30)  # tamano de botones


class VentanaPrincipal(wx.Frame):

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(500, 500))
        self.Centre()

        self.CreateStatusBar()  # barra de estado
        menubar = wx.MenuBar()  # barra de menu
        primerMenubar = wx.Menu()  # primer menu
        segundoMenubar = wx.Menu()  # segundo menu
        tercerMenubar = wx.Menu()  # tercer menu
        # asignar
        menubar.Append(primerMenubar, "archivos")
        menubar.Append(segundoMenubar, "editar")
        menubar.Append(tercerMenubar, "ayuda")

        # wx.ID_ABOUT y wx.ID_EXIT son tipos estandard incluidos en wxWidgets
        # Se aconseja usar los tipos estandard para hacer la interfaz
        # más nativa -> http://docs.wxwidgets.org/stable/wx_stdevtid.html

        # primer menu
        arch_nVentana = primerMenubar.Append(
            wx.NewId(), "&ventana Nueva\tCtrl+N", "click para abrir una nueva ventana")
        arch_open = primerMenubar.Append(
            wx.ID_OPEN, "&Abrir...\tCtrl+O ", "Click para abrir un nuevo archivo")
        arch_cVentana = primerMenubar.Append(
            wx.ID_EXIT, "&Salir\tCtrl+Q", "salir del programa")
        # Binds
        self.Bind(wx.EVT_MENU, self.openCam, arch_nVentana)  # nueva ventan
        self.Bind(wx.EVT_MENU, cerrarTodo, arch_cVentana)  # cerrar todo
        self.Bind(wx.EVT_MENU, self.abrirArchivo, arch_open)  # abrir un archivo
        # tercer menu
        tercerMenubar.Append(wx.ID_ABOUT, "&Acerca de",
                             "informacion del programa")

        # para agregar barra de menus
        self.SetMenuBar(menubar)  # se anade la barra de menu

        # agrega etiqueta
        saludo = wx.StaticText(
            self, label="buenos dias, buenas tardes", pos=(10, 20))
        # agregar boton para webcam
        btn_abrirCam = wx.Button(self, label="webcam",
                              pos=(10, 100), size=tamano_btn)
        btn_abrirCam.Bind(wx.EVT_BUTTON, self.openCam)

        # agrega btn para cerrar programa
        btn_cerrarMain = wx.Button(self, label="cerrar",
                                pos=(400, 425), size=tamano_btn)
        btn_cerrarMain.Bind(wx.EVT_BUTTON, cerrarTodo)

        self.Show()

    def openCam(self, Event):
        screenCam = VentanaWebcam(self)
        screenCam.Show()

    def abrirArchivo(self, event):
        self.dirname = ''
        dlg = FileDialog(self, "elegir un archivo",
                         self.dirname, "", "*.*", OPEN)
        # cuando se seleccione alguno -> ok?
        if dlg.ShowModal() == ID_OK:
            self.filename = dlg.GetFilename()  # guardamos el nombre del archivo
            self.dirname = dlg.GetDirectory()  # se guarda el directorio

            # se abre el fichero en modo lectura
            fichero = open(os.path.join(self.dirname, self.filename), 'r')
            # con setValue se pasa el fichero al control de texto
            self.control.setValue(fichero.read())
            fichero.close()
        dlg.Destory()


class VentanaWebcam(wx.Frame):

    def __init__(self, parent):
        super(VentanaWebcam, self).__init__(
            parent, title="ventana Webcam", size=(400, 400))
        # self.Centre()
        self.CreateStatusBar()# barra de estado

        self.txtWebcam = wx.StaticText(self, label="Ok!, to Work!", pos=(100, 50))

        btn_CloseWc = wx.Button(self, label="cerrar cam", pos=(300, 330), size=tamano_btn)
        btn_CloseWc.Bind(wx.EVT_BUTTON, self.cerrarCam)

        # agrego boton para modificar la imagen y buscar los valores de seteo
        # de los verdes
        btn_setColor = wx.Button(self, label="set color",
                              pos=(200, 330), size=(tamano_btn))
        btn_setColor.Bind(wx.EVT_BUTTON, self.setColores)

        # agregar el video a la ventana
        self.capture = cv2.VideoCapture(0)
        self.capture.set(3, 400)
        self.capture.set(4, 300)

        if self.capture.isOpened():
            ret, frame = self.capture.read()
        else:
            ret = False
            print "problemas por aqui?"

        ret, frame = self.capture.read()

        (height, width) = frame.shape[:2]
        self.bmp = wx.BitmapFromBuffer(width, height, frame)

        print "a ved -> ", self.bmp.GetSize()
        # los siguientes codigos son para que se capture los videos framexframe
        # se toma un timer para iniciar la secuencia de frames
        fps = 15
        self.timer = wx.Timer(self)
        self.timer.Start(1000. / fps)

        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_TIMER, self.onNextFrame)

    def onPaint(self, evt):
        dc = wx.PaintDC(self)
        dc.DrawBitmap(self.bmp, 20, 20, True)

    def onNextFrame(self, evt):
        ret, frame = self.capture.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.bmp.CopyFromBuffer(frame)
        self.Refresh()

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        cv2.imshow('hsv', hsv)

        bajosrb = np.array([49, 50, 50])
        altosrb = np.array([80, 255, 255])

        # toma los rangos de verdes en hsv
        mask = cv2.inRange(hsv, bajosrb, altosrb)
        # para refinar la maskara se le aplica la operacion morfologica openig
        kernel = np.ones((5, 5), np.uint8)
        # refina el ruido externo a las regiones blancas correspondientes
        opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        cv2.imshow('mask con opening', opening)

        moments = cv2.moments(mask)
        area = moments['m00']


        # invierte los colores de la mascara
        mask2 = cv2.bitwise_and(frame, frame, mask=~opening)
        
        mask2_inv = cv2.cvtColor(mask2, cv2.COLOR_BGR2RGB)
        # muestra la mascara invertida y en color RGB y con el verde en negro
        cv2.imshow('mask2 cvt rgb', mask2_inv)

        # veremos como remplazar los pixeles negros por otra cosa

        # se crea un cuadro de color x para remplazo de la region negra dada por el verde
        # toReplace = cv2.imread('img/img1.png')
        # cv2.imshow('toReplace', toReplace)

        # maskReplace = cv2.bitwise_not(toReplace, toReplace, mask=mask2_inv)
        # cv2.imshow('maskReplace', maskReplace)




    def cerrarCam(self, Event):
        self.Destroy()
        cv2.destroyAllWindows()

    def setColores(self, Frame):
        nFrame = SetColorVerdes("set colores")
        nFrame.ShowModal()
        nFrame.Destroy()


class SetColorVerdes(wx.Dialog):

    def __init__(self, parent):
        super(SetColorVerdes, self).__init__(None, -1, "set colores")
        self.SetSize((200, 170))

        # se crea una caja vertical para ir cargano los elementos
        panel = wx.Panel(self)
        vBox = wx.BoxSizer(wx.VERTICAL)

        sb = wx.StaticBox(panel, 1, label="colores")
        sbs = wx.StaticBoxSizer(sb, wx.VERTICAL)

        # se crean diferente caja horizontales que iran en la vertical
        # Horizontal Box 1
        hBox1 = wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(wx.StaticText(panel, -1, 'R : '), 1)
        self.r_tc = wx.TextCtrl(panel, -1, value='0')
        hBox1.Add(self.r_tc, 0)
        sbs.Add(hBox1, 0, wx.LEFT)

        # horzontalBox 2
        hBox2 = wx.BoxSizer(wx.HORIZONTAL)
        hBox2.Add(wx.StaticText(panel, -1, 'G : '), 1)
        self.g_tc = wx.TextCtrl(panel, -1, value='255')
        hBox2.Add(self.g_tc, 0)
        sbs.Add(hBox2, 0, wx.LEFT)

        # Horizontal Box 3
        hBox3 = wx.BoxSizer(wx.HORIZONTAL)
        hBox3.Add(wx.StaticText(panel, -1, 'B : '), 1)
        self.b_tc = wx.TextCtrl(panel, -1, value='0')
        hBox3.Add(self.b_tc, 0)
        sbs.Add(hBox3, 0, wx.LEFT)

        panel.SetSizer(sbs)
        # botones
        hBoxBotones = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self, 0, label="ok")
        cnclButton = wx.Button(self, 0, label="cancel")
        hBoxBotones.Add(okButton)
        hBoxBotones.Add(cnclButton)

        # se agregan los paneles al vertical Box
        vBox.Add(panel, -1, wx.ALL | wx.EXPAND, border=10)
        vBox.Add(hBoxBotones, 0, wx.ALIGN_CENTER | wx.BOTTOM, border=10)
        self.SetSizer(vBox)

        okButton.Bind(wx.EVT_BUTTON, self.envData)
        cnclButton.Bind(wx.EVT_BUTTON, self.cerrar)

    def envData(self, Event):
        red_getData = self.r_tc.GetValue()
        blue_getData = self.b_tc.GetValue()
        green_getData = self.g_tc.GetValue()

        print "valor RGB = (%s,%s,%s)" % (red_getData, green_getData, blue_getData)

        # a tener en cuenta lo siguiente para pasar los valores a hsv
        colorBGR = np.uint8(
            [[[int(red_getData), int(green_getData), int(blue_getData)]]])
        colorHSV = cv2.cvtColor(colorBGR, cv2.COLOR_BGR2HSV)
        #(h,s,v) = colorHSV
        # print "valores H = %i,S = %i,V = %i ->"%(h,s,v)
        print "hsv ->", colorHSV

        # return colorHSV

        # resultado
        # [[[ 60 255 255]]]

        # Para obtener el rango mín y el max de este color Hacemos lo sig…

        # Rango Min [H-10, 100,100] se resta al primer valor ((-10) ,100,100)
        # Max [H + 10, 255, 255] se le suma la primer valor ((+10), 255,255)

        # min = 50,100,100
        # Max = 70,255,255

    def cerrar(self, Event):
        self.Destroy()


app = wx.App(0)
VentanaPrincipal(None, title="Main Frame")
app.MainLoop()
