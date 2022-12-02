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

    return render(request,"SPMS.html", context={"plot1":plot_div,
                                                "page":"dashboard",
                                                "id":queries.getCurrUser()[0],
                                                "group":queries.getCurrUser()[1],
                                                "name":queries.getCurrUser()[0]})

def authenticate(request):
    username=request.POST.get("userid")
    password=request.POST.get("password")
    if queries.isValid(username)==True:
        passwords = queries.getPassword(username)
        if passwords==password:
            queries.setCurrUser(username)
            group=queries.getGroup(1416455)
            return home(request)
        else:
            return HttpResponse("error")
    else:
        return HttpResponse("error")

def login(request):
    return render(request, "login.html")

def logout(request):
    queries.deleteCurrUser()
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

def StuPloAnal(request):
    return render(request,"StuPloAnal.html",{"page":"stuplo-anal"})

def StuPloTbl(request):
    return render(request,"StuPloTbl.html",{"page":"stuplo-tbl"})

def CourseReport(request):
    return render(request,"CourseReport.html",{"page":"coursereport"})

def QuestionBankEntry(request):
    return render(request,"QuestionBankEntry.html",{"page":"quesentry"})

def COentry(request):
    return render(request,"COentry.html",{"page":"coentry"})

## Creating Graphs

def OneTraceSpider(rl,tl):
    fig = go.Figure(data=go.Scatterpolar(
        r = rl,
        theta = tl,
        fill='toself'
    ))
    return plot(fig, output_type='div',include_plotlyjs=True)


