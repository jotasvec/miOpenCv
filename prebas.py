# import time, random
# from threading import *
# import wx
# import thread

# # Button definitions
# ID_START = wx.NewId()
# ID_STOP = wx.NewId()

# # Define notification event for thread completion
# EVT_RESULT_ID = wx.NewId()

# def EVT_RESULT(win, func):
#     """Define Result Event."""
#     win.Connect(-1, -1, EVT_RESULT_ID, func)

# class ResultEvent(wx.PyEvent):
#     """Simple event to carry arbitrary result data."""
#     def __init__(self, data):
#         """Init Result Event."""
#         wx.PyEvent.__init__(self)
#         self.SetEventType(EVT_RESULT_ID)
#         self.data = data

# # Thread class that executes processing
# class WorkerThread(Thread):
#     """Worker Thread Class."""
#     def __init__(self, notify_window):
#         """Init Worker Thread Class."""
#         Thread.__init__(self)
#         self._notify_window = notify_window
#         self._want_abort = 0
#         # This starts the thread running on creation, but you could
#         # also make the GUI thread responsible for calling this
#         self.start()

#     def run(self):
#         """Run Worker Thread."""
#         # This is the code executing in the new thread. Simulation of
#         # a long process (well, 10s here) as a simple loop - you will
#         # need to structure your processing so that you periodically
#         # peek at the abort variable
#         for i in range(10):
#             time.sleep(1)
#             if self._want_abort:
#                 # Use a result of None to acknowledge the abort (of
#                 # course you can use whatever you'd like or even
#                 # a separate event type)
#                 wx.PostEvent(self._notify_window, ResultEvent(None))
#                 return
#         # Here's where the result would be returned (this is an
#         # example fixed result of the number 10, but it could be
#         # any Python object)
#         wx.PostEvent(self._notify_window, ResultEvent(10))

#     def abort(self):
#         """abort worker thread."""
#         # Method for use by main thread to signal an abort
#         self._want_abort = 1

# # GUI Frame class that spins off the worker thread
# class MainFrame(wx.Frame):
#     """Class MainFrame."""
#     def __init__(self, parent, id):
#         """Create the MainFrame."""
#         wx.Frame.__init__(self, parent, id, 'Thread Test')

#         # Dumb sample frame with two buttons
#         wx.Button(self, ID_START, 'Start', pos=(0,0))
#         wx.Button(self, ID_STOP, 'Stop', pos=(0,50))
#         self.status = wx.StaticText(self, -1, '', pos=(0,100))

#         self.Bind(wx.EVT_BUTTON, self.OnStart, id=ID_START)
#         self.Bind(wx.EVT_BUTTON, self.OnStop, id=ID_STOP)

#         # Set up event handler for any worker thread results
#         EVT_RESULT(self,self.OnResult)

#         # And indicate we don't have a worker thread yet
#         self.worker = None

#     def OnStart(self, event):
#         """Start Computation."""
#         # Trigger the worker thread unless it's already busy
#         if not self.worker:
#             self.status.SetLabel('Starting computation')
#             self.worker = WorkerThread(self)

#     def OnStop(self, event):
#         """Stop Computation."""
#         # Flag the worker thread to stop if running
#         if self.worker:
#             self.status.SetLabel('Trying to abort computation')
#             self.worker.abort()

#     def OnResult(self, event):
#         """Show Result status."""
#         if event.data is None:
#             # Thread aborted (using our convention of None return)
#             self.status.SetLabel('Computation aborted')
#         else:
#             # Process results here
#             self.status.SetLabel('Computation Result: %s' % event.data)
#         # In either event, the worker is done
#         self.worker = None

# class MainApp(wx.App):
#     """Class Main App."""
#     def OnInit(self):
#         """Init Main App."""
#         self.frame = MainFrame(None, -1)
#         self.frame.Show(True)
#         self.SetTopWindow(self.frame)
#         return True

# if __name__ == '__main__':
#     app = MainApp(0)
#     app.MainLoop()

