from django.urls import path

from . import views

urlpatterns = [
    path('showinfo', views.show_info, name='showinfo'),
    path('create-pdf', views.pdf_report_create, name='create-pdf'),
]