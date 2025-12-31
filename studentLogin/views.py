from django.shortcuts import render,redirect
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.db import connection
from django.http import HttpResponse
from faculty.models import *
from faculty.views import *

def studentLogin (request):
    if request.method == 'POST':
        form = StudentLoginForm(request.POST)
        if form.is_valid():
            ID = form.cleaned_data.get('hallTicketNum')
            PASSWORD = form.cleaned_data.get('studentPassword')
            try:
                student = studentReg.objects.get(hallTicketNum=ID, studentPassword=PASSWORD)
                
                request.session['student_id'] = student.id
                return redirect('studentDashboard')
            except studentReg.DoesNotExist:
                messages.error(request, 'Invalid hall ticket number or password.')

    else:
        form = StudentLoginForm()
    
    return render(request, 'studentLogin.html', {'form': form})

def studentRegistration (request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST , request.FILES)
        if form.is_valid():
            form.save()  
            return redirect('studentDashboard')
    else:
        form = StudentRegistrationForm()
    return render(request , 'studentRegistration.html', {'form': form})

def studentDashboard(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('studentLogin')
    student= studentReg.objects.get(id=student_id)
    
    total_sessions = AttendanceSession.objects.count()  # Total lectures conducted
    attended_sessions = AttendanceRecord.objects.filter(student=student).count()  # Total attended
    if total_sessions > 0 :
        percentage = (attended_sessions / total_sessions) * 100  
    else:
        0
    return render(request, 'studentDashboard.html', {'student': student , 'attendance_percentage': round(percentage, 2)})

def getStudentIp(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    print("Student IP:", ip)
    return ip

def sameSubnet(ip1, ip2):
    return ip1.split('.')[:3] == ip2.split('.')[:3]

def mark_attendance(request):
    if request.method == 'POST':
        qr_code_data_ip = request.POST.get('qr_code_data')
        student_id = request.session.get('student_id')

        if not student_id:
            return HttpResponse("Not logged in.")

        try:
            qr_code_data, faculty_ip = qr_code_data_ip.split('|') 
        except ValueError:
            return HttpResponse("Invalid QR data format.")

        student_ip = getStudentIp(request)

        if not sameSubnet(faculty_ip, student_ip):
            return HttpResponse("You must be on the same network as your faculty.")


        try:
            session = AttendanceSession.objects.get(qr_code_data=qr_code_data)
            student = studentReg.objects.get(id=student_id)

            AttendanceRecord.objects.create(student=student, session=session)
            return HttpResponse("Attendance marked successfully!")

        except AttendanceSession.DoesNotExist:
            return HttpResponse("Invalid QR code.")

        except:
            return HttpResponse("You have already marked attendance.")
        print("Attendance saved for:", student.studentName)
    return render(request, 'studentScanQR.html')

def studentLogout(request):
    print("Student Logout")
    request.session.flush()  
    return redirect('studentLogin')