from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from SPMS import queries
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import plot
# Create your views here.
def home(request):
    plot_div = OneTraceSpider([1,2,3,4,5,6],["banna","inja","jaima","niaz","akib","faiza"])
    return render(request,"SPMS.html", context={"plot1":plot_div,"page":"dashboard"})

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
    return render(request,"co-plo-analysis.html",{"page":"coplo"})

def coursePloAnal(request):
    return render(request,"course-plo-analysis.html",{"page":"course"})

def PloAchievement(request):
    return render(request,"PloAchievement.html",{"page":"plo"})

def QuestionBank(request):
    return render(request,"QuestionBank.html",{"page":"ques"})


## Creating Graphs

def OneTraceSpider(rl,tl):
    fig = go.Figure(data=go.Scatterpolar(
        r = rl,
        theta = tl,
        fill='toself'
    ))
    return plot(fig, output_type='div',include_plotlyjs=True)


