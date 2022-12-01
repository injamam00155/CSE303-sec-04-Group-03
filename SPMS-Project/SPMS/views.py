from django.shortcuts import render
from django.http import HttpResponse
from .queries import *

# Create your views here.
def home(request):
    getStudentCGPA()
    return render(request,"SPMS.html")

