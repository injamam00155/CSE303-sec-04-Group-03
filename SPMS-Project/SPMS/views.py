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

    return render(request,"Student/sHome.html", context={"plot1":plot_div,
                                                "page":"dashboard",
                                                "id":queries.getCurrUser()[0],
                                                "group":queries.getCurrUser()[1],
                                                "name":queries.getName(str(queries.getCurrUser()[0]))})

def authenticate(request):
    username=request.POST.get("userid")
    password=request.POST.get("password")
    if queries.isValid(username)==True:
        passwords = queries.getPassword(username)
        if passwords==password:
            queries.setCurrUser(username)
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
    return render(request,"Student/sHome.html")

def CoPloAnal(request):
    # queries.getStudentCourseWiseCO(queries.getCurrUser()[0],)
    return render(request,"Student/co-plo-analysis.html",{"page":"coplo",
                                                "page":"dashboard",
                                                "id":queries.getCurrUser()[0],
                                                "group":queries.getCurrUser()[1],
                                                "name":queries.getName(str(queries.getCurrUser()[0]))})

def coursePloAnal(request):
    return render(request,"Student\course-plo-analysis.html",{"page":"course",
                                                "page":"dashboard",
                                                "id":queries.getCurrUser()[0],
                                                "group":queries.getCurrUser()[1],
                                                "name":queries.getName(str(queries.getCurrUser()[0]))})

def PloAchievement(request):
    return render(request,"Student\PloAchievement.html",{"page":"plo",
                                                "page":"dashboard",
                                                "id":queries.getCurrUser()[0],
                                                "group":queries.getCurrUser()[1],
                                                "name":queries.getName(str(queries.getCurrUser()[0]))})

def QuestionBank(request):
    return render(request,"Student\QuestionBank.html",{"page":"ques",
                                                "page":"dashboard",
                                                "id":queries.getCurrUser()[0],
                                                "group":queries.getCurrUser()[1],
                                                "name":queries.getName(str(queries.getCurrUser()[0]))})

def StuPloAnal(request):
    return render(request,"Faculty\StuPloAnal.html",{"page":"stuplo-anal",
                                                "page":"dashboard",
                                                "id":queries.getCurrUser()[0],
                                                "group":queries.getCurrUser()[1],
                                                "name":queries.getName(str(queries.getCurrUser()[0]))})

def StuPloTbl(request):
    return render(request,"Faculty\StuPloTbl.html",{"page":"stuplo-tbl",
                                                "page":"dashboard",
                                                "id":queries.getCurrUser()[0],
                                                "group":queries.getCurrUser()[1],
                                                "name":queries.getName(str(queries.getCurrUser()[0]))})

def CourseReport(request):
    return render(request,"Faculty\CourseReport.html",{"page":"coursereport",
                                                "page":"dashboard",
                                                "id":queries.getCurrUser()[0],
                                                "group":queries.getCurrUser()[1],
                                                "name":queries.getName(str(queries.getCurrUser()[0]))})

def QuestionBank(request):
    return render(request,"Student\QuestionBank.html",{"page":"quesentry",
                                                "page":"dashboard",
                                                "id":queries.getCurrUser()[0],
                                                "group":queries.getCurrUser()[1],
                                                "name":queries.getName(str(queries.getCurrUser()[0]))})
def QuestionBankEntry(request):
    context={
            "page":"quesentry",
            "id":queries.getCurrUser()[0],
            "group":queries.getCurrUser()[1],
            "name":queries.getName(str(queries.getCurrUser()[0]))}
    return render(request,"Faculty\QuestionBankEntry.html",context)

def COentry(request):
    context={
            "page":"dashboard",
            "id":queries.getCurrUser()[0],
            "group":queries.getCurrUser()[1],
            "name":queries.getName(str(queries.getCurrUser()[0]))}
    return render(request,"Faculty\COentry.html",context)

## Creating Graphs

def OneTraceSpider(rl,tl):
    fig = go.Figure(data=go.Scatterpolar(
        r = rl,
        theta = tl,
        fill='toself'
    ))
    return plot(fig, output_type='div',include_plotlyjs=True)


