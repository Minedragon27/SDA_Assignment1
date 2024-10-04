import cv2
import numpy as np
from Shape import *

class Camera:
    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.vid_capture = cv2.VideoCapture(self.camera_index, cv2.CAP_DSHOW)
        self.captured_image_path = 'captured_image.jpg'

    def setResolution(self):
        pass

    def getImage(self):
        if not self.vid_capture.isOpened():
            print("Error opening the webcam")
            return
        while self.vid_capture.isOpened():
            ret, frame = self.vid_capture.read()
            if ret:                
                cv2.imshow('Webcam Feed', frame)
                key = cv2.waitKey(20)
                if key == ord('d'):
                    cv2.imshow(self.captured_image_path, frame)
                    print(f"Image captured and saved as '{self.captured_image_path}'")
                    break
                elif key == ord('q'):
                    break
            else:
                break

        self.vid_capture.release()
        cv2.destroyAllWindows()

    def getShapes(self, image):
        pass

    def setResolution(self, width, height):
        pass

webcam = Camera()
webcam.getImage() 




