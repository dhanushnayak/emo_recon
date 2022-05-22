import numpy as np
import cv2 as cv
from deepface import DeepFace
import os

class EMO_DATA():
    def __init__(self) -> None:
        self.cap = cv.VideoCapture(0)
        if not self.cap.isOpened():
            print("Cannot open camera")
            exit()
            

    def get_data(self):
        

        c = 0
        path = 'output.jpg'
        while True:
            # Capture frame-by-frame
            ret, frame = self.cap.read()
            # if frame is read correctly ret is True
            
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break
            # Our operations on the frame come here
            
            # Display the resulting frame
            if c == 100 :

                cv.imwrite(path,frame)
                print('Captured')
            #cv.imshow('frame', frame)
            c+=1
            if cv.waitKey(1) == ord('q') or c==150:
                break
        # When everything done, release the capture
        self.cap.release()
        cv.destroyAllWindows()

        obj = DeepFace.analyze(img_path = path, actions =  ['emotion'],enforce_detection=False)
        if obj and os.path.isfile(path): os.remove(path)
        return obj