# Hilo a arrancar
# class MiHilo(Thread):
#     # Se le pasa un numero identificador del hilo y un event
#     def __init__(self, evento):
#         Thread.__init__(self)
#         self.evento=evento

#     # Espera al event
#     def run(self):
#         self.evento.wait()
#         print "Entra hilo "

# if __name__ == '__main__':
#     # Crea el evento
#     evento = Event()
#     # Arranca el hilo
#     hilo=MiHilo(evento)
#     hilo.start()
#     # Espera dos segundos y activa el evento
#     time.sleep(2)
#     print "Hago evento.set()"
#     evento.set()

# class Test(Thread):
#     def __init__(self, evento):
#         Thread.__init__(self)
#         self.start()
#         self.evento = evento
#     def run(self):
#         self.evento.wait()
#         self.hola = self.evento.getopt()
#         print "evento contiene -> ", self.hola
#         # print "TEST START"
#         # for i in range(10):
#         #     print "->", str(i).encode('utf-8')
#         #     time.sleep(1)
#         # print "TEST END"


# class Frame(wx.Frame):
#     def __init__(self):
#         wx.Frame.__init__(self, None, title="X", size=(350,200))
#         p = wx.Panel(self)
#         bOnOpen = wx.Button(p, -1, "open cam", pos=(10,10))
#         bOnOpen.Bind(wx.EVT_BUTTON, onOpenCam)
#         bOnOpenImg = wx.Button(p, -1, "open Img", pos=(10,60))
#         bOnOpenImg.Bind(wx.EVT_BUTTON, onOpenImg)
#         bOnOpenVid = wx.Button(p, -1, "open video", pos=(10,110))
#         bOnOpenVid.Bind(wx.EVT_BUTTON, onOpenVid)
#         self.Show()

# app = wx.App(redirect=False)
# app.SetTopWindow(Frame())
# app.MainLoop()
# #--- EOF
# experiment with wxPython's
# wx.media.MediaCtrl(parent, id, pos, size, style, backend)
# the backend (szBackend) is usually figured by the control
# wxMEDIABACKEND_DIRECTSHOW   Windows
# wxMEDIABACKEND_QUICKTIME    Mac OS X
# wxMEDIABACKEND_GSTREAMER    Linux (?)
# plays files with extension .mid .mp3 .wav .au .avi .mpg
# tested with Python24 and wxPython26 on Windows XP   vegaseat  10mar2006

# import threading,wx

# ID_RUN=101
# ID_RUN2=102

# class MyFrame(wx.Frame):
#     def __init__(self, parent, ID, title):
#         wx.Frame.__init__(self, parent, ID, title)
#         panel = wx.Panel(self, -1)
#         mainSizer=wx.BoxSizer(wx.HORIZONTAL)
#         mainSizer.Add(wx.Button(panel, ID_RUN, "Click me"))
#         mainSizer.Add(wx.Button(panel, ID_RUN2, "Click me too"))
#         panel.SetSizer(mainSizer)
#         mainSizer.Fit(self)
#         wx.EVT_BUTTON(self, ID_RUN, self.onRun)
#         wx.EVT_BUTTON(self, ID_RUN2, self.onRun2)

#     def onRun(self,event):
#         print "Clicky!"
#         wx.CallAfter(self.AfterRun, "I don't appear until after OnRun exits")
#         s=raw_input("Enter something:")
#         print s

#     def onRun2(self,event):
#         t=threading.Thread(target=self.__run)
#         t.start()

#     def __run(self):
#         wx.CallAfter(self.AfterRun, "I appear immediately (event handler\n"+ "exited when OnRun2 finished)")
#         s=raw_input("Enter something in this thread:")
#         print s

#     def AfterRun(self,msg):
#         dlg=wx.MessageDialog(self, msg, "Called after", wx.OK | wx.ICON_INFORMATION)
#         dlg.ShowModal()
#         dlg.Destroy()


