#pruebaForegroundExt.py
#aqui veremos Interactive Foreground Extraction using GrabCut Algorithm
#la idea es identificar el contorno de una persona y poner la imagen "verde" detras para el efecto chroma
#force chromakey in any video
#https://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_imgproc/py_grabcut/py_grabcut.html#grabcut
'''
Simply display the contents of the webcam with optional mirroring using OpenCV
via the new Pythonic cv2 interface.  Press <esc> to quit.
'''

import cv2

def show_webcam(mirror=False):
	cam = cv2.VideoCapture(0)
	while True:
		ret_val, img = cam.read()
		if mirror:
			img = cv2.flip(img, 1)
		img2 = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)
		cv2.imshow('my webcam', img)
		cv2.imshow('my webcam2', img2)

		if cv2.waitKey(1) == 27:
			break  # esc to quit
	cv2.destroyAllWindows()

def main():
	show_webcam(mirror=True)

if __name__ == '__main__':
	main()