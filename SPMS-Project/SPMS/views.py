from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from SPMS import queries
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import plot
import plotly.figure_factory as ff
from io import BytesIO
# from xhtml2pdf import pisa





# Create your views here.

def PloAchieve(user_id):
    # fig = px.bar(x=queries.getStudentWisePLO(user_id)[0], y=queries.getStudentWisePLO(user_id)[1])
    # fig = px.bar(queries.getStudentWisePLO(user_id))
    fig = px.bar(
        x=queries.getStudentWisePLO(user_id)[0], 
        y=queries.getStudentWisePLO(user_id)[1],
        labels={'x':'PLO ID','y':'Percentage Achieved'})
    return plot(fig, output_type='div',include_plotlyjs=True)

def home(request):  
    user_id=queries.getCurrUser()[0][0]
    user_dept=queries.getDept(user_id)
    context={
        "page":"dashboard",
        "id":user_id,
        "group":queries.getCurrUser()[0][1],
        "name":queries.getName(str(queries.getCurrUser()[0][0])),
        "department":queries.getDept(queries.getCurrUser()[0][0]),
        "PLOAchievement":PloAchieve(user_id),
        "COAchievement":OneTraceSpider(queries.getStudentWiseCLO(user_id)[1],queries.getStudentWiseCLO(user_id)[0]),
        "PLOAchievePercent":OneTraceSpider(queries.getStudentWisePLO(user_id)[1],queries.getStudentWisePLO(user_id)[0]),
        "GPAAnalysis":TwoTraceLineChart(queries.getStudentSemesterWiseGPA(user_id)[0],queries.getStudentSemesterWiseGPA(user_id)[1],queries.getDeptSemesterWiseGPA(user_dept)[1]),
        "PLOComparison":PloCompare(user_id)
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
    user_id=queries.getCurrUser()[0][0]
    context={
            "page":"coplo",
        "id":queries.getCurrUser()[0][0],
        "group":queries.getCurrUser()[0][1],
        "name":queries.getName(str(queries.getCurrUser()[0][0])),
        "department":queries.getDept(queries.getCurrUser()[0][0]),
        "COwisePLO":cowiseplo(user_id)
            }
    return render(request,"Student/co-plo-analysis.html",context)

def coursePloAnal(request):
    context={
            "page":"course",
        "id":queries.getCurrUser()[0][0],
        "group":queries.getCurrUser()[0][1],
        "name":queries.getName(str(queries.getCurrUser()[0][0])),
        "courseploanal":coursewiseplo(queries.getCurrUser()[0][0])
            }
    return render(request,"Student\course-plo-analysis.html",context)

def PloAchievement(request):
    context={
        "page":"plo",
        "id":queries.getCurrUser()[0][0],
        "group":queries.getCurrUser()[0][1],
        "name":queries.getName(str(queries.getCurrUser()[0][0])),
        "PloAchieveTable":PLOAchieveTable(queries.getCurrUser()[0][0]),
        "department":queries.getDept(queries.getCurrUser()[0][0]),
        }
    return render(request,"Student\PloAchievement.html",context)

def CourseOutlineData(request):
    course_id=request.GET.get('courseid')
    section_num=request.GET.get('section')
    semester=request.GET.get('semester')
    try:
        thisDictionary={
        "facultyname":queries.getCourseOutline(course_id,semester,section_num)[0]+' '+queries.getCourseOutline(course_id,semester,section_num)[1],
        "facultyemail":queries.getCourseOutline(course_id,semester,section_num)[2],
        "course_description":queries.getCourseOutline(course_id,semester,section_num)[3],
        "required_textbook":queries.getCourseOutline(course_id,semester,section_num)[4],
        "course_policy":queries.getCourseOutline(course_id,semester,section_num)[5],
        
        }
        
        return thisDictionary
    except:
        pass

# def getOutline(request):
#     course_id=request.GET.get('course_')
#     try:
#         queries.getCourseOutline(course_id,semester,section_num)
#     except:
    

# def toPDF(template,context):
#     template=get_template(template_source)
#     html=template.render(context)
#     result=BytesIO()
#     pdf=pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")),result)
#     if not pdf.err():
#         return HttpResponse(result.getvalue(),context_type="application/pdf")
#     return None

def CourseOutline(request):
        course_id=request.GET.get('courseid')
        section_num=request.GET.get('section')
        semester=request.GET.get('semester')
        context={
        "page":"cout",
        "id":queries.getCurrUser()[0][0],
        "group":queries.getCurrUser()[0][1],
        "name":queries.getName(str(queries.getCurrUser()[0][0])),
        "department":queries.getDept(queries.getCurrUser()[0][0]),
        # "facultyname":queries.getCourseOutline(course_id,semester,section_num)[0]+' '+queries.getCourseOutline(course_id,semester,section_num)[1],
        # "facultyemail":queries.getCourseOutline(course_id,semester,section_num)[2],
        # "course_description":queries.getCourseOutline(course_id,semester,section_num)[3],
        # "required_textbook":queries.getCourseOutline(course_id,semester,section_num)[4],
        # "course_policy":queries.getCourseOutline(course_id,semester,section_num)[5],
        }
        context2=CourseOutlineData(request)
        # context.update(context2)
        return render (request,"Student\CourseOutline.html",context)

def StuPloAnal(request):
    context={
        "page":"stuplo-anal",
        "id":queries.getCurrUser()[0][0],
        "group":queries.getCurrUser()[0][1],
        "name":queries.getName(str(queries.getCurrUser()[0][0])),
        "department":queries.getDept(queries.getCurrUser()[0][0]),
        }
    return render(request,"Faculty\StuPloAnal.html",context)

def StuPloTbl(request):
    context={
        {"page":"stuplo-tbl",
        "id":queries.getCurrUser()[0][0],
        "group":queries.getCurrUser()[0][1],
        "name":queries.getName(str(queries.getCurrUser()[0][0])),
        "department":queries.getDept(queries.getCurrUser()[0][0]),
        }
    }
    return render(request,"Faculty\StuPloTbl.html",context)

def CourseReport(request):
    context={
        "page":"coursereport",                                                
        "id":queries.getCurrUser()[0][0],
        "group":queries.getCurrUser()[0][1],
        "name":queries.getName(str(queries.getCurrUser()[0][0])),
        "department":queries.getDept(queries.getCurrUser()[0][0]),
        }
    return render(request,"Faculty\CourseReport.html",context)

def QTable(request):
    question=[]
    fig=[]
    course_id=request.GET.get('courseid')
    section_num=request.GET.get('section_num')
    assessment=request.GET.get('assessment')
    semester=request.GET.get('semester')
    try:
        question=queries.fetchQuestions(course_id,section_num,assessment,semester)
        df=[["Q Num","Question","Marks","Weight","CO Num"]]
        for i in range(len(question)):
            df.append(question[i])
        fig=ff.create_table(df)
        return plot(fig, output_type='div',include_plotlyjs=True)    
    except:
        pass

def QuestionBank(request):
    context={
        "page":"ques",
        "id":queries.getCurrUser()[0][0],
        "group":queries.getCurrUser()[0][1],
        "name":queries.getName(str(queries.getCurrUser()[0][0])),
        "department":queries.getDept(queries.getCurrUser()[0][0]),
        "QuestionTable":QTable(request)
        }
    return render(request,"Student\QuestionBank.html",context)
    
def QuestionBankEntry(request):
    context={
            "page":"quesentry",
            "id":queries.getCurrUser()[0][0],
            "group":queries.getCurrUser()[0][1],
            "department":queries.getCurrDept(),
            "name":queries.getName(str(queries.getCurrUser()[0][0])),
            "department":queries.getDept(queries.getCurrUser()[0][0]),
            }
    return render(request,"Faculty\QuestionBankEntry.html",context)

def COentry(request):
    context={
            "page":"dashboard",
            "id":queries.getCurrUser(),
            "group":queries.getCurrUser(),
            "name":queries.getName(str(queries.getCurrUser()[0][0])),
            "department":queries.getDept(queries.getCurrUser()[0][0]),
            }
    return render(request,"Faculty\COentry.html",context)

def ProgramW(request):
    context={
            "page":"ProgramW",
            "id":queries.getCurrUser()[0],
            "group":queries.getCurrUser()[1],
            "name":queries.getName(str(queries.getCurrUser()[0])),
            "department":queries.getDept(queries.getCurrUser()[0][0]),
            }
    return render(request,"Faculty\ProgramW.html",context)

def departmentWise(request):
    context={
            "page":"departmentWise",
            "id":queries.getCurrUser()[0],
            "group":queries.getCurrUser()[1],
            "name":queries.getName(str(queries.getCurrUser()[0])),
            "department":queries.getDept(queries.getCurrUser()[0][0]),
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
    fig=go.Figure()
    fig.add_trace(data=go.Scatterpolar(
        r = r1,
        theta = t,
        fill='toself',
        name="You",
    ))
    fig.add_trace(data=go.Scatterpolar(
        r = r2,
        theta = t,
        fill='toself',
        name="Department Average"
    ))
    return plot(fig, output_type='div',include_plotlyjs=True)

def TwoTraceLineChart(a,b,c):
    trace0 = go.Scatter(
        x=a,
        y=b
    )
    trace1 = go.Scatter(
        x=a,
        y=c
    )
    graph=[trace0,trace1]
    fig=go.Figure(data=graph)
    return plot(fig, output_type='div',include_plotlyjs=True)

def cowiseplo(user_id):
    df=pd.DataFrame({
        'PLONumber':queries.getCOWiseStudentPLO(user_id)[0],
        'CLO1':queries.getCOWiseStudentPLO(user_id)[2][0],
        'CLO2':queries.getCOWiseStudentPLO(user_id)[2][1],
        'CLO3':queries.getCOWiseStudentPLO(user_id)[2][2],
        'CLO4':queries.getCOWiseStudentPLO(user_id)[2][3]
    })
    fig = px.histogram(df,x="PLONumber",y=["CLO1","CLO2","CLO3","CLO4"])
    return plot(fig, output_type='div',include_plotlyjs=True)

def coursewiseplo(user_id):
    row=queries.getCourseWiseStudentPLOAnal(user_id)
    df=pd.DataFrame(data=row[2],
                    index=row[1],
                    columns=row[0])
    fig = px.histogram(df)
    return plot(fig, output_type='div',include_plotlyjs=True)

def PloCompare(user_id):
    df=pd.DataFrame({
        'PLONumber':queries.getStudentWisePLO(user_id)[0],
        'YourPLO':queries.getStudentWisePLO(user_id)[1],
        'DeptAverage':queries.getDeptWisePLO(queries.getDept(user_id))[1]
    })
    fig = px.histogram(df,x="PLONumber",y=["YourPLO","DeptAverage"],barmode='group')
    return plot(fig, output_type='div',include_plotlyjs=True)

def PLOAchieveTable(user_id):
        row=queries.getCourseWiseStudentPLO(user_id)
        df=[["Courses","PLO1","PLO2","PLO3","PLO4","PLO5","PLO6","PLO7","PLO8","PLO9","PLO10","PLO11","PLO12"]]
        for i in range(len(row[2])):
            df.append(row[2][i])
        fig=ff.create_table(df)
        return plot(fig, output_type='div',include_plotlyjs=True)