# class MyApp(wx.App):
#     def OnInit(self):
#         frame = MyFrame(None, -1, "CallAfter demo")
#         frame.Show(True)
#         frame.Centre()
#         return True

# app = MyApp(0)
# app.MainLoop()

# import threading

# class MainFrame(wx.Frame):

#     def __init__(self, parent):
#         wx.Frame.__init__(self, parent, title='CallAfter example')

#         panel = wx.Panel(self)
#         self.label = wx.StaticText(panel, label="Ready")
#         self.btn = wx.Button(panel, label="Start")
#         self.gauge = wx.Gauge(panel)

#         sizer = wx.BoxSizer(wx.VERTICAL)
#         sizer.Add(self.label, proportion=1, flag=wx.EXPAND)
#         sizer.Add(self.btn, proportion=0, flag=wx.EXPAND)
#         sizer.Add(self.gauge, proportion=0, flag=wx.EXPAND)

#         panel.SetSizerAndFit(sizer)
#         self.Bind(wx.EVT_BUTTON, self.OnButton)

#     def OnButton(self, event):
#         """ This event handler starts the separate thread. """
#         self.btn.Enable(False)
#         self.gauge.SetValue(0)
#         self.label.SetLabel("Running")

#         thread = threading.Thread(target=self.LongRunning)
#         thread.start()

#     def OnLongRunDone(self):
#         self.gauge.SetValue(100)
#         self.label.SetLabel("Done")
#         self.btn.Enable(True)

#     def LongRunning(self):
#         """This runs in a different thread.  Sleep is used to
#          simulate a long running task."""
#         time.sleep(3)
#         wx.CallAfter(self.gauge.SetValue, 20)
#         time.sleep(5)
#         wx.CallAfter(self.gauge.SetValue, 70)
#         time.sleep(4)
#         wx.CallAfter(self.OnLongRunDone)

# if __name__ == "__main__":
#     app = wx.App(0)
#     frame = MainFrame(None)
#     frame.Show()
#     app.MainLoop()

# def sumar(a, b):
#     return a + b

# def restar(a, b):
#     return a - b

# def multiplicar(a, b):
#     return a * b

# num1 = raw_input("Num1: ")
# num2 = raw_input("Num2: ")

# print("Opciones\n1.- Sumar\n2.- Restar\n3.- Multiplicar")

# operaciones = {'1': sumar, '2': restar, '3': multiplicar}

# seleccion = raw_input('Escoge una: ')
# try:
#     resultado = operaciones[seleccion](int(num1), int(num2))
#     print resultado
# except:
#     print("Esa no vale")

#!/usr/bin/env python3

# Adapted from http://www.creativetux.com/2012/11/streaming-to-twitchtv-with-linux.html
#
# Make sure to put your twitch.tv key in a file called "key" in the current directory.
#
# Before running, make sure PulseAudio is set up with the correct loopback modules
# and a null sink named "mix". You can use something ilke the following commands:
#
# pactl load-module module-null-sink sink_name=mix
# pactl load-module module-loopback sink=mix
# pactl load-module module-loopback sink=mix
#
# Then go in with the `pavucontrol` utility and set the inputs for both loopbacks:
# one as a monitor of your audio out, and one for your microphone in. Do this on the
# recording tab (you may have to select "show All Streams")
#
# NOTE: for non-debian distros, change "avconv" to "ffmpeg" below, and any other
# necessary changes to the command arguments.

import cv2
import librtmp
import numpy as np

cap = cv2.VideoCapture(0)

conn = librtmp.RTMP("rtmp://moises.inf.uct.cl/live/canal1", live=True)

conn.connect()


stream = conn.create_stream()
while True:
    stream.write("img/bg.avi")
# #data = stream.read(1024)
# while True:
#     #se toma cada frame
#     ret, frame = cap.read()
#     cv2.imshow('webCam', frame)
#     stream.write(frame)

#     esc = cv2.waitKey(5) & 0xFF == 27
#     if esc:
#         break

# cap.release()
# cv2.destroyAllWindows()