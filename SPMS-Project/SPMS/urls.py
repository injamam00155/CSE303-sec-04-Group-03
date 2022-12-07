"""SPMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from SPMS import views

urlpatterns = [
    path('', views.login),
    path('shome', views.authenticate, name='authenticationHome'),
    path('home', views.home,name="home"),
    path('logout', views.logout,name="logout"),
    path('CoPloAnal', views.CoPloAnal,name="CoPloAnal"),
    path('coursePloAnal', views.coursePloAnal,name="coursePloAnal"),
    path('PloAchievement', views.PloAchievement,name="PloAchievement"),
    path('QuestionBank', views.QuestionBank,name="QuestionBank"),
    path('QuestionBankEntry',views.QuestionBankEntry,name="quesentry"),
    path('StuPloAnal',views.StuPloAnal,name="StuPloAnal"),
    path('StuPloTbl',views.StuPloTbl,name="StuPloTbl"),
    path('CourseReport',views.CourseReport,name="CourseReport"),
    path('coentry',views.COentry,name="coentry"),
    path('pdf',views.pdf,name="pdf_convert"),

]