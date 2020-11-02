from camera import views
from django.urls import path,include

app_name = 'camera'

urlpatterns=[
    path('register/',views.register,name='register'),
    path('user_login/',views.user_login,name='user_login'),

    path('camera_feed/',views.camera_feed, name='camera_feed'),
    path('face_detect/',views.face_detect, name='face_detect'),
]