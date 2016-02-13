#!/usr/bin/env python
# -*- coding: utf-8 -*-
# coding=utf-8

# import wxversion
# wxversion.select("2.8")
import wx
import cv2
import sys
import numpy as np
import os

def cerrarTodo(self):
    sys.exit(0)

tamano_btn = (90, 30)  # tamano de botones

wildcardImagen = "Imagen source (*.jpg, *.png, *.gif)|*.jpg;*.png; *.gif\
            |All files (*.*)|*.*"

wildcardVideo = "Video source (*.avi, *.mp4, *.divx, *.mov)|*.avi; *.mp4; *.divx; *.mov\
                |All files (*.*)|*.*"
currentDirectory = os.getcwd()

listaImgs= []
listaVids= []
esImagen = 0

class ImagenBackground:
    #def __init__(self):
    def selectFromListImg(self, itemImg):
        print "item elegido de a lista ",itemImg
        if len(listaImgs) != 0:
                if itemImg in listaImgs:
                    print "ya se encuentra"
                    listaImgs.remove(itemImg)
                    listaImgs.insert(0,str(itemImg))
                else:
                    listaImgs.insert(0,str(itemImg))
        else:
            listaImgs.insert(0,str(itemImg))
        print "-> ",listaImgs

    def selectFromListVids(self, itemVideo):
        print "item elegido de a lista ",itemVideo
        if len(listaVids) != 0:
                if itemVideo in listaVids:
                    print "ya se encuentra"
                    listaVids.remove(itemVideo)
                    listaVids.insert(0,str(itemVideo))
                else:
                    listaVids.insert(0,str(itemVideo))
        else:
            listaVids.insert(0,str(itemVideo))
        print "-> ",listaVids


    def getImgBackground(self):
        return listaImgs[0]

    def seleccionRb(self, selec):
        print "se seleccionó -> ",selec
        global esImagen
        esImagen = selec

    def getSeleccionRb(self):
        return esImagen

class VentanaPrincipal(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(450, 350))
        self.Centre()

        self.CreateStatusBar()  # barra de estado

########-Barra de Menus-##############################################################################
        menubar = wx.MenuBar()  # barra de menu
        primerMenubar = wx.Menu()  # primer menu
        segundoMenubar = wx.Menu()  # segundo menu
        tercerMenubar = wx.Menu()  # tercer menu

        # asignar
        menubar.Append(primerMenubar, "Archivos")
        menubar.Append(segundoMenubar, "Editar")
        menubar.Append(tercerMenubar, "Ayuda")

        # wx.ID_ABOUT y wx.ID_EXIT son tipos estandard incluidos en wxWidgets
        # Se aconseja usar los tipos estandard para hacer la interfaz
        # más nativa -> http://docs.wxwidgets.org/stable/wx_stdevtid.html

        # primer menu

        #nueva ventana
        arch_nVentana = primerMenubar.Append(
            wx.NewId(), "&ventana Nueva\tCtrl+N", "click para abrir una nueva ventana")
        #abrir archivos
        arch_open = wx.Menu()
        arch_open_img = arch_open.Append(wx.ID_ANY, "Abrir archivos de imagen")
        arch_open_vid = arch_open.Append(wx.ID_ANY, "Abrir archivos de Video")

        primerMenubar.AppendMenu(wx.ID_ANY, "Abrir Archivos", arch_open)
        #primerMenubar.Append(wx.ID_OPEN, "&Abrir...\tCtrl+O ", "Click para abrir un nuevo archivo")
        arch_save = primerMenubar.Append(wx.ID_SAVE, '&Save')
        #cerrar ventana
        arch_cVentana = primerMenubar.Append(wx.ID_EXIT, "&Salir\tCtrl+Q", "salir del programa")

        # Binds
        self.Bind(wx.EVT_MENU, self.openCam, arch_nVentana)  # nueva ventan
        self.Bind(wx.EVT_MENU, cerrarTodo, arch_cVentana)  # cerrar todo
        self.Bind(wx.EVT_MENU, self.onSave, arch_save)
        self.Bind(wx.EVT_MENU, self.onOpenImage, arch_open_img)  # abrir un archivo
        self.Bind(wx.EVT_MENU, self.onOpenVideo, arch_open_vid)  # abrir un archivo

        # tercer menu
        tercerMenubar.Append(wx.ID_ABOUT, "&Acerca de",
                             "informacion del programa")

        # para agregar barra de menus
        self.SetMenuBar(menubar)  # se añade la barra de menu

########-Barra de Menus-##############################################################################

#se crea un panel para agregar los distintos elementos de las ventanas
        panel = wx.Panel(self)
        sizerGrid = wx.GridBagSizer(10,10)

        # agrega etiqueta de saludo u otra cosa
        txtSaludo = wx.StaticText(panel, label="buenos dias, \nbuenas tardes")
        sizerGrid.Add(txtSaludo, pos=(0,0),flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=10)
        #se agrega una linea de separacion
        line = wx.StaticLine(panel)
        sizerGrid.Add(line, pos=(1,0), span=(1,10),flag=wx.EXPAND | wx.BOTTOM)

#se crea el texto, combobox y boton de agregar fondos tipo imagen
        #texto
        txtCmboImg = wx.StaticText(panel, label=" select a image: \n backgorund ")
        sizerGrid.Add(txtCmboImg, pos=(2,0), flag=wx.TOP | wx.EXPAND, border= 5)
        #comboBox
        self.cmboBoxImg = wx.ComboBox(panel, style=wx.CB_DROPDOWN, choices=listaImgs, value="elija una opcion")
        sizerGrid.Add(self.cmboBoxImg, pos=(2,1), span=(1,6), flag= wx.TOP | wx.LEFT | wx.BOTTOM | wx.EXPAND, border=5)  # ,  flag=wx.TOP| wx.EXPAND, border=10)
        self.cmboBoxImg.Bind(wx.EVT_COMBOBOX, self.selectItemImg)
        #boton
        btnCmboImg = wx.Button(panel, label="abrir")
        sizerGrid.Add(btnCmboImg, pos=(2,7), flag=wx.TOP | wx.RIGHT, border=5)
        btnCmboImg.Bind(wx.EVT_BUTTON, self.onOpenImage)

#se crea el texto, combobox y boton de agregar fondos tipo video
        #texto
        txtCmboVideo = wx.StaticText(panel, label=" select a video: \n backgorund ")
        sizerGrid.Add(txtCmboVideo, pos=(3,0), flag=wx.EXPAND | wx.BOTTOM, border=5)
        #comboBox
        self.cmboBoxVideo = wx.ComboBox(panel, style=wx.CB_DROPDOWN, choices=listaVids, value="elija una opcion")
        sizerGrid.Add(self.cmboBoxVideo, pos=(3,1), span=(1,6), flag= wx.TOP | wx.LEFT | wx.BOTTOM | wx.EXPAND, border=5)
        self.cmboBoxVideo.Bind(wx.EVT_COMBOBOX, self.selectItemVideo)
        #boton
        btnCmboVideo = wx.Button(panel, label="abrir")
        sizerGrid.Add(btnCmboVideo, pos=(3,7), flag=wx.TOP | wx.RIGHT, border=5)
        btnCmboVideo.Bind(wx.EVT_BUTTON, self.onOpenVideo)

# se agregan unos radioButtom para seleccionar si usamos un fondo de tipo imagen o de tipo Video
        radioList = ['Imagen','Video']
        self.rdBox = wx.RadioBox(panel, label="seleccione tipo BackGround", choices=radioList)
        # self.rdButtomImage = wx.RadioButton(self.rdBox, label="imagen")
        # self.rdButtomVideo = wx.RadioButton(self.rdBox, label="video")
        sizerGrid.Add(self.rdBox, pos=(4,1), span=(1,6), flag= wx.TOP | wx.LEFT | wx.BOTTOM | wx.EXPAND, border=5)

        self.rdBox.Bind(wx.EVT_RADIOBOX, self.selectRadioBox)

