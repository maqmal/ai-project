from django.http import HttpResponse,StreamingHttpResponse, HttpResponseServerError
from django.shortcuts import render
from django.conf import settings
import cv2
import os
import numpy as np

faceDetect = cv2.CascadeClassifier(os.path.join(settings.BASE_DIR,'haarcascade/haarcascade_frontalface_default.xml'))

class VideoCamera(object):
    def __init__(self):
        self.capture = cv2.VideoCapture(0)
    def __del__(self):
        self.capture.release()
    def get_frame(self):
        _,frame = self.capture.read()
        resize_frame = cv2.resize(frame, (640, 480), interpolation = cv2.INTER_LINEAR) 
        _,jpeg = cv2.imencode('.jpg',resize_frame)
        return jpeg.tobytes() 
    
class FaceDetect(object):
    def __init__(self):
        self.capture = cv2.VideoCapture(0)
    def __del__(self):
        self.capture.release()
    def get_frame(self):
        _,frame = self.capture.read()
        resize_frame = cv2.resize(frame, (640, 480), interpolation = cv2.INTER_LINEAR) 
        gray = cv2.cvtColor(resize_frame,cv2.COLOR_BGR2GRAY)
        face_detected = faceDetect.detectMultiScale(gray,1.3,5)
        for (x,y,w,h) in face_detected:
            cv2.rectangle(resize_frame,(x,y), (x+w,y+h),(0,255,0),2)
        _,jpeg = cv2.imencode('.jpg',resize_frame)
        return jpeg.tobytes() 
    


