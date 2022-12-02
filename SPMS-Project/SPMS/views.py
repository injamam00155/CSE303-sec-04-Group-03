from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from SPMS import queries
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import plot
# Create your views here.
def home(request):
    fig = go.Figure(data=go.Scatterpolar(
        r = [1,2,3,4,5,6],
        theta = ["banna","inja","jaima","niaz","akib","faiza"],
        fill='toself'
    ))
    plot_div = plot(fig, output_type='div',include_plotlyjs=True)
    return render(request,"base.html", context={"plot1":plot_div})

def authenticate(request):
    username=request.POST.get("userid")
    password=request.POST.get("password")
    if queries.isValid(username)==True:
        passwords = queries.getPassword(username)
        if passwords==password:
            return home(request)
        else:
            return HttpResponse("error")
    else:
        return HttpResponse("error")

def login(request):
    return render(request, "login.html")

def logout(request):
    return render(request,"login.html")

def dashboard(request):
    return render(request,"SPMS.html")

def CoPloAnal(request):
    return render(request,"co-plo-analysis.html")

def coursePloAnal(request):
    return render(request,"course-plo-analysis.html")

def PloAchievement(request):
    return render(request,"PloAchievement.html")

def QuestionBank(request):
    return render(request,"QuestionBank.html")