#se agregan los botones a la parte de abajo
        # agregar boton para webcam

        btn_abrirCam = wx.Button(panel, label="webcam", size=tamano_btn)
        sizerGrid.Add(btn_abrirCam, pos=(5,0), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=5)
        btn_abrirCam.Bind(wx.EVT_BUTTON, self.openCam)

        # agrega btn para cerrar programa
        btn_cerrarMain = wx.Button(panel, label="cerrar", size=tamano_btn)
        sizerGrid.Add(btn_cerrarMain, pos=(5,4), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=5)
        btn_cerrarMain.Bind(wx.EVT_BUTTON, cerrarTodo)

        #se setea el grid
        panel.SetSizer(sizerGrid)

        self.Show()
    def onSave():
        pass

    def openCam(self, Event):
        if len(listaImgs) != 0 or len(listaVids) != 0:
            screenCam = VentanaWebcam(self)
            screenCam.Show()
        else:
            print "agrega algun tipo de fondo"
            wx.MessageBox('Ups! no has agregando un fondo de Imagen o Video', 'Info', wx.OK | wx.ICON_INFORMATION)

    def onOpenImage(self, Event):
        dirname = currentDirectory
        dlg = wx.FileDialog(None, "elegir un archivo", dirname, "", wildcardImagen, wx.OPEN)
        # cuando se seleccione alguno -> ok?
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()    # se guarda el nombre del archivo
            self.dirname = dlg.GetDirectory()    # se guarda la ruta al directorio
            self.path = dlg.GetPath()
            print "file name -> %s \n dirname -> %s \n path -> %s" %(str(self.filename), str(self.dirname), str(self.path))
            if self.path in listaImgs:
                wx.MessageBox('Ups! este fondo ya ah sido agregado a la lista', 'Info', wx.OK | wx.ICON_INFORMATION)
            else:
                self.addListImgBg(self.path)
        dlg.Destroy()

    def onOpenVideo(self, Event):
        dirname = currentDirectory
        dlg = wx.FileDialog(None, "elegir un archivo", dirname, "", wildcardVideo, wx.OPEN)
        # cuando se seleccione alguno -> ok?
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()    # se guarda el nombre del archivo
            self.dirname = dlg.GetDirectory()    # se guarda la ruta al directorio
            self.path = dlg.GetPath()
            print "file name -> %s \n dirname -> %s \n path -> %s" %(str(self.filename), str(self.dirname), str(self.path))
            if self.path in listaVids:
                wx.MessageBox('Ups! este fondo ya ah sido agregado a la lista', 'Info', wx.OK | wx.ICON_INFORMATION)
            else:
                self.addListVidBg(self.path)
        dlg.Destroy()


    #se agrega la direccion que contien la imagen a la lista, se setean los valores por defecto de los comboBox y se autoselecciona el item nuevo
    def addListImgBg(self, imageDir):
        print "se agregara la sigte direccion -> ", imageDir
        self.cmboBoxImg.Append(imageDir)
        setValor = self.cmboBoxImg.SetValue(imageDir)
        self.selectItemImg(setValor)

    def addListVidBg(self, videoDir):
        print "se agregara la sigte direccion -> ", videoDir
        self.cmboBoxVideo.Append(videoDir)
        setValor = self.cmboBoxVideo.SetValue(videoDir)
        self.selectItemVideo(setValor)

    #esta funcion enviara los datos a la siguiente clase
    def selectItemImg(self, Event):
        itemselecionado = self.cmboBoxImg.GetValue()
        print "el item seleccionado es -> ", itemselecionado
        ImagenBackground().selectFromListImg(itemselecionado)

    def selectItemVideo(self, Event):
        itemselecionado = self.cmboBoxVideo.GetValue()
        print "el item seleccionado es -> ", itemselecionado
        ImagenBackground().selectFromListVids(itemselecionado)

    def selectRadioBox(self, Event):
        if self.rdBox.GetSelection() == 0:
            self.esImagen = 0
        elif self.rdBox.GetSelection() == 1:
            self.esImagen = 1
        ImagenBackground().seleccionRb(self.esImagen)

