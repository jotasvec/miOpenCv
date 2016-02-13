#pruebaVideo.py recorder

""" app prueba para grabar desde la webcam y guardarlo en un video, para posteriormente
    el video ser usado en otro lado por ejemplo en el chroma """

#import numpy as np
import cv2


cap = cv2.VideoCapture(0)
width, height = (640,480)

#fourcc = cv2.cv.CV_FOURCC(*'XDIV')
fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
out = cv2.VideoWriter('img/output.avi',fourcc, 20, (width,height))


while(cap.isOpened()):
    ret, frame = cap.read()
    if ret:
        frame = cv2.flip(frame,1,frame)

        # write the flipped frame
        out.write(frame)

        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    else:
        break


# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()