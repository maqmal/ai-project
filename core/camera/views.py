from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse,StreamingHttpResponse,HttpResponseServerError
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators import gzip

from camera.forms import UserForm,UserProfileInfoForm
from camera.opencv import VideoCamera, FaceDetect

# Create your views here.
def index(request):
    return render(request,'camera/index.html')

@login_required
def login_succsess(request):
    return HttpResponse("You are logged in !")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'user_pic' in request.FILES:
                print('found it')
                profile.user_pic = request.FILES['user_pic']
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request,'camera/registration.html',{'user_form':user_form,'profile_form':profile_form,'registered':registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")

    else:
        return render(request, 'camera/login.html', {})


def generator(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@gzip.gzip_page
def camera_feed(request):
    return StreamingHttpResponse(generator(VideoCamera()),content_type="multipart/x-mixed-replace;boundary=frame")

@gzip.gzip_page
def face_detect(request):
    return StreamingHttpResponse(generator(FaceDetect()),content_type="multipart/x-mixed-replace;boundary=frame")