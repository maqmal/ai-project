from django.http import HttpResponse,StreamingHttpResponse, HttpResponseServerError
from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.models import User
import face_recognition, os, cv2, glob
import numpy as np
from multiprocessing import Pool

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
    

def face_encode():
    known_face_encodings = []
    known_faces_filenames = []
    image_dir = os.path.join(settings.MEDIA_DIR)
    
    if os.path.exists(image_dir) and os.path.isdir(image_dir):  
        if not os.listdir(image_dir):
            print("IMAGE DIRECTORY NOT FOUND")
        else:
            for file in glob.glob('media/user_pic/*.jpg'):
                filenames = file[15:]
                known_faces_filenames.append(filenames)

    for filename in known_faces_filenames:
        face = face_recognition.load_image_file(os.path.join(settings.BASE_DIR,"media//user_pic/",filename))
        known_face_encodings.append(face_recognition.face_encodings(face)[0])
    return known_face_encodings

def knowm_face():
    known_face_names = []
    user_list = User.objects.values()
    # for i in range(len(user_list)):
    #     known_face_names.append(user_list[i]['username'])
    known_face_names.append(user_list[2]['username'])
    known_face_names.append(user_list[4]['username'])
    return known_face_names


def draw_face(frame):
    resize_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    face_locations = []
    face_encodings = []
    face_names = []
    name = []
    
    known_face_encodings = face_encode()
    known_face_names = knowm_face()
    rgb_small_frame = cv2.cvtColor(resize_frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    face_names = []
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name="Unkown"

        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)

        if matches[best_match_index]:
            name = known_face_names[best_match_index]
        face_names.append(name)

    return name,face_locations,face_names

    

class FaceDetect(object):
    def __init__(self):
        self.capture = cv2.VideoCapture(0)
        self.name = []
        self.face_locations = []
        self.face_names = []
        self.justrun = True
    def __del__(self):
        self.capture.release()
    def get_frame(self):
        _,frame = self.capture.read()
        resize_frame = cv2.resize(frame, (640, 480), interpolation = cv2.INTER_LINEAR) 
        
        self.name,self.face_locations,self.face_names = draw_face(resize_frame)
        
        for (top, right, bottom, left), self.name in zip(self.face_locations, self.face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(resize_frame, (left, top), (right, bottom), (0, 255, 0), 2)

            cv2.rectangle(resize_frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(resize_frame, self.name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)
            
        _,jpeg = cv2.imencode('.jpg',resize_frame)
        return jpeg.tobytes() 


# def recognition(imagename):
#     known_face_encodings = []
#     known_face_names = []
#     known_faces_filenames = []
#     image_dir = os.path.join(settings.MEDIA_DIR)
    
#     if os.path.exists(image_dir) and os.path.isdir(image_dir):  
#         if not os.listdir(image_dir):
#             print("IMAGE DIRECTORY NOT FOUND")
#         else:
#             for file in glob.glob('media/user_pic/*.jpg'):
#                 filenames = file[15:]
#                 known_faces_filenames.append(filenames)

#     for filename in known_faces_filenames:
#         face = face_recognition.load_image_file(os.path.join(settings.BASE_DIR,"media//user_pic/",filename))
#         known_face_names.append(filename)
#         known_face_encodings.append(face_recognition.face_encodings(face)[0])
    
#     face_locations = []
#     face_encodings = []
#     face_names = []
#     imagename_new =  face_recognition.load_image_file(imagename)
#     face_locations = face_recognition.face_locations(imagename_new)
#     face_encodings = face_recognition.face_encodings(imagename_new, face_locations)

#     face_names = []

#     for face_encoding in face_encodings:
#         matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
#         name = "Unknown"

#         face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
#         best_match_index = np.argmin(face_distances)
#         if matches[best_match_index]:
#             name = known_face_names[best_match_index]

#         face_names.append(name)

#     return name