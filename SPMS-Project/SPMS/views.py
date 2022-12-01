from django.shortcuts import render
from django.http import HttpResponse
from .queries import *

# Create your views here.
def home(request):
    return render(request,"SPMS.html")


def authenticate(request,username,password):
    if (isValid(username) and (password==getPassword(password))):
        if (getGroup(username)=="Student"):
            return render(request,"student_home.html")
        elif (getGroup(username)=="Faculty"):
            return render(request,"faculty_SPMS.html")
        elif (getGroup(username)=="Admin"):
            return render(request,"admin_SPMS.html")
        else :
            return render(request,"SPMS.html")

