"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from home.views import *
from studentLogin.views import * 
from faculty.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home1 , name="home1" ),
    path('studentLogin/', studentLogin, name="studentLogin"),
    path('studentLogin/studentDashboard', studentDashboard, name="studentDashboard"),
    path('studentLogin/studentRegistration/', studentRegistration, name="studentRegistration"),
    path('studentLogin/studentDashboard/markAttendance/', mark_attendance, name='mark_attendance'),
    path('studentLogin/studentDashboard/studentLogout', studentLogout, name='studentLogout'),

    path('facultyLogin/', facultyLogin, name="facultyLogin"),
    path('facultyLogin/facultyRegistration/', facultyRegistration, name="facultyRegistration"),
    path('facultyLogin/facultyDashboard/', facultyDashboard, name="facultyDashboard"),
    path('facultyLogin/facultyDashboard/facultyLogout/', facultyLogout, name='facultyLogout'),

    path('get_attendance_records/<int:session_id>/', get_attendance_records, name='get_attendance_records'),
    path('download-attendance/<int:session_id>/', download_attendance_excel, name='download_attendance_excel'),

    #path('studentLogin/verify-face/', verify_face, name='verify_face'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
