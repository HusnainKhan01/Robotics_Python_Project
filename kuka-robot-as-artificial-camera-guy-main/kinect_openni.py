# needs https://structure.io/openni
# much is taken from https://github.com/severin-lemaignan/openni-python

from openni import openni2
import numpy as np
import cv2
import time

isCalibrate = False
onLoadTime = None
class FixedPositionCamera:
    def __init__(self):
        openni2.initialize() # can also accept the path of the OpenNI redistribution
        dev = openni2.Device.open_any()
        dev.set_depth_color_sync_enabled(True)
        self.depth_stream = dev.create_depth_stream()
        self.depth_stream.start()
        self.color_stream = dev.create_color_stream()
        self.color_stream.start()
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        
    def get_face_and_depth_info(self): 
        info = []
        depth_frame = self.depth_stream.read_frame()
        depth_data = depth_frame.get_buffer_as_uint16()
        depth_img1 = np.ndarray((depth_frame.height, depth_frame.width), dtype=np.uint16, buffer=depth_data).astype(np.float32)
        depth_img = depth_img1/10.0 # convert to meters 
        cv2.imshow("Depth", depth_img-.5) # uniform shift by 0.5 m distance for better display
        # print('start=', depth_img[depth_frame.height//2,depth_frame.width//2]) ## access one distance sample from the middle
        color_frame = self.color_stream.read_frame()
        color_data = color_frame.get_buffer_as_uint8()
        color_img = np.ndarray((color_frame.height, color_frame.width, 3), dtype=np.uint8, buffer=color_data)
        # Convert to grayscale
        gray = cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY)
        # Detect the faces
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        # Draw the rectangle around each face
        for (x, y, w, h) in faces:
            cv2.rectangle(color_img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = color_img[y:y+h, x:x+w]
            eyes = self.eye_cascade.detectMultiScale(roi_gray)
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
            height = int(y+(h/2))
            width = int(x+(w/2))
            depth = depth_img[height, width]
            if depth == 0.0:
                continue
            info_new = openni2.convert_depth_to_world(self.depth_stream, height, width, depth)
            #print("info_new= ", info_new)
            info.extend([height, width, float("{:.2f}".format(depth))])
        # Display
        cv2.imshow("Color", color_img[...,::-1])    
        yield info
        
    def close_frames(self):
        self.depth_stream.stop()
        self.color_stream.stop()
        openni2.unload()