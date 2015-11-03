import numpy
import math
import cv2


def colorclose(Cb_p,Cr_p, Cb_key, Cr_key, tola, tolb):
	temp = ((Cb_key-Cb_p)**2+(Cr_key-Cr_p)**2) **0.5
	if temp < tola:
		z= 0.0
	elif temp < tolb:
		z= ((temp-tola)/(tolb-tola))
	else:
		z= 1.0
	return z


def magic(inImg, inbg , keyColor=None, tolerance = None):

	# Change color space from RGB to YCrCb
	inDataFG = cv2.cvtColor(inImg, cv2.COLOR_RGB2YCR_CB)

	# Initialize keycolor and tolerance if it's not already set
	if keyColor == None:keyColor = inDataFG[10,10]
	if tolerance == None: tolerance = [50,130]
	[Y_key, Cb_key, Cr_key] = keyColor
	[tola, tolb]= tolerance

	
	keyColorRGB = inImg[10,10]  # Change color space from RGB to YCrCb for key Color

	(y,x,d) = inDataFG.shape # Get array dimensions
	
	maskgen = numpy.vectorize(colorclose)  # Vectorize masking function
	
	alphaMask = maskgen(inDataFG[:,:,1],inDataFG[:,:,2] ,Cb_key, Cr_key, tola, tolb) # Generate mask - broadcast
	alphaMask.shape = (y,x)  # Set mask dimensions to original image dimenssions

	invertMask = 1.0 - alphaMask # Invert mask

	alphaMask = numpy.repeat(alphaMask,3) # Create 3d array -- mulyiply size * 3
	alphaMask.shape = inDataFG.shape # set the shape as color image

	invertMask = numpy.repeat(invertMask,3)  # Create 3d array -- mulyiply size * 3
	invertMask.shape = inDataFG.shape # set the shape as color image

	# colorMask = numpy.tile([0,0,0], (y,x,1)) # Create zero array -- image size
	allKeyColor = numpy.tile(keyColorRGB, (y,x,1)) # create color image array initialized with keyColorRGB


	colorMask = allKeyColor * invertMask # BG output -- FG should be black
	cleaned = inImg - colorMask # FG output -- remove BG from input image
	inbg = numpy.uint8(inbg * invertMask + cleaned * alphaMask) # fill BG image with FG image

	# cv2.imshow('colorMask',colorMask)
	# cv2.imshow('inImg',inImg)
	# cv2.imshow('cleaned',cleaned)

	return inbg



def testPicture(background, inputPic, outputFileName = 'testPicture_out.png'):

	t1 = cv2.getTickCount()

	output = magic(inputPic,background)#, tolerance=[10,20])

	t2 = cv2.getTickCount()
	print 'testPicture processed in {0} s'.format((t2 - t1)/cv2.getTickFrequency())

	cv2.imwrite(outputFileName, output)



def testWebcam(background):

	# capture object
	cap = cv2.VideoCapture(0)

	while(True):
		
		# Capture frame-by-frame
		ret, frame = cap.read()

		output = magic(frame,background, tolerance=[10,20])

		# Display the resulting frame
		cv2.imshow('frame',frame)
		cv2.imshow('output',output)

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	# When everything done, release the capture
	cap.release()
	cv2.destroyAllWindows()






if __name__ == '__main__':

	background = cv2.imread('colombia_640.png',1)
	inputPic = cv2.imread('bgInCol.jpg',1)

	testPicture(background, inputPic)
	testWebcam(background)