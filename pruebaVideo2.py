#pruebaVideo2.py open video
#import cv2
import wx
import os

wildcardImagen = "Imagen source (*.jpg, *.png, *.gif)|*.jpg;*.png; *.gif\
			|All files (*.*)|*.*"

wildcardVideo = "|Video source (*.avi, *.mp4, *.divx, *.mov)|*.avi; *.mp4; *.divx; *.mov\
				|All files (*.*)|*.*"
currentDirectory = os.getcwd()
def openFileImage():
	""" se crea y se muestra la ventana
	para seleccionar archivos tipo imagen"""
	dlgOpen = wx.FileDialog(None, message="elije un archivo de imagen o video",
		defaultDir=currentDirectory,
		defaultFile="",
		wildcard=wildcardImagen,
		style = wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR)

	if dlgOpen.ShowModal() != wx.ID_OK:
		print "oh oh! problemas"
	#destruimos el dialogo
	dlgOpen.Destroy()
	#destruimos la ventana principal

	path = dlgOpen.GetPath()
	print "se abrira el siguiente archivo: ", path
	return path

class MainFrame(wx.Frame):
	def retornarImagen(self, Evt):
		hola = openFileImage()
		print "hola hola -->",hola
		return "retorna desde Main Frame"
		self.Destroy()

	def __init__(self):
		wx.Frame.__init__(self, None, title="principal", size=(150,70))
		self.Centre()
		self.Show()
		panel = wx.Panel(self, wx.ID_ANY)

		openFileVideo = wx.Button(panel, label="abrir archivo")
		openFileVideo.Bind(wx.EVT_BUTTON, self.openFileVideo)

		openFileimage = wx.Button(panel, label="abrir archivo")
		openFileimage.Bind(wx.EVT_BUTTON, self.retornarImagen)

		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(openFileVideo, 0, wx.ALL | wx.CENTRE, 5)
		sizer.Add(openFileimage, 0, wx.ALL | wx.CENTRE, 5)

		panel.SetSizer(sizer)




	def openFileVideo(self, Evt):
		pass
		# """ se crea y se muestra la ventana
		# 	para seleccionar archivos Tipo video """
		# dlgOpen = wx.FileDialog(
		# 	self, message="elije un archivo de imagen o video",
		# 	defaultDir=currentDirectory,
		# 	defaultFile="",
		# 	wildcard=wildcardVideo,
		# 	style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR)

		# if dlgOpen.ShowModal() != wx.ID_OK:
		# 	print "oh oh! problemas"

		# dlgOpen.Destroy()
		# self.path = dlgOpen.GetPath()
		# print "se abrira el siguiente archivo: ", self.path

		# return self.path

app = wx.App(False)
MainFrame()
app.MainLoop()