from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse("Whatever")

def login(request):
    return render(request,"SPMS/login.html")