class VentanaWebcam(wx.Frame):
    def __init__(self, parent):
        super(VentanaWebcam, self).__init__(
            None, title="ventana Webcam", size=(400, 400))
        self.Centre()
        self.CreateStatusBar()  # barra de estado

        self.txtWebcam = wx.StaticText(self, label="Ok!, to Work!", pos=(100, 50))

        btn_CloseWc = wx.Button(self, label="cerrar cam", pos=(300, 330), size=tamano_btn)
        btn_CloseWc.Bind(wx.EVT_BUTTON, self.cerrarCam)

        # agrego boton para modificar la imagen y buscar los valores de seteo
        # de los verdes
        btn_setColor = wx.Button(self, label="set color", pos=(200, 330), size=(tamano_btn))
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
#funcion para crear punto de dibujo de bitmap
    def onPaint(self, evt):
        dc = wx.PaintDC(self)
        dc.DrawBitmap(self.bmp, 20, 20, True)
#funcion que muestra los siguientes frames a partir del on point
    def onNextFrame(self, evt):
        ret, frame = self.capture.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.flip(frame,1,frame)
        self.bmp.CopyFromBuffer(frame)
        self.Refresh()

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        #cv2.imshow('hsv', hsv)
        bajosrb = np.array([49, 50, 50])
        altosrb = np.array([80, 255, 255])

        # toma los rangos de verdes en hsv
        mask = cv2.inRange(hsv, bajosrb, altosrb)
        # para refinar la maskara se le aplica la operacion morfologica openig y creamo un kernel
        kernel = np.ones((7, 7), np.uint8)
        # refina el ruido externo a las regiones blancas correspondientes
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.dilate(mask, kernel, iterations=1)
        #ret, mask = cv2.threshold(mask, 100,255, cv2.THRESH_BINARY)
        mask = cv2.GaussianBlur(mask, (7,7),0)
        #cv2.imshow('mask con opening', mask)

        #se se invierte la mascara para mostrar los verdes en negro con la aplicacion de filtros

        #se produce una segunda mascara para luego utilizarla con el fondo
        ret, mask = cv2.threshold(mask, 170,255,cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)
        mask_inv = cv2.GaussianBlur(mask_inv, (5,5),0)
        mask_inv = cv2.morphologyEx(mask_inv, cv2.MORPH_OPEN,kernel)
        #cv2.imshow('mask_inv', mask_inv)


#print listaImgs[0]  # DirBgImg.getImgBackground()
        #vemos que tipo de backGround es si es 0 es imagen si es 1 es tipo video
        if ImagenBackground().getSeleccionRb() == 0:
            bgimg = cv2.imread(listaImgs[0])
        elif ImagenBackground().getSeleccionRb() == 1:
            capVideo = cv2.VideoCapture()
            capVideo.open(listaVids[0])
            ret2, bgimg = capVideo.read()
            cv2.imshow('bgImg', bgimg)

        #se configuran el tamaños de las imagenes
        size_bg = bgimg.shape[:2]
        size_ibi = mask_inv.shape[:2]

        (x,y) = size_ibi
        if size_bg != size_ibi:
            bgimg = cv2.resize(bgimg,(y,x))

        #seleccion area de interes
        roi = cv2.bitwise_and(bgimg, bgimg, mask=~mask_inv)
        #cv2.imshow('roi', roi)

        # invierte los colores de la mascara
        mask = cv2.bitwise_and(frame, frame, mask=~mask)
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2RGB)


        # se superponen las dos capas de imagenes para mostrar el chroma

        final = cv2.add(roi, mask)
        cv2.imshow('chroma', final)

        cv2.destroyAllWindows()

    def getChroma():
        pass

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

        # Primero voy a publicar un pequeño código que convierte BRG a HSV en la cual introducimos un color en BRG y nos da como resultado HSV:


        # green = np.uint8([[[0,255,0 ]]])
        # hsv_green = cv2.cvtColor(green,cv2.COLOR_BGR2HSV)
        # print hsv_green

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
