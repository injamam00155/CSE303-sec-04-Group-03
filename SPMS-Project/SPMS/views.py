from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from SPMS import queries
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import plot




# Create your views here.

def PloAchieve(user_id):
    # fig = px.bar(x=queries.getStudentWisePLO(user_id)[0], y=queries.getStudentWisePLO(user_id)[1])
    # fig = px.bar(queries.getStudentWisePLO(user_id))
    fig = px.bar(
        x=queries.getStudentWisePLO(user_id)[0], 
        y=queries.getStudentWisePLO(user_id)[1],
        labels={'x':'PLO ID','y':'Percentage Achieved'})
    PloAchievement=fig.to_html()
    return PloAchievement

def home(request):
    # plot_div = OneTraceSpider([1,2,3,4,5,6],["banna","inja","jaima","niaz","akib","faiza"])
    student_id=queries.getCurrUser()[0][0]
    context={
        "page":"dashboard",
        "id":student_id,
        "group":queries.getCurrUser()[0][1],
        "name":queries.getName(str(queries.getCurrUser()[0][0])),
        "PloAchievement":PloAchieve(student_id),
        "COAchievement":OneTraceSpider(queries.getStudentWiseCLO(student_id)[1],queries.getStudentWiseCLO(student_id)[0]),
        "PLOAchievePercent":OneTraceSpider(queries.getStudentWisePLO(student_id)[1],queries.getStudentWisePLO(student_id)[0])
        }
        
    return render(request,"Student/sHome.html", context)

def authenticate(request):
    userID=request.POST.get("userid")
    password=request.POST.get("password")
    if queries.isValid(userID)==True:
        passwords = queries.getPassword(userID)
        if passwords==password:
            queries.setCurrUser(userID)
            return home(request)
        else:
            return HttpResponse("error")
    else:
        return HttpResponse("error")

def login(request):
    return render(request, "login.html")

def logout(request):
    queries.deleteCurrUser()
    return redirect("/")

def dashboard(request):
    return render(request,"Student/sHome.html")

def CoPloAnal(request):
    # queries.getStudentCourseWiseCO(queries.getCurrUser()[0][0],"CSE101")
    context={
            "page":"coplo",
        "id":queries.getCurrUser()[0][0],
        "group":queries.getCurrUser()[0][1],
        "name":queries.getName(str(queries.getCurrUser()[0][0])),
            }
    return render(request,"Student/co-plo-analysis.html",context)

def coursePloAnal(request):
    context={
            "page":"course",
        "id":queries.getCurrUser()[0][0],
        "group":queries.getCurrUser()[0][1],
        "name":queries.getName(str(queries.getCurrUser()[0][0])),
            }
    return render(request,"Student\course-plo-analysis.html",context)

def PloAchievement(request):
    context={
        "page":"plo",
        "id":queries.getCurrUser()[0][0],
        "group":queries.getCurrUser()[0][1],
        "name":queries.getName(str(queries.getCurrUser()[0][0])),
        }
    return render(request,"Student\PloAchievement.html",context)

def QuestionBank(request):
    context={
        "page":"ques",
        "id":queries.getCurrUser()[0][0],
        "group":queries.getCurrUser()[0][1],
        "name":queries.getName(str(queries.getCurrUser()[0][0])),
        }
    return render(request,"Student\QuestionBank.html",context)

def StuPloAnal(request):
    context={
        "page":"stuplo-anal",
        "id":queries.getCurrUser()[0][0],
        "group":queries.getCurrUser()[0][1],
        "name":queries.getName(str(queries.getCurrUser()[0][0])),
        }
    return render(request,"Faculty\StuPloAnal.html",context)

def StuPloTbl(request):
    context={
        {"page":"stuplo-tbl",
        "id":queries.getCurrUser()[0][0],
        "group":queries.getCurrUser()[0][1],
        "name":queries.getName(str(queries.getCurrUser()[0][0])),
        }
    }
    return render(request,"Faculty\StuPloTbl.html",context)

def CourseReport(request):
    context={
        "page":"coursereport",                                                
        "id":queries.getCurrUser()[0][0],
        "group":queries.getCurrUser()[0][1],
        "name":queries.getName(str(queries.getCurrUser()[0][0])),
        }
    return render(request,"Faculty\CourseReport.html",context)

def QuestionBank(request):
    context={
        "page":"ques",
        "id":queries.getCurrUser()[0][0],
        "group":queries.getCurrUser()[0][1],
        "name":queries.getName(str(queries.getCurrUser()[0][0])),
        }
    return render(request,"Student\QuestionBank.html",context)
    
def QuestionBankEntry(request):
    context={
            "page":"quesentry",
            "id":queries.getCurrUser()[0][0],
            "group":queries.getCurrUser()[0][1],
            "department":queries.getCurrDept(),
            "name":queries.getName(str(queries.getCurrUser()[0][0])),
            }
    return render(request,"Faculty\QuestionBankEntry.html",context)

def COentry(request):
    context={
            "page":"dashboard",
            "id":queries.getCurrUser(),
            "group":queries.getCurrUser(),
            "name":queries.getName(str(queries.getCurrUser()[0][0])),
            }
    return render(request,"Faculty\COentry.html",context)

def ProgramW(request):
    context={
            "page":"ProgramW",
            "id":queries.getCurrUser()[0],
            "group":queries.getCurrUser()[1],
            "name":queries.getName(str(queries.getCurrUser()[0])),
            }
    return render(request,"Faculty\ProgramW.html",context)

def departmentWise(request):
    context={
            "page":"departmentWise",
            "id":queries.getCurrUser()[0],
            "group":queries.getCurrUser()[1],
            "name":queries.getName(str(queries.getCurrUser()[0])),
            }
    return render(request,"Faculty\departmentWise.html",context)

## Creating Graphs

def OneTraceSpider(rl,tl):
    fig = go.Figure(data=go.Scatterpolar(
        r = rl,
        theta = tl,
        fill='toself'
    ))
    fig=fig.to_html()
    return fig

def TwoTraceSpider(t,r1,r2):
    fig=go.figure()
    fig.add_trace(data=go.Scatterpolar(
        r = r1,
        theta = t,
        fill='toself'
        name="You"
    ))
    fig.add_trace(data=go.Scatterpolar(
        r = r2,
        theta = t,
        fill='toself'
        name="Department Average"
    ))
    return plot(fig, output_type='div',include_plotlyjs=True)


