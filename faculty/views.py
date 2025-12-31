from django.shortcuts import render,redirect
from django.http import HttpResponse , JsonResponse
import qrcode
from datetime import datetime
import io
import base64
from studentLogin.models import * 
from faculty.models import facultyReg
import uuid
from django.utils.timezone import localtime
from django.http import HttpResponse
from openpyxl import Workbook
from .models import *  
from django.utils.encoding import smart_str


def facultyLogin(request):
    if request.method == 'POST':
        faculty_id = request.POST.get('facultyId')
        password = request.POST.get('facultyPassword')
        print(f"Submitted ID: {faculty_id}, Password: {password}")
        try:
            faculty = facultyReg.objects.get(facultyId=faculty_id, facultyPassword=password)
            request.session['faculty_id'] = faculty.id  # putting faculty ID in session
            return redirect('facultyDashboard')
        except facultyReg.DoesNotExist:
            return render(request, 'facultyLogin.html', {
                'error': 'Invalid Faculty ID or Password'
            })

    return render(request, 'facultyLogin.html')

def facultyRegistration (request):
    return render(request , "facultyRegistration.html")

def getFacultyIp(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    print("Faculty IP:", ip)
    return ip

def facultyDashboard(request):
    faculty_id = request.session.get('faculty_id')
    if not faculty_id:
        return HttpResponse("Not logged in.")

    faculty = facultyReg.objects.get(id=faculty_id)

    # new session
    qr_code_data = str(uuid.uuid4())
    faculty_ip = getFacultyIp(request)
    print(f"Faculty IP: {faculty_ip}")
    session = AttendanceSession.objects.create(qr_code_data=qr_code_data, faculty=faculty)

    qr_payload = f"{qr_code_data}|{faculty_ip}"

    # QR code geneeration
    qr = qrcode.make(qr_payload)
    buffer = io.BytesIO()
    qr.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    img_data = f"data:image/png;base64,{img_str}"

 
    attendance_records = AttendanceRecord.objects.filter(session__faculty=faculty).select_related('student', 'session').order_by('-marked_at')

    return render(request, "facultyDashboard.html", {
        "qr_code": img_data,
        "qr_code_data": qr_code_data,
        "attendance_records": attendance_records,
        "session": session
    })

def get_attendance_records(request, session_id):#ajax
    records = AttendanceRecord.objects.filter(session_id=session_id).select_related('student')

    data = [
        {
            "name": r.student.studentName,
            "hall_ticket": r.student.hallTicketNum,
            "timestamp": localtime(r.marked_at).strftime("%d-%m-%Y %H:%M:%S")
        }
        for r in records
    ]
    return JsonResponse({"records": data})

def facultyLogout(request):
    print("Faculty Logout")
    request.session.flush()  # Clears all session data
    return redirect('facultyLogin')

def download_attendance_excel(request, session_id):
    # Create a new Excel workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Attendance"

    # Header row
    ws.append(['Student Name', 'Hall Ticket Number', 'Phone Number', 'Marked At'])

    # Get records for the specified session
    records = AttendanceRecord.objects.filter(session_id=session_id).select_related('student')

    # Add rows to Excel
    for record in records:
        student = record.student
        ws.append([
            student.studentName,
            student.hallTicketNum,
            student.phoneNum,
            localtime(record.marked_at).strftime('%d-%m-%Y %H:%M:%S')
        ])

    # Prepare HTTP response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=attendance_session_{session_id}.xlsx'

    # Save the workbook into the response
    wb.save(response)
    return response
