from django.shortcuts import render
from django.http import HttpResponse
from SPMS import queries
# Create your views here.
def home(request):
    return render(request,"SPMS.html")
def authenticate(request):
    username=request.POST.get("userid")
    password=request.POST.get("password")
    if queries.isValid(username):
        if queries.getPassword(username)==password:
            return home(request)
    else:
        return HttpResponse("error")
def login(request):
    return render(request, "login.html")

