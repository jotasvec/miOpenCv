#!/usr/bin/env python
import pygst
pygst.require("0.10")
import gst
#import gtk
import cv2
#v4l2src device=/dev/video0  !  autovideosink

player = gst.parse_launch("v4l2src device=/dev/video0 ! autovideosink")
cap = cv2.VideoCapture(player)


while True:
	#se toma cada frame
	ret, frame = cap.read()

	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	cv2.imshow('webCam', frame)

	esc = cv2.waitKey(5) & 0xFF == 27
	if esc:
		break

cap.release()
cv2.destroyAllWindows()


# class FaceDetect:

	# def __init__(self):
	# 	pipe = """filesrc location=img/dudegreen.jpg ! decodebin ! ffmpegcolorspace ! facedetect ! ffmpegcolorspace ! ximagesink"""
	# 	self.pipeline = gst.parse_launch(pipe)
	# 	self.bus = self.pipeline.get_bus()
	# 	self.bus.add_signal_watch()
	# 	self.bus.connect("message::element", self.bus_message)

	# 	self.pipeline.set_state(gst.STATE_PLAYING)

	# def bus_message(self, bus, message):
	# 	st = message.structure
	# 	if st.get_name() == "face":
	# 		print "Face found at %d,%d with dimensions %dx%d" % (st["x"], st["y"], st["width"], st["height"])

# if __name__ == "__main__":
# 	f = FaceDetect()
# 	gtk.main()

#!/usr/bin/env python
#Example 2.2 http://pygstdocs.berlios.de/pygst-tutorial/playbin.html


# import wx
# import pygst
# pygst.require("0.10")
# import gst

# import gobject
# gobject.threads_init()

# class WX_Main(wx.App):

# 	def OnInit(self):
# 		window = wx.Frame(None)
# 		window.SetTitle("Video-Player")
# 		window.SetSize((500, 400))
# 		window.Bind(wx.EVT_CLOSE,self.destroy)
# 		vbox = wx.BoxSizer(wx.VERTICAL)
# 		hbox = wx.BoxSizer(wx.HORIZONTAL)
# 		self.entry = wx.TextCtrl(window)
# 		hbox.Add(self.entry, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
# 		self.button = wx.Button(window,label="Start")
# 		hbox.Add(self.button, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
# 		self.button.Bind(wx.EVT_BUTTON, self.start_stop)
# 		self.btnEfecto = wx.Button(window, label="efecto")
# 		hbox.Add(self.btnEfecto, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
# 		self.btnEfecto.Bind(wx.EVT_BUTTON, self.efecto)
# 		vbox.Add(hbox, 0, wx.EXPAND, 0)
# 		#panel de video
# 		self.movie_window = wx.Panel(window)
# 		vbox.Add(self.movie_window,1,wx.ALL | wx.EXPAND,4)
# 		window.SetSizer(vbox)
# 		window.Layout()
# 		window.Show()
# 		self.SetTopWindow(window)
# 		videoCamara = cv2.VideoCapture("v4l2src device=/dev/video0")
# 		self.player = gst.parse_launch(videoCamara)
# 		self.player2 = gst.parse_launch("v4l2src device=/dev/video1   !   mezclador.   videomixer name=mezclador   !   fisheye   !   videorate   !   ffmpegcolorspace   !   video/x-raw-yuv   !   v4l2sink device=/dev/video0 autovideosink  ")
# 		bus = self.player.get_bus()
# 		bus.add_signal_watch()
# 		bus.enable_sync_message_emission()
# 		bus.connect('message', self.on_message)
# 		bus.connect('sync-message::element', self.on_sync_message)

# 		return True

# 	def start_stop(self, event):
# 		if self.button.GetLabel() == "Start":
# 			#filepath = "img/bg.avi"
# 			#if os.path.exists(filepath):
# 			self.button.SetLabel("Stop")
# 			#self.player.set_property('uri',"file//img/bg.avi")
# 			self.player.set_state(gst.STATE_PLAYING)
# 		else:
# 			self.player.set_state(gst.STATE_NULL)
# 			self.button.SetLabel("Start")

# 	def efecto(self, Event):
# 		if self.btnEfecto.GetLabel() == "efecto":
# 			self.btnEfecto.SetLabel("Stop")
# 			self.player2.set_state(gst.STATE_PLAYING)
# 		else:
# 			self.player2.set_state(gst.STATE_NULL)
# 			self.btnEfecto.SetLabel("efecto")

# 	def on_message(self, bus, message):
# 		t = message.type
# 		if t == gst.MESSAGE_EOS:
# 			self.player.set_state(gst.STATE_NULL)
# 			self.button.SetLabel("Start")
# 		elif t == gst.MESSAGE_ERROR:
# 			self.player.set_state(gst.STATE_NULL)
# 			self.button.SetLabel("Start")

# 	def on_sync_message(self, bus, message):
# 		if message.structure is None:
# 			return
# 		message_name = message.structure.get_name()
# 		if message_name == 'prepare-xwindow-id':
# 			imagesink = message.src
# 			imagesink.set_property('force-aspect-ratio', True)
# 			imagesink.set_xwindow_id(self.movie_window.GetHandle())

# 	def destroy(self,event):
# 		#Stop the player pipeline to prevent a X Window System error
# 		self.player.set_state(gst.STATE_NULL)
# 		event.Skip()

# app = WX_Main()
# app.MainLoop()